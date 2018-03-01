#!/usr/bin/python3

"""
Locate in which Firefox Bookmarks directory is a particular URL.
"""

import argparse
import sqlite3



def main(url, db, record_type=None):

	try:
		conn = sqlite3.connect(db)
	except sqlite3.OperationalError as e:
		print("Unable to open database file.")
		return False

	conn.row_factory = sqlite3.Row

	if not url[0:4]=='http':
		print_folders_names_match(conn, url, record_type)
		return True

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
		if row['title']!='':
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



def print_folders_names_match(conn, needle, record_type=None):

	needle = '%'+needle+'%'
	sql = "SELECT parent, title FROM moz_bookmarks WHERE title LIKE :needle"

	if record_type=='bm':
		sql += " AND type=1"
	elif record_type=='dir':
		sql += " AND type=2"

	paramsDict = {'needle': needle}
	cursor = conn.execute(sql, paramsDict)

	for row in cursor:
		print('')
		print(' Title: %s' % (row['title']), )
		if row['parent']!=0:
			print_folder_paths(conn, row['parent'], 'id')

	return True



def get_ff_places():

	#TODO: Get this automatically!
	db = '/home/dotancohen/.mozilla/firefox/lixn8e40.default/places.sqlite'

	return db



if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('query', help="The query to search for. If a URL is provided then bookmarks to that exact URL will be returned.")
	parser.add_argument('-db', '--database', help="Specify which Firefox database to use.")
	parser.add_argument('-t', '--type', help="Specify 'bm' for bookmarks or 'dir' for directories.", choices=['bm', 'dir'])
	args = parser.parse_args()

	if args.database==None:
		database = get_ff_places()
	else:
		database = args.database

	if args.type in ['bm', 'dir']:
		record_type = args.type
	else:
		record_type = None

	main(args.query, database, record_type)

