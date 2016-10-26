'''Convert arxiv list to a bibtex file with nice annotations

Usage:
    arxiv2bib INFILE [-o OUTFILE]

Options:
    INFILE            specify the filename to process
    -o,--out            specify the optional out name

'''
import cgi
import re
import urllib
from xml.etree import ElementTree
import xml.etree
import os
import sys
from docopt import docopt
maxpapers=100

def format_one(pub, format='bibtex'):
    """
        Input: dictionary with publication data.
        Output: BibTeX record 
    """ 
    for key, values in pub.items():
        if isinstance(values, list):
            if len(values) > 0 and isinstance(values[0], list):
                continue    
            values = [v.encode('utf8') for v in values]
        else:
            values = values.encode('utf8')
        pub[key] = values
    is_published = (pub['journal'] != None) or (pub['dois'] != None and len(pub['dois']) > 0)
    pub['pub_type'] = ("@online" if format == "biblatex" else "@misc") if not is_published else "@article"
    pub['eprint'] = ("" if format=='biblatex' else "arXiv:") + str(pub['id'])
    pub['authors'] = ', '.join(pub['authors'])
    bib_entry = """{pub_type}{{{id},
    author={{{authors}}},
    title={{{title}}}, 
    year={{{year}}}, 
    abstract={{{abstract}}},
    link={{{page_url}}}
    }}
    """
    try:
        bib_entry = bib_entry.format(**pub)
    except UnicodeEncodeError as e:
        print("pub is breaking things: ")
        print(pub)
        for k,v in pub.items():
            try:
                print("{}".format(v))
            except Exception as e:
                print("found it")
                print(k,v)
                print(k,v.encode('utf8'), type(v))
                break
        raise e


    return bib_entry

def parse_one(paper):
    title_element = paper.find("{http://www.w3.org/2005/Atom}title")
    if title_element == None:
        return
    title = re.sub(r"\s*\n\s*", r" ", title_element.text)
    authors = paper.getiterator("{http://www.w3.org/2005/Atom}author")
    authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in authors]
    abstract = paper.find("{http://www.w3.org/2005/Atom}summary").text.strip()
    links = paper.getiterator("{http://www.w3.org/2005/Atom}link")
    pdf_url = ""
    page_url = ""
    for link in links:
        attributes = link.attrib
        if attributes.has_key("href"):
            linktarget = attributes["href"]
            linktype = attributes["type"] if attributes.has_key("type") else None
            linktitle = attributes["title"] if attributes.has_key("title") else None
        if linktype == "application/pdf":
            pdf_url = linktarget
        elif linktype == "text/html":
            page_url = linktarget
    paper_id = page_url.split("/abs/")[-1].split("v")[0]
    year = paper.find("{http://www.w3.org/2005/Atom}published").text.split('-')[0]
    dois = [doi.text for doi in paper.getiterator("{http://arxiv.org/schemas/atom}doi")]
    journal = paper.find("{http://arxiv.org/schemas/atom}journal_ref")
    journal = "" if journal is None else journal.text
    pub = dict(id=paper_id, authors=authors, title=title, abstract=abstract, dois=dois, 
               journal=journal, year=year, pdf_url=pdf_url, page_url=page_url)
    return pub


def retrieve(arxiv_ids):
        arxiv_url = "http://export.arxiv.org/api/query?id_list=" + ",".join(arxiv_ids) + "&max_results=" + str(maxpapers)
        download = urllib.urlopen(arxiv_url)
        download.encoding = "UTF-8"
        data = download.read()
        if data == None:
            print("could not retrieve anything")
        else:
            feed = xml.etree.ElementTree.fromstring(data)
            first_title = feed.find("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}title")
            if first_title == None or first_title.text == "Error":
                print("could not retreive anything")
            else:
                papersiterator = feed.getiterator("{http://www.w3.org/2005/Atom}entry")
                for paper in papersiterator:
                    pub = parse_one(paper)
                    pub = format_one(pub)
                    yield pub

#for pub in retrieve(['1608.00525']):
#   print(pub)

if __name__ == '__main__':
    args = docopt(__doc__, version="arxvi2bib; v0.2")
    print(args)
    inname = args['INFILE']
    if args['--out']:
        outname = args['OUTFILE']
    else:
        outname = args["INFILE"] + ".bib"
    with open(inname) as fp:
        arxivids = [x.replace("\n","").strip() for x in fp.readlines()]

    with open(outname, 'w') as fp:
        fp.write("% title: {}; from arxiv\n".format(args['INFILE']))
        fp.write("% categories: bibs\n")
        fp.write("% description: automatically generated from arxiv2bib.py\n\n")
        fp.write("\n\n".join(retrieve(arxivids)))
