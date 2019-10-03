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

    def add_image(self, image):
        self.book.add_item(image)

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


class EAPLSEpub:
    def __init__(self, html_root):
        self.html_root = html_root
        self.book = BookGenerator()

        self.add_foreword()

        self.chapters_metdata = [
            ('Environment and the programming language Self part.html',
             'chap_01.xhtml'),
            ('Environment and the programming language Self part 1.html',
             'chap_02.xhtml'),
            ('Environment and the programming language Self part 2.html',
             'chap_03.xhtml'),
            ('Environment and the programming language Self part 3.html',
             'chap_04.xhtml'),
        ]

        for article_path, chapter_fn in self.chapters_metdata:
            self.convert_chapter(article_path, chapter_fn)

    def add_foreword(self):
        chapter = epub.EpubHtml(title="Foreword", file_name="foreword.html")
        chapter.content = """
<p>This book was converted from the HTML articles originally published at my blog
<a href="http://blog.rfox.eu">blog.rfox.eu</a>.</p>

<p>I want to apologize for the low quality of the export. If you feel like you
want to improve the quality, your contribution is most welcomed:<p>

<ul>
    <li><a href=""></a></li>
</ul> 
        """
        self.book.add_chapter(chapter)

    def convert_chapter(self, article_path, chapter_fn, title=None):
        with open(os.path.join(self.html_root, article_path)) as f:
            dom = dhtmlparser.parseString(f.read())

        if not title:
            title = dom.find("title")[0].getContent()
            title = title.split("(")[-1].split(")")[0].capitalize()

        body = dom.find("div", {"class":"page-body"})[0]

        self._remove_fluff_from_the_beginning(body)
        self._remove_fluff_from_the_end(body)
        self._inline_images(body)

        chapter = epub.EpubHtml(title=title, file_name=chapter_fn)
        chapter.content = body.getContent()
        self.book.add_chapter(chapter)

    def _remove_fluff_from_the_beginning(self, body):
        while body.childs[0].getTagName() != "hr":
            body.childs.pop(0)
        body.childs.pop(0)

    def _remove_fluff_from_the_end(sefl, body):
        look_for = ["Next episodes", "Next episode", "Last episode", "Relevant discussions"]

        selected_phrase = ""
        for phrase in look_for:
            if body.find("h1", fn=lambda x: x.getContent() == phrase):
                selected_phrase = phrase
                break
        else:
            return

        while body.childs[-1].getContent() != selected_phrase:
            body.childs.pop()
        body.childs.pop()

    def _inline_images(self, body):
        for img in body.find("img"):
            epub_img = epub.EpubImage()

            epub_img.file_name = os.path.basename(img.params["src"])
            image_path = os.path.join(self.html_root, img.params["src"])
            with open(image_path, "rb") as f:
                epub_img.content = f.read()

            if "style" in img.params:
                del img.params["style"]

            self.book.add_image(epub_img)
            img.params["src"] = epub_img.file_name

    def generate_ebook(self, path):
        return self.book.generate_ebook(path)


def put_ebook_together(html_path):
    book = EAPLSEpub(html_path)
    book.generate_ebook('environment_and_programming_language_self_2019.epub')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "PATH",
            help="Path to the directory with the blog section about Self."
    )
    args = parser.parse_args()

    put_ebook_together(args.PATH)
