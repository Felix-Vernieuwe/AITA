import markdown
from bs4 import BeautifulSoup

def plain_text(source, is_markdown=True):
    if is_markdown: source = html(source)
    soup = BeautifulSoup(source, features="html.parser")
    return soup.get_text()

def html(source):
    return markdown.markdown(source)
