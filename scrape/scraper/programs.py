from html.parser import HTMLParser
import requests


class _ProgramParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.toogle = False
        self.text = ''

    def process(self, text):
        self.toogle = False
        self.text = ''
        self.feed(text)
        return self.text

    def handle_starttag(self, tag, attrs):
        if tag == 'pre' and not self.toogle:
            self.toogle = True
            self.text = ''
        elif self.toogle:
            self.text += f'<{tag}>'

    def handle_endtag(self, tag):
        if tag == 'pre' and self.toogle:
            self.toogle = False
        elif self.toogle:
            self.text += f'</{tag}>'

    def handle_data(self, data):
        if self.toogle:
            self.text += data


def get_program(initials):
    parser = _ProgramParser()
    query = f'http://catalogo.uc.cl/index.php?tmpl=component&view=programa&sigla={initials}'
    text = requests.get(query).text
    return parser.process(text)
