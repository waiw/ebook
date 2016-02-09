from ebooklib import epub
import urllib
from bs4 import BeautifulSoup

def get_content(url):
    r = urllib.urlopen(url).read()
    s = BeautifulSoup(r, "html.parser")
    div = s.find('div',{"class":"book"})
    title = div.h1.string
    author = div.h2.a.string
    print title
    print author
    chapters = []
    count = 1
    for line in div.dl.find_all('a', href=True):
        print line
        chapters.append([line['href'], line.string, ('chap_'+str(count)+'.xhtml')])
        count = count + 1
    return title,author,chapters

def create_catalog(chapters):
    s = BeautifulSoup("<body><p></p></body>")
    for ch in chapters:
        new_tag = s.new_tag("a", href=ch[2])
        new_tag.string = ch[1]
        s.p.append(new_tag)
        s.p.append(s.new_tag("br"))
    return s

 
def get_paragraph(url):
    r = urllib.urlopen(url).read()
    s = BeautifulSoup(r, "html.parser")
    p = s.find('p', attrs={'class':None})

    return p


if __name__ == "__main__":
    url = 'http://wx.ty2016.net/book/shendiaoxialv/'
    book = epub.EpubBook()

    #set metadata
    #book.set_identifier('id12334')
    title, author, chapters = get_content(url)
    book.set_title(title)
    #book.set_language('')
    book.add_author(author)

    style = '''h1{text-align:right; margin-right:2em; page-break-before: always; font-size:1.6em; font-weight:bold;} h3 { text-align: center;}p.center{text-align:center;}p.catalog{margin:20px 10px;padding:0;}'''
    default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)

    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    #Create Introduction
    p = get_paragraph(url)
    c = epub.EpubHtml(title='Introduction', file_name='intro.xhtml')
    c.content='<h1>Introduction</h1>'+str(p).decode("utf8")
    c.add_item(default_css)
    book.add_item(c)
    book.toc.append((epub.Section('Introduction'),(c,)))
    book.spine.append(c)

    #Create catalog.html
    c = epub.EpubHtml(title='Catalog', file_name='catalog.xhtml')
    c.content= str(create_catalog(chapters))
    c.add_item(default_css)
    book.add_item(c)
    book.toc.append((epub.Section('Catalog'),(c,)))
    book.spine.append(c)

    for ch in chapters:
        p = get_paragraph(url+ch[0]) 
        c = epub.EpubHtml(title=ch[1], file_name=ch[2])
        c.content='<h1>'+ch[1]+'</h1>'+str(p).decode("utf8")
        c.add_item(default_css)
        book.add_item(c)
        book.toc.append((epub.Section(ch[1]),(c,)))
        book.spine.append(c)

    # add navigation files
    book.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    nav.add_item(nav_css)
    book.add_item(nav)

    # add css files
    book.add_item(default_css)
    book.add_item(nav_css)

    epub.write_epub(title+'.epub', book)
