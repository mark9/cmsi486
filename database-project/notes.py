import bottle
import MySQLdb
import cgi
import re

# This route is the main page of the database
# fetches the first 5 rows 
@bottle.route('/')
@bottle.get("/notes")
@bottle.get("/notes/")
@bottle.route('/notesmain')
def notes_index():
    results = sql_noparam("select * from notes order by _id desc limit 5")
    l = format_notes(results)
    return bottle.template("template_notes_main", dict(notes=l), errors="")

# This page fetches all the rows of the notes table
@bottle.route('/notesall')
def notes_all():
    results = sql_noparam("select * from notes order by _id desc")
    l = format_notes(results)
    return bottle.template("template_notes_all", dict(notes=l), errors="")

@bottle.get('/newnote')
def get_newnote():
    return bottle.template("template_notes_new", dict(body = "", errors="", tag=""))

@bottle.post('/newnote')
def post_newnote():
    text = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")
    #text = cgi.escape(text)
    #tags = cgi.escape(tags, quote=True)
    #tags = cgi.escape(tags)
    if text == "":
        errors = "note must contain text"
        return bottle.template("template_notes_new", dict(body=text, tags=tags, errors=errors))
    else:
        # insert note
        note_id = insert_note(text)
        
        # insert the tags
        insert_tags(note_id, tags)
        
        bottle.redirect("/notesmain")

def insert_note(text):
        cur=db.cursor()
        sql_param("insert into notes (text) values (%s)", text)
        # use last_insert_id() to get the id of this note
        results = sql_noparam("select last_insert_id()")
        return str(results[0][0])

def insert_tags(note_id, tags):
    array = array_tags(tags)
    for tag in array:
        if tag != "":
            # if the tag is not in the table already, add it
            if count_tags(tag) == 0:
                insert_tag(tag)
            # now it should be in there for sure.
            
            # lastly, insert the relation in the note_tag table
            tag_id = get_tagid(tag)
            insert_notetag(note_id, tag_id)

# turns a string of comma separated tags into an array of tags
def array_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("",str(tags))
    tags_array = nowhite.split(',')
    new = []
    for tag in tags_array:
        if tag not in new and tag != "":
            new.append(tag)
    return new

# checks if a tag already exists by counting the number of appearances
def count_tags(tag):
    results=sql_param("select count(*) from tags where tag=%s", tag)
    if results[0][0] == 1:
       return 1
    return 0

def insert_tag(tag):
    sql_param("insert into tags (tag) values (%s)", tag)

def insert_notetag(note_id, tag_id):
    sql="insert into note_tag (_id_note, _id_tag) values ("+note_id+', '+tag_id+')'
    sql_noparam(sql)

@bottle.get("/notes/note_not_found")
def note_not_found():
    return "Sorry, note not found"

# Displays a particular note
@bottle.get("/notes/<id>")
def show_note(id="notfound"):
    id = cgi.escape(id)
    results = sql_param("select count(*) from notes n where n._id=%s", id)
    
    # if note id doesn't exist, redirect
    if results[0][0] == 0:
        print results[0][0]
        bottle.redirect("/notes/note_not_found")
        
    else:
        # get note information
        results = sql_param("select * from notes n where n._id=%s", id)
        note = format_note(results)
        return bottle.template("template_notes_key", id=note[0], text=note[1], creation_date=note[2], tags=read_tags(note[0]), errors="")

@bottle.post('/tags/new')
def add_newtag():
    tags = bottle.request.forms.get("tags")
    note_id = bottle.request.forms.get("id")
    insert_tags(tags, note_id)

@bottle.get('/tags/<tag>')
def show_notes_by_tag(tag="notfound"):
    tag = cgi.escape(tag)
    results = sql_param("select count(*) from tags t where t.tag=%s", tag)
    
    # if tag id doesn't exist, redirect
    if results[0][0] == 0:
        print results[0][0]
        bottle.redirect("/tag/tag_not_found")
        
    else:
        # get note information
        results = sql_param("select * from notes n join note_tag nt on nt._id_note=n._id join tags t on t._id=nt._id_tag where t.tag=%s order by n._id desc", tag)
        l = format_notes(results)
        return bottle.template("template_tags_tag", dict(notes=l), title=tag, errors="")

#
# HELPER FUNCTIONS
#


def format_note(results):
    return ( results[0][0], results[0][1], fixup_date(results[0][2]) )

# returns notes in list format, for use on html page
# used by: home page queries, retreiving notes by tag, search query results
def format_notes(results):
    l = []
    for row in results:
        num = row[0]
        date = fixup_date(row[2])
        tags=read_tags(num)
        l.append({'id':num, 'text':row[1], 'tags':tags, 'creation_date':date})
    return l

def get_tagid(tag):
    results=sql_param("select _id from tags where tag=%s", tag)
    return str(results[0][0]) 

#given the id number of a note, this function returns a list of all the tags
def read_tags(id):
    results = sql_param("select t.tag from tags t join note_tag nt on t._id=nt._id_tag where nt._id_note=%s", id)
    return format_tags(results)
	
# given id, perform join to get tags
def format_tags(results):
    l = []
    for row in results:
        l.append(row[0])
    return l
	
# executes an sql query that DOES need a parameter inputted
def sql_param(sql, param):
	cur = db.cursor()
	cur.execute(sql, param)
	results = cur.fetchall()
	db.commit()
	return results

# executes an sql query that DOES NOT need a parameter inputted
def sql_noparam(sql):
	cur = db.cursor()
	cur.execute(sql)
	results = cur.fetchall()
	db.commit()
	return results

def fixup_date(date):
    formatted = date.strftime("%A, %B %d %Y at %I:%M%p") # fix up date
    return formatted



db=MySQLdb.connect(host="mysql4.cs.lmu.edu",port=3306,user="mlawranc",passwd="keck",db="mlawranc")
#db=MySQLdb.connect(read_default_file='./config_file.mysql')
#db=MySQLdb.connect(read_default_file='~/my.cnf')
cur=db.cursor()

bottle.debug(True)
# Start the webserver running and wait for requests
bottle.run(host='localhost', port=8082)