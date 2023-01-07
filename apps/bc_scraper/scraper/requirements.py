from .request import get_text
from html.parser import HTMLParser
from django.conf import settings

CATALOGO_URL = getattr(settings, "CATALOGO_URL")


class _RequirementsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.toogle = False
        self.values = []

    def process(self, text):
        self.toogle = False
        self.values = []
        self.feed(text)
        return self.values[0], self.values[1], self.values[2]

    def handle_starttag(self, tag, attrs):
        if tag == "span" and not self.toogle:
            self.toogle = True

    def handle_endtag(self, tag):
        if tag == "span" and self.toogle:
            self.toogle = False

    def handle_data(self, data):
        if self.toogle and data:
            self.values.append(data)


def get_requirements(initials):
    parser = _RequirementsParser()
    query = f"{CATALOGO_URL}/index.php?tmpl=component&view=requisitos&sigla={initials}"
    text = get_text(query)
    return parser.process(text)
