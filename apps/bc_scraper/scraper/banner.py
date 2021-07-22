from html.parser import HTMLParser


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
