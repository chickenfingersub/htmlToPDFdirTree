#original bookmarks2fs https://github.com/bookmarks-tools/bookmarks2fs/blob/master/bookmarks2fs.py
import configparser
from pathlib import Path
import base64
from urllib.parse import urlparse
import bookmarks_parser
import unicodedata
import re
import pdfkit
import os
import shutil

config = configparser.RawConfigParser()
config.optionxform = str

def create_bookmark(bookmark, folder_name):
    title = re.sub('[^0-9a-zA-Z]+', '_', bookmark['title'])
    html = re.sub('#(\.css|\.js)\?[^"]+#',  '$1', bookmark['url'])
    options = {
        "load-error-handling ignore": None,
        "load-error-handling ignore": None,
        "load-media-error-handling ignore": None
    }
    if bookmark.get('title'):
        domain_name = urlparse(bookmark['url'])
        relative_path = Path("icons/{}.png".format(domain_name))
        if not relative_path.exists():
            path = Path.cwd() / relative_path
        else:
            path = Path.cwd() / domain_name
        try:
            pdfkit.from_url(html,('{}/{}'.format(folder_name,  title+'.pdf', options=options)))
        except OSError as e:
            if 'Done' not in str(e):
               raise e
    else:
        try:
            pdfkit.from_url(html,('{}/{}'.format(folder_name,  title+'.pdf', options=options)))
        except OSError as e:
            if 'Done' not in str(e):
               raise e

def title2path(child, prev=None):
    for bookmark in child:
        if bookmark.get('children'):
            if prev:
                bookmark['title'] = '{}/{}'.format(prev['title'], bookmark['title'])
            bookmark_folder_path = Path(bookmark['title'])
            if not bookmark_folder_path.exists():
                bookmark_folder_path.mkdir()
            if bookmark['children']:
                title2path(bookmark['children'], bookmark)
        elif bookmark['type'] == 'bookmark':
            create_bookmark(bookmark, prev['title'])

if __name__ == '__main__':
    bookmarks = bookmarks_parser.parse("test.html")
    p = Path('icons')
    if not p.exists():
        p.mkdir()
    title2path(bookmarks)
