#!/usr/bin/python3

import argparse
import sqlite3




def main(url, db):

	print()
	print('URL: ' + url)
	print(' DB: ' + str(db))

	conn = sqlite3.connect(db)
	conn.row_factory = sqlite3.Row

	ids = get_url_ids(conn, url)

	for moz_fk in ids:
		print()
		print_folder_paths(conn, moz_fk)

	return True



def print_folder_paths(conn, moz_fk, search_field='fk'):

	sql = "SELECT parent, title FROM moz_bookmarks WHERE " + search_field + "=:moz_fk"
	paramsDict = {'moz_fk': moz_fk}
	cursor = conn.execute(sql, paramsDict)

	for row in cursor:
		print(' Title: %s' % (row['title']), )
		if row['parent']!=0:
			print_folder_paths(conn, row['parent'], 'id')

	return True



def get_url_ids(conn, url):

	sql = "SELECT id FROM moz_places WHERE url=:url"
	paramsDict = {'url': url}
	cursor = conn.execute(sql, paramsDict)

	for row in cursor:
		yield row['id']



def get_ff_places():

	#TODO: Get this automatically!
	db = '/home/dotancohen/.mozilla/firefox/lixn8e40.default/places.sqlite'

	return db



if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('url')
	parser.add_argument('-db')
	args = parser.parse_args()

	if args.db==None:
		db = get_ff_places()
	else:
		db = args.db

	main(args.url, db)

"""
sqlite> .schema moz_bookmarks
CREATE TABLE moz_bookmarks (  id INTEGER PRIMARY KEY, type INTEGER, fk INTEGER DEFAULT NULL, parent INTEGER, position INTEGER, title LONGVARCHAR, keyword_id INTEGER, folder_type TEXT, dateAdded INTEGER, lastModified INTEGER, guid TEXT);
CREATE INDEX moz_bookmarks_itemindex ON moz_bookmarks (fk, type);
CREATE INDEX moz_bookmarks_parentindex ON moz_bookmarks (parent, position);
CREATE INDEX moz_bookmarks_itemlastmodifiedindex ON moz_bookmarks (fk, lastModified);
CREATE UNIQUE INDEX moz_bookmarks_guid_uniqueindex ON moz_bookmarks (guid);


sqlite> select * from moz_bookmarks where title like 'An Introduction to %' limit 3;
3059|1|3096|40|50|An Introduction to Machine Learning | Architects Zone|||1367507340000000|1367507340000000|n1YV3yO-xwIF
6333|1|5874|3687|84|An Introduction to Python Lists|||1355653279000000|1355653279000000|m1cGhEqRLikq
8801|1|7985|4227|10|An introduction to Linux kernel programming - Lesson 1: Building and running a new Linux kernel|||1425511157000000|1425511157000000|fB4r3iZU74Pg


sqlite> select * from moz_bookmarks where id=40;
40|2||34|3|toWork|||1362077299000000|1429013598812000|G5vgV5ibeAM-
sqlite> select * from moz_bookmarks where id=34;
34|2||2|25|Sync Folder|||1406725615000000|1436128018349000|0564jUUFZpcL
sqlite> select * from moz_bookmarks where id=2;
2|2||1|0|Bookmarks Menu|||1316762007000000|1439829612918000|menu________


sqlite> .schema moz_places
CREATE TABLE moz_places (   id INTEGER PRIMARY KEY, url LONGVARCHAR, title LONGVARCHAR, rev_host LONGVARCHAR, visit_count INTEGER DEFAULT 0, hidden INTEGER DEFAULT 0 NOT NULL, typed INTEGER DEFAULT 0 NOT NULL, favicon_id INTEGER, frecency INTEGER DEFAULT -1 NOT NULL, last_visit_date INTEGER , guid TEXT, foreign_count INTEGER DEFAULT 0 NOT NULL);
CREATE INDEX moz_places_faviconindex ON moz_places (favicon_id);
CREATE INDEX moz_places_hostindex ON moz_places (rev_host);
CREATE INDEX moz_places_visitcount ON moz_places (visit_count);
CREATE INDEX moz_places_frecencyindex ON moz_places (frecency);
CREATE INDEX moz_places_lastvisitdateindex ON moz_places (last_visit_date);
CREATE UNIQUE INDEX moz_places_url_uniqueindex ON moz_places (url);
CREATE UNIQUE INDEX moz_places_guid_uniqueindex ON moz_places (guid);


sqlite> select * from moz_places where id=3096;
3096|http://architects.dzone.com/articles/introduction-machine-learning||moc.enozd.stcetihcra.|0|0|0||47||jFNGSZ35razz|1
"""

