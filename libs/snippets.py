
from twisted.web.resource import Resource
import sqlite3
import string
import cgi
import sys

from libs.templates import template_html

class snippets(Resource):
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)

        self.m_conn = sqlite3.connect("./dbs/snippets.db")
        self.m_cursor = self.m_conn.cursor()

        self.m_users = {}
        self.load_users()

    def load_users(self):
        self.m_cursor.execute("SELECT id, name FROM users")
        for row in self.m_cursor:
            id = row[0]
            name = row[1]

            self.m_users[id] = name


    #def get_tags_list(self):
    #    self.m_cursor.execute("SELECT DISTINCT(category) FROM expenses ORDER BY category asc")

    def get_snippets(self):
        snippets = []

        self.m_cursor.execute("SELECT id, cdate, ctime, language, label, author, description FROM snippets ORDER BY id DESC")
        for row in self.m_cursor:
            snippet = {"id"   : row[0],
                       "date" : row[1],
                       "time" : row[2],
                       "language" : row[3],
                       "label" : row[4],
                       "author" : row[5],
                       "description" : row[6]}

            snippets.append(snippet)

        return snippets

    def get_snippet(self, id, revid):
        self.m_cursor.execute("SELECT cdate, ctime, language, label, author, description FROM snippets WHERE id=? ORDER BY id DESC", (id))
        snippet = None

        for row in self.m_cursor:
            snippet = {"date"     : row[0],
                       "time"     : row[1],
                       "language" : row[2],
                       "label"    : row[3],
                       "author"   : row[4],
                       "description" : row[5]}
        
        snippet["data"] = ""

        if(revid != None):
            self.m_cursor.execute("SELECT data FROM revisions WHERE sid=? and id=?", (id, revid))
        else:
            self.m_cursor.execute("SELECT data FROM revisions WHERE sid=? ORDER by id DESC LIMIT 1", (id))

        for row in self.m_cursor:
            snippet["data"] = row[0]

        return snippet

    def get_revisions(self, id):
        self.m_cursor.execute("SELECT id FROM revisions WHERE sid=?", (id))

        json_data = []
        for row in self.m_cursor:
            revid = row[0]
            json_data.append("'%s':'%s'" % (revid,revid))

        json_data = ','.join(json_data)

        return json_data


    def render_summary(self, request):
        styles = """
div.row
{
    clear:both;border-bottom:1px solid #ccc;background-color:#ffffff;height:25px;width:100%;'
}
div.row_odd
{
    clear:both;border-bottom:1px solid #ccc;background-color:#f7f7f7;height:25px;width:100%;'
}
div.row:hover,
div.row_odd:hover
{
    background-color:#e0e0e0;
}
"""
        script = ''
        
        body = """<h1>Snippets</h1>
<input type='button' onclick='return snippet_add();' value='Add'/>
<br/>
<div style='float:left;padding:20px;width:90%;'>
<div style='clear:both;border-bottom:1px solid #ccc;background-color:#f0f0f0;height:25px;width:100%;'>
  <div style="float:left;font-weight:bold;width:5%;min-width:5%;">ID</div>
  <div style="float:left;font-weight:bold;width:10%;min-width:10%;">Author</div>
  <div style="float:left;font-weight:bold;width:20%;min-width:20%;">Label</div>
  <div style="float:left;font-weight:bold;width:20%;min-width:20%;">Date</div>
  <div style="float:left;font-weight:bold;width:20%;min-width:20%;">Time</div>
  <div style="float:left;font-weight:bold;width:20%;min-width:20%;">Language</div>
</div>
"""

        snippets = self.get_snippets()

        i = 0
        for snippet in snippets:
            id = snippet["id"]
            cdate = snippet["date"]
            ctime = snippet["time"]
            language = snippet["language"]
            label = snippet["label"]
            if(snippet.has_key("author") and snippet["author"] != None):
                author = self.m_users[snippet["author"]]
            else:
                author = "&nbsp;"

            #data     = snippet["data"]

            cls = "row"
            if(i & 1):
                cls = "row_odd"
            i += 1
            body += string.Template("""
<div class='$class' onclick='snippet_open(${id})'>
  <div style="float:left;width:5%;min-width:5%;">${id}</div>
  <div style="float:left;width:10%;min-width:10%;">${author}</div>
  <div style="float:left;width:20%;min-width:20%;">${label}</div>
  <div style="float:left;width:20%;min-width:20%;">${date}</div>
  <div style="float:left;width:20%;min-width:20%;">${time}</div>
  <div style="float:left;width:20%;min-width:20%;">${language}</div>
</div>
""").substitute({"id" : id, "label" : label, "class" : cls, "date" : cdate, "time" : ctime, "language" : language, "author" : author})

        json_categories = '';

        script = """
$(document).ready(function() {
     $('.edit').editable('/snippets/update');
      });
$(document).ready(function() {
     $('.edit_items').editable('/snippets/update', {
        data : "{ %s }",
        type: 'select',
        submit : 'OK'
      })});
""" % json_categories

        html = template_html.substitute({
            "body" : body,
            "onload" : "",
            "version" : "0.1",
            "title"   : "Snippets",
            "styles"  : styles,
            "script"  : script
        }
        )

        return html


    def render(self, request):
        print request.uri

        if(request.uri.startswith("/snippets/add")):
            self.m_cursor.execute("INSERT INTO snippets (cdate, ctime, language, label) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'c', 'No Name')")
            self.m_conn.commit()
            id = self.m_cursor.lastrowid

            return "/snippets/edit?id=%d" % id

        elif(request.uri.startswith("/snippets/save")):
            print request.args
            id = cgi.escape(request.args["id"][0])
            data = cgi.escape(request.args["data"][0])
            print "Saving snippet %s" % id
            print "Data: %s" % data

            # First query the last revision and only save the
            # changes if there is a delta.

            self.m_cursor.execute("INSERT INTO revisions (sid, cdate, ctime, data) VALUES (?, date('now', 'localtime'), time('now', 'localtime'), ?)", (id, data))
            self.m_conn.commit()
            print "Saved data"

            return data

        elif(request.uri.startswith("/snippets/update")):
            print "In /snippets/update"
            print request.args
            id = cgi.escape(request.args["id"][0])
            value = cgi.escape(request.args["value"][0])
            parts = id.split("_")
            id = parts[1]
            field = parts[2]
            self.m_cursor.execute("UPDATE snippets SET %s=? WHERE ROWID=?" % field, (value, id))
            self.m_conn.commit()

            return value

        elif(request.uri.startswith("/snippets/edit")):
            id = cgi.escape(request.args["id"][0])
            revid = None
            if(request.args.has_key("revid")):
                revid = cgi.escape(request.args["revid"][0])

            snippet = self.get_snippet(id, revid)
            language = snippet["language"]
        
            languages = [
                {"name"    : "c",       "lexer" : "clike", "mime" : "x-c++src"},
                {"name"    : "css",     "mime" : "x-css"},
                {"name"    : "dotreg",  "mime" : "dotreg", "styles" : '''
.cm-s-default .cm-comment      {color: #009900;}
.cm-s-default .cm-comment-block{color: #a0a0a0;}
.cm-s-default .cm-comment-body {color: #00aa00;font-style:italic;margin-left:10px;}
.cm-s-default .cm-keyword      {color: #990033;}
.cm-s-default .cm-register     {color: #0000ff;font-weight:bold;}
.cm-s-default .cm-bitfield     {color: #cc00cc;font-weight:bold;}
'''},
                {"name"    : "makefile","mime" : "x-makefile"},
                {"name"    : "markdown","mime" : "x-markdown"},
                {"name"    : "python",  "mime" : "x-python"},
                {"name"    : "verilog", "mime" : "x-systemverilog"},
                {"name"    : "shorte",  "mime" : "shorte"},
                {"name"    : "sql",     "mime" : "x-sql"}
            ]

            json_languages = []
            for l in languages:
                if(l["name"] == language):
                    language = l
                json_languages.append("'%s' : '%s'" % (l["name"], l["name"]))
            json_languages = ",".join(json_languages)

            json_revisions = self.get_revisions(id)

            script = """
$(document).ready(function() {
     $('.edit').editable('/snippets/update');
      });

$(document).ready(function() {
     $('.edit_description').editable('/snippets/update', {
         type : 'textarea',
         submit : 'OK'
      })});

$(document).ready(function() {
     $('.edit_revisions').editable(function(value, settings) {
        window.location.href = "/snippets/edit?id=%s&revid=" + value
     }, {
        data : "{%s}",
        type: 'select',
        submit : 'OK'
      })});

$(document).ready(function() {
     $('.edit_languages').editable('/snippets/update', {
        data : "{%s}",
        type: 'select',
        submit : 'OK'
      })});

$(document).ready(function() {
     $('.edit_users').editable('/snippets/update', {
        data : "{'1' : 'guest', '2' : 'belliott', '3' : 'dlinnington'}",
        type: 'select',
        submit : 'OK'
      })});
""" % (id, json_revisions, json_languages)

            lexer = language['name']
            if(language.has_key("lexer")):
                lexer = language["lexer"]

            styles = ""
            if(language.has_key("styles")):
                styles = language["styles"]
            mime  = language['mime']

            author = ""
            if(snippet.has_key("author") and snippet["author"] != None):
                author = self.m_users[snippet["author"]]

            description = ""
            if(snippet["description"] != None):
                description = snippet["description"]

            body = string.Template("""
<style>
  div.field_label {float:left;margin-left:20px;font-weight:bold;padding-right:20px;}
</style>

<!-- This message is used to display a message when generating the document -->
<div id='loading' style='display:none;position:fixed;top:0;left:0;background:#c0c0c0;width:100%;height:100%;z-index:1000;'>
<div style='width:300px;height:200px;border:2px solid #aaa;border-radius:5px;background-color:white;text-align:center;position:absolute;left:50%;top:50%;margin-left:-150px;margin-top:-100px;'>
<b>Generating PDF ... please be patient ...</b>
</div>
</div>

<!-- A warning message used to display information to the user -->
<div id='warning' style='display:none;position:fixed;top:0;left:0;background:#c0c0c0;width:100%;height:100%;z-index:1000;'>
  <div style='width:500px;height:180px;border:2px solid #aaa;border-radius:5px;background-color:white;text-align:center;position:absolute;left:50%;top:50%;margin-left:-250px;margin-top:-90px;'>
    <div style='width:100%;height:24px;background-color:#ccc;border-bottom:1px solid #aaa;'><b>Warning:</b></div>
    <div id='warning_message' style='height:128px;margin-top:10px;'></div>
    <div style='height:27px;background-color:#ddd;'>
      <input type='button' style='margin-top:5px;' value='Close' onclick="$$('#warning').hide()"></input>
    </div>
  </div>
</div>

<div style='border-top:1px solid #ccc;background-color:#f7f7f7;padding:4px;margin:20px;margin-bottom:0px;'>
    <div class='field_label'>Name:</div><div style='float:left;' class='edit' id='snippet_${id}_label' name='snippet_${id}_label'>${label}</div>
    <div class='field_label'>Language:</div><div style='float:left;' class='edit_languages' id='snippet_${id}_language' name='snippet_${id}_language'>${language}</div>
    <div class='field_label'>Author:</div><div style='float:left;' class='edit_users' id='snippet_${id}_author' name='snippet_${id}_author'>${author}</div>
    <div class='field_label'>Revisions:</div><div style='float:left;' class='edit_revisions' id='snippet_${id}_revisions' name='snippet_${id}_revisions'>...</div>
    <div class='field_label' style='float:right;'><input type='button' onclick='return snippet_add();' value='Create'/></div>
    <div class='field_label' style='float:right;'><input type='button' onclick='return snippet_save(${id});' value='Save'/></div>
    <div class='field_label' style='float:right;'><input type="button" value="HTML" onclick='generate(editor, FORMAT_HTML, "${label}", "${language}");'/></div>
    <div class='field_label' style='float:right;'><input type="button" value="PDF" onclick='generate(editor, FORMAT_PDF, "${label}", "${language}");'/></div>
    <div style='clear:both;'></div>
</div>
<div style='border-top:1px solid #ccc;background-color:#fff;padding:10px;margin:20px;margin-top:0px;margin-bottom:0px;padding-left:20px;'>
    <div style='white-space:pre;' class='edit_description' id='snippet_${id}_description' name='snippet_${id}_description'>${description}</div>
</div>
<textarea id="snippet" name="snippet">${data}</textarea>

<script src="/codemirror/mode/${lexer}/${lexer}.js"></script>
<script>
function betterTab(cm) {
  if (cm.somethingSelected()) {
    cm.indentSelection("add");
  } else {
    cm.replaceSelection(cm.getOption("indentWithTabs")? "\t":
      Array(cm.getOption("indentUnit") + 1).join(" "), "end", "+input");
  }
}
var editor = CodeMirror.fromTextArea(document.getElementById("snippet"), {
   mode: "text/${mime}",
   lineNumbers: true,
   viewportMargin: Infinity,
   tabSize: 4,
   indentWithTabs: false,
   indentUnit: 4,
   extraKeys: {"Tab": betterTab, "Ctrl-Space" : "autocomplete"}
});

</script>
""").substitute({"id" : id, "data" : snippet["data"],
                 "lexer" : lexer, "mime" : mime, "label" : snippet["label"], "language" : snippet["language"],
                 "author" : author,
                 "description" : description})

            html = template_html.substitute({
                "body" : body,
                "onload" : "",
                "version" : "0.1",
                "title"   : "Snippet",
                "styles"  : styles,
                "script"  : script
                }
            )

            return html.encode('utf-8')

        
        html = self.render_summary(request)

        return html.encode('utf-8')
