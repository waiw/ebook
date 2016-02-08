from ebooklib import epub
import urllib
from bs4 import BeautifulSoup

def parse_content(url):
    r = urllib.urlopen(url).read()
    s = BeautifulSoup(r, "html.parser")
    div = s.find('div',{"class":"book"})
    title = div.h1.string
    author = div.h2.a.string
    print title
    print author
    chapters = 'test'


    return title,author,chapters

 



if __name__ == "__main__":
    book = epub.EpubBook()

    #set metadata
    #book.set_identifier('id12334')
    title, author, chapters = parse_content('http://wx.ty2016.net/book/shendiaoxialv/')
    book.set_title(title)
    #book.set_language('')
    book.set_author(author)


    count = 1
    for line in soup.dl.find_all('a', href=True):
        print line.string
