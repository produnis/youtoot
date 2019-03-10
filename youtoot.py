#!/usr/bin/env python3
#............................
import os.path
import sys
import feedparser
from mastodon import Mastodon 
import json
import requests
import re
import sqlite3
from datetime import datetime, date, time, timedelta

if len(sys.argv) < 4:
    print("Usage: python3 youtoot.py youtube_channel_id mastodon_login mastodon_passwd mastodon_instance")
    sys.exit(1)

# sqlite db to store processed tweets (and corresponding toots ids)
sql = sqlite3.connect('youtoot.db')
db = sql.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS tweets (tweet text, toot text, youtube text, mastodon text, instance text)''')

if len(sys.argv)>4:
	instance = sys.argv[4]
else:
	instance = 'botsin.space'

if len(sys.argv)>5:
    days = int(sys.argv[5])
else:
    days = 1

youtube = sys.argv[1]
mastodon = sys.argv[2]
passwd = sys.argv[3]

mastodon_api = None

d = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id='+youtube)

for t in reversed(d.entries):
	# check if this tweet has been processed
	db.execute('SELECT * FROM tweets WHERE tweet = ? AND youtube = ?  and mastodon = ? and instance = ?',(t.id, youtube, mastodon, instance))
	last = db.fetchone()
	
	# process only unprocessed tweets less than 1 day old
	if last is None:
		if mastodon_api is None:
			# Create application if it does not exist
			if not os.path.isfile(instance+'.secret'):
				if Mastodon.create_app(
					'tootbot',
					api_base_url='https://'+instance,
					to_file = instance+'.secret'
				):
					print('tootbot app created on instance '+instance)
				else:
					print('failed to create app on instance '+instance)
					sys.exit(1)

			try:
				mastodon_api = Mastodon(
					client_id=instance+'.secret',
					api_base_url='https://'+instance
				)
				mastodon_api.log_in(
					username=mastodon,
					password=passwd,
					scopes=['read', 'write'],
					to_file=mastodon+".secret"
				)
			except:
				print("ERROR: First Login Failed!")
				sys.exit(1)

		#print(t.id+" "+t.link+" "+t.summary+" %s" % len(t.summary))
		textmessage = t.summary
		if (len(t.summary) > 350):
			textmessage = t.summary[0:350]
		tootmessage = "%s\n%s" % (t.link,textmessage)
		print(tootmessage)
		toot = mastodon_api.status_post(status=tootmessage, in_reply_to_id=None, sensitive=False, visibility='public', spoiler_text=None)
		if "id" in toot:
			db.execute("INSERT INTO tweets VALUES ( ? , ? , ? , ? , ? )",
			(t.id, toot["id"], youtube, mastodon, instance))
			sql.commit()
