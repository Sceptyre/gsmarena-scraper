from bs4 import BeautifulSoup

def parse_html(html_str: str) -> BeautifulSoup:
    return BeautifulSoup(html_str, 'html.parser')

def parse_xml(xml_str: str) -> BeautifulSoup:
    return BeautifulSoup(xml_str, 'xml')