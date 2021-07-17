import psycopg2
import requests
from html.parser import HTMLParser
import sys
from datetime import datetime
import json
from time import sleep


# SETUP
if len(sys.argv) < 2:
    print("Debe entragar los argumentos AÑO y SEMESTRE")
    print("ej: python banner.py 2020 1")
    exit()
ANO = sys.argv[1]
SEMESTRE = sys.argv[2]
PERIOD = ANO + "-" + SEMESTRE

BANNER = "0"
if "-b" in sys.argv:
    BANNER = sys.argv[sys.argv.index("-b") + 1]

settings = None
with open("settings.json") as file:
    settings = json.load(file)

BATCH_SIZE = settings["batch_size"]
BATCH_SIZE = 25
INSERT = f"INSERT INTO courses_quota (section_id, date, category, quota, banner) VALUES (%s, %s, %s, %s, '{BANNER}');"
UPDATE = "UPDATE courses_section SET available_quota=%s WHERE id=%s;"


class BannerParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.toogle = False
        self.values = {}
        self.col = 0
        self.cupos = None

    def process(self, text):
        self.toogle = False
        self.values = {}
        self.col = 0
        self.name = ""
        self.feed(text)
        return self.values

    def handle_starttag(self, tag, attrs):
        if not self.toogle and tag == "tr" and ("class", "resultadosRowImpar") in attrs:
            self.toogle = True
        if tag == "td" and self.toogle:
            self.col += 1

    def handle_endtag(self, tag):
        if tag == "tr":
            self.col = 0

    def handle_data(self, data):
        data = data.strip()
        if data == "&nbsp;":
            self.toogle = False
        if self.toogle and data:
            if self.col < 5:
                self.name = data
            elif self.col < 7:
                self.name += " - " + data
            elif self.col == 9:
                self.values[self.name] = int(data)
                self.name = ""


class BannerBCParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.toogle = False
        self.col = 0
        self.cupos = None

    def process(self, text):
        self.toogle = False
        self.col = 0
        self.cupos = None
        self.feed(text)
        return self.cupos

    def handle_starttag(self, tag, attrs):
        if not self.toogle and tag == "tr" and ("class", "resultadosRowPar") in attrs:
            self.toogle = True
        if tag == "td" and self.toogle:
            self.col += 1

    def handle_endtag(self, tag):
        if tag == "tr":
            self.col = 0

    def handle_data(self, data):
        if self.col == 15 and self.toogle:
            self.cupos = int(data.strip())
            self.toogle = False


# START
print("Collecting quotas for", PERIOD)
db_conn = psycopg2.connect(
    host=settings["db_host"],
    user=settings["db_user"],
    password=settings["db_passwd"],
    dbname=settings["db_name"],
)
db_cursor = db_conn.cursor()

db_cursor.execute(f"SELECT COUNT(*) FROM courses_section WHERE period = '{PERIOD}';")
total = int(db_cursor.fetchone()[0])
print(total, "courses found.")

offset = 0
parser = BannerParser()
parser_bc = BannerBCParser()
while offset < total:
    # Process by batches
    print("Collecting from", offset, "to", offset + BATCH_SIZE, "of", total)
    db_cursor.execute(
        f"SELECT id, nrc FROM courses_section WHERE period = '{PERIOD}' ORDER BY id LIMIT {BATCH_SIZE} OFFSET {offset};"
    )
    cursos = db_cursor.fetchall()
    for curso in cursos:
        id = int(curso[0])
        nrc = curso[1]
        query = f"http://buscacursos.uc.cl/informacionVacReserva.ajax.php?nrc={nrc}&termcode={PERIOD}"
        text = requests.get(query).text
        # sleep(0.1)
        date = str(datetime.now())
        cupos_dict = parser.process(text)
        if not len(cupos_dict):
            # Solo vacantes libres, buscar en página principal
            query = f"http://buscacursos.uc.cl/?cxml_semestre={PERIOD}&cxml_nrc={nrc}"
            text = requests.get(query).text
            cupos_dict = {"Total": parser_bc.process(text)}

        try:
            values = []
            free_quota = 0
            for categoria, cupos in cupos_dict.items():
                values.append((id, date, categoria, cupos))
                free_quota += cupos
            if not len(values):
                raise Exception("Nothing scrapped.")
            db_cursor.executemany(INSERT, values)
            db_cursor.execute(UPDATE, (str(free_quota), id))
            db_conn.commit()
            print(db_cursor.rowcount, "id scrapped:", id)
        except Exception as err:
            print(err)
            with open("logs/error.log", "a+") as log:
                log.write("Error: " + str(err) + "\n")
                log.write("Context: " + str([id, date, BANNER, cupos_dict]) + "\n")

    offset += BATCH_SIZE
    sleep(1.5)

db_cursor.close()
db_conn.close()
