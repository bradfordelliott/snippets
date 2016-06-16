
db:
	rm -f dbs/snippets.db
	sqlite3 dbs/snippets.db < dbs/db.sql
