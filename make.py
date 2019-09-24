#! /usr/bin/env python3
import argparse

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
        self._add_first_chapter()
        self._add_css()
        self._add_toc()

        epub.write_epub(path, self.book, {})

    def _add_first_chapter(self):
        c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml')
        c1.content=u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

        self.book.add_item(c1)
        self.chapters.append(c1)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "PATH",
            help="Path to the directory with the blog section about Self."
    )

    args = parser.parse_args()

    book = BookGenerator()
    book.generate_ebook('test.epub')
