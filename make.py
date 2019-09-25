#! /usr/bin/env python3
import os.path
import argparse

import dhtmlparser
from ebooklib import epub


class BookGenerator:
    def __init__(self):
        self.book = epub.EpubBook()
        self.title = 'Environment and the programming language Self'
        self.chapters = []

        # book.set_identifier('id123456')
        self.book.set_title(self.title)
        self.book.set_language('en')
        self.book.add_author('Bystroushaak')

    def generate_ebook(self, path):
        self._add_css()
        self._add_toc()

        epub.write_epub(path, self.book, {})

    def add_chapter(self, chapter):
        self.book.add_item(chapter)
        self.chapters.append(chapter)

    def _add_toc(self):
        self.book.toc = (
            (epub.Section(self.title),
             self.chapters),
        )

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        self.book.spine = ['nav'] + self.chapters

    def _add_css(self):
        # define CSS style
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style
        )

        self.book.add_item(nav_css)


def pick_first_chapter(html_path):
    article_path = 'Environment and the programming language Self part.html'

    with open(os.path.join(html_path, article_path)) as f:
        data = f.read()
        dom = dhtmlparser.parseString(data)

    title = dom.find("title")[0].getContent()
    title = title.split("(")[-1].split(")")[0].capitalize()

    c1 = epub.EpubHtml(title=title, file_name='chap_01.xhtml')

    body = dom.find("div", {"class":"page-body"})[0]

    while body.childs[0].getTagName() != "hr":
        body.childs.pop(0)
    body.childs.pop(0)

    while body.childs[-1].getContent() != "Next episodes":
        body.childs.pop()
    body.childs.pop()

    c1.content = body.getContent()

    return c1


def pick_second_chapter(html_path):
    article_path = 'Environment and the programming language Self part 1.html'
    c2 = epub.EpubHtml(title='Second', file_name='chap_02.xhtml')
    c2.content = u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

    return c2


def pick_third_chapter(html_path):
    article_path = 'Environment and the programming language Self part 2.html'
    c3 = epub.EpubHtml(title='Third', file_name='chap_03.xhtml')
    c3.content = u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

    return c3


def pick_fourth_chapter(html_path):
    article_path = 'Environment and the programming language Self part 3.html'
    c4 = epub.EpubHtml(title='Fourth', file_name='chap_04.xhtml')
    c4.content = u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

    return c4


def put_ebook_together(html_path):
    book = BookGenerator()

    book.add_chapter(pick_first_chapter(html_path))
    # book.add_chapter(pick_second_chapter(html_path))
    # book.add_chapter(pick_third_chapter(html_path))
    # book.add_chapter(pick_fourth_chapter(html_path))

    book.generate_ebook('test.epub')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "PATH",
            help="Path to the directory with the blog section about Self."
    )
    args = parser.parse_args()

    put_ebook_together(args.PATH)
