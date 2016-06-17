-- This is the overall snippet manager table
CREATE TABLE snippets
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cdate TEXT,
    ctime TEXT,
    language TEXT,
    label TEXT,
    author INTEGER,
    description TEXT,
    status TEXT
);

CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- This table is used to track revisions of a given document
CREATE TABLE revisions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sid INTEGER,
    cdate TEXT,
    ctime TEXT,
    data TEXT
);

-- Used to manage tags associated with a given document
CREATE TABLE tags
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sid INTEGER,
    data TEXT
);

INSERT INTO users (name) VALUES('guest');
INSERT INTO users (name) VALUES('belliott');
INSERT INTO users (name) VALUES('dlinnington');

INSERT INTO snippets (cdate, ctime, language, label, author, description) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'c',        'test_c',        1, 'A test snippet');
INSERT INTO snippets (cdate, ctime, language, label, author, description) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'python',   'test_python',   1, 'Another test snippet');
INSERT INTO snippets (cdate, ctime, language, label, author, description) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'shorte',   'test_shorte',   1, 'Type $ followed by <ctrl+space> to activate autocompletion');
INSERT INTO snippets (cdate, ctime, language, label, author, description) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'markdown', 'test_markdown', 1, 'A markdown snippet');
INSERT INTO snippets (cdate, ctime, language, label, author, description) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'dotreg',   'test_dotreg',   1, 'Type $ followed by <ctrl+space> to activate autocompletion');
INSERT INTO snippets (cdate, ctime, language, label, author, description) VALUES(date('now', 'localtime'), time('now', 'localtime'), 'makefile', 'test_makefile', 1, 'A makefile example');

INSERT INTO revisions (sid, cdate, ctime, data) VALUES(1, date('now', 'localtime'), time('now', 'localtime'), '
int main(int argc, char* argv[])
{
    printf("Hello world!\n");
}');

INSERT INTO revisions (sid, cdate, ctime, data) VALUES(2, date('now', 'localtime'), time('now', 'localtime'), '
print "Hello world!"
');

INSERT INTO revisions (sid, cdate, ctime, data) VALUES(3, date('now', 'localtime'), time('now', 'localtime'), '
@doc.title Hello World
@doc.subtitle My Document
@doc.body
@h1 Hello world
');

INSERT INTO revisions (sid, cdate, ctime, data) VALUES(4, date('now', 'localtime'), time('now', 'localtime'), '
Markdown
========

A second heading
----------------
');


INSERT INTO revisions (sid, cdate, ctime, data) VALUES(5, date('now', 'localtime'), time('now', 'localtime'), '
###################
addressWidth 8
dataWidth 16
prefix CAUI_TX
referencePrefix PAM
###################

register TX_MAIN_CONTROL 8''h0
attr no_check_type
registerComment
This is TBD
endComment
endRegister
');


INSERT INTO revisions (sid, cdate, ctime, data) VALUES(6, date('now', 'localtime'), time('now', 'localtime'), '
all:
	echo "Hello world!"
');
