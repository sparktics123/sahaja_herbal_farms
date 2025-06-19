import os
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

REPO_ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = list(REPO_ROOT.glob('*.html'))


def extract_nav_links(html_path: Path):
    """Return href values from navigation menus in the HTML file."""
    soup = BeautifulSoup(html_path.read_text(encoding='utf-8'), 'html.parser')
    links = []
    for a in soup.select('.clv_menu_nav a[href]'):
        href = a.get('href')
        if href:
            links.append(href.strip())
    return links


@pytest.mark.parametrize('html_file', HTML_FILES, ids=[p.name for p in HTML_FILES])
def test_navigation_links_exist(html_file: Path):
    links = extract_nav_links(html_file)
    for href in links:
        if href.startswith(('http://', 'https://', 'javascript:', '#')):
            continue
        if href.endswith('.html'):
            target = (REPO_ROOT / href)
            assert target.exists(), f"{html_file.name} links to missing {href}"

