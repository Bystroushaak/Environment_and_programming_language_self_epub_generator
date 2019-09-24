#! /usr/bin/env python3
import argparse

from ebooklib import epub


def generate_ebook(path):
    book = epub.EpubBook()

    # book.set_identifier('id123456')
    title = 'Environment and the programming language Self'
    book.set_title(title)
    book.set_language('en')
    book.add_author('Bystroushaak')

    # create chapter
    c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml')
    c1.content=u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

    # add chapter
    book.add_item(c1)

    # define Table Of Contents
    book.toc = (
        epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
        (epub.Section(title),
         (c1,))
    )

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=style
    )

    # add CSS file
    book.add_item(nav_css)

    # basic spine
    book.spine = ['nav', c1]

    # write to the file
    epub.write_epub(path, book, {})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "PATH",
            help="Path to the directory with the blog section about Self."
    )

    args = parser.parse_args()

    generate_ebook('test.epub')