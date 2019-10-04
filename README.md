# EAPLS generator

This is a script that takes a bunch of .html files from [my series of articles about the programming language Self](http://blog.rfox.eu/Bystroushaak%20s%20blog/English%20section/Series%20about%20Self.html) and converts them to epub.

## How to use

Clone my blog:

    git clone https://github.com/Bystroushaak/notion_blog.git

Install requirements:

    pip3 install --user -r requirements.txt

Run conversion script with path to the series root dir

    ./make.py notion_blog/blog/Bystroushaak\ s\ blog/English\ section/Series\ about\ Self/

Optionally, you can also run the calibre conversion script to fix all kind of wrongness with the epub:

    ebook-convert environment_and_programming_language_self_2019.epub environment_and_programming_language_self_2019_cleaned.epub
