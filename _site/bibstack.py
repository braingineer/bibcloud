import time
import bibtexparser
import glob
import os
import logging
import logging.config

bp = bibtexparser.bparser.BibTexParser()
bp.ignore_nonstandard_types=False

class Bib(object):
    def __init__(self, db):
        self.entries = [BibEntry(e) for e in db.entries]

class BibEntry(object):
    def __init__(self, bibentry):
        default = {k:'Empty' for k in ['link', 'title', 'author', 'abstract', 'notes', 'year']}
        default['link'] = "#"
        self.__dict__.update(default)
        self.__dict__.update({k:v.encode('utf-8') for k,v in bibentry.items()})
        self.abstract = self.abstract.replace("\n", " ")
        self.saved = bibentry


def make(bib_filepath):
    with open(bib_filepath) as bibtex_file:
        bib_contents = bibtex_file.read()
        special = [line.replace("%","").split(":") for line in bib_contents.split("\n") if "%" in line]
        special = [line for line in special if len(line)>1]
        special = {k.strip():v.strip() for k,v in special}
        bib_blob = Bib(bibtexparser.loads(bib_contents, parser=bp))

    template = """<li>
                  <div id='entry{0}' class='bib entry'>

                    <a href='{1.link}' class='title'>{1.title}</a>
                    <br><span class='author'>{1.author}.</span> <br>
                    <span class='year'>{1.year}</span><br>
                    <div id='annotation{0}hider' class='bib no-selection btn'>hide annotations</div>
                    <div id='anno{0}' class='bib annotation'>
                          <div id='abstract{0}' class='bib abstract'><b>Abstract</b>
                            {1.abstract}</div>
                          <div id='notes{0}' class='bib notes'><b>Notes</b>
                           {1.notes}</div>
                    </div>
                  </div>
                 </li>
                """

    output = "<div id='bibitems'><div class='btn-container'>"
    output += "<br><input class='search' placeholder='Search title, authors, abstract, and notes'/><br>"
    output += "<button class='sort' data-sort='author'>Sort by Author</button>"
    output += "<button class='sort' data-sort='year'>Sort by Year</button>"
    output += "<button class='sort' data-sort='title'>Sort by Title</button>"
    output += "<button id='showhide'>Expand all annotations</button></div>\n"
    output += "<ul class='bib list'>"
    ender = "</ul></div>"
    js = "\n<script>var options={valueNames:['title','author','year', 'abstract', 'notes']};\n"
    js += "var userList = new List('bibitems', options);</script>"
    mutualall = "<script> var allshowing=false; \n"
    showall = "function showall() { \n"
    showall += "allshowing=true;\n"
    hideall = "function hideall() { \n"
    hideall += "allshowing=false;"
    for i, entry in enumerate(bib_blob.entries):
        #if i == 0 and "feb" in bib_filepath:
        #    print(entry.saved)
        #    print(bib_filepath)

        output += template.format(i, entry) + "\n"
        js += make_js(i) + "\n"
        showall+="bibentry{0}on = false; $('#annotation{0}hider').click();\n".format(i)
        hideall+="bibentry{0}on = true; $('#annotation{0}hider').click();\n".format(i)
        #print(showall)
    output += ender
    showall += "}\n"
    hideall += "}\n"
    finalall = mutualall + hideall + showall
    finalall += "$('#showhide').click(function() {"
    finalall += "if (allshowing) { hideall(); $('#showhide').html('Expand all annoations');}"
    finalall += "else { showall(); $('#showhide').html('Hide all annoations');}});"
    finalall += "</script>"
    js += finalall+"\n"

    return output, js, special

def make_js(num):
    output = """<script>
        var bibentry{0}on = true;
        $('#annotation{0}hider').click(function() {{
            console.trace('here');
            if (bibentry{0}on) {{
                $('#annotation{0}hider').html('show annotations');
                $('#anno{0}.bib.annotation').css('display', 'none');
                bibentry{0}on = false;
            }}
            else {{
                $('#anno{0}.bib.annotation').css('display', 'inherit');
                $('#annotation{0}hider').html("hide annotations");
                bibentry{0}on = true;
            }}
        }});
        $('#annotation{0}hider').click();</script>""".encode("utf-8").format(num)
    return output

def make_all():
    basepath = "/home/cogniton/research/code"
    bibpath = basepath+"/chronicles/wiki/dissertation/bibs"
    devblogpath = basepath+"/devblog/_drafts"
    for filename in glob.glob(os.path.join(bibpath, "*.bib")):
        bibname = filename.split("/")[-1].replace(".bib", "")
        content, js,meta = make(filename)
        with open(os.path.join(devblogpath, bibname+".html"), 'w') as fp:
            thedate = time.strftime("%Y-%m-%d", time.localtime())
            fp.write("\n".join(["---", "title: {}".format(meta.setdefault("title", bibname)),
                                "layout: main",
                                "categories: bibs", "date: {}".format(thedate), "---"]))
            fp.write("\n"*5)
            fp.write("<blockquote><p>{}</p></blockquote>\n\n".format(meta.setdefault("desc", "A Bibliography")))
            fp.write(content)
            fp.write("\n\n")
            fp.write(js)
