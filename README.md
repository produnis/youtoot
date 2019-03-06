# YouToot

A small python 3.x script to post youtube-videos on a mastodon account. 
It is based on https://github.com/cquest/tootbot by Christian Quest

The script only need mastodon login/pass to post toots.

It gets the videos from RSS available at https://www.youtube.com/feeds/videos.xml?channel_id=

A sqlite database is used to keep track of tweets than have been tooted.

The script is simply called by a cron job and can run on any server (does not have to be on the mastodon instance server).

## Setup

```
# clone this repo
git clone https://github.com/produnis/youtoot.git
cd youtoot

# install required python modules
pip3 install -r requirements.txt
```

## Useage

`python3 youtoot.py <youtube_chanel_id> <mastodon_account> <mastodon_password> <mastodon_domain>`

Example:

`python3 youtoot.py UCT0hbLDa-unWsnZ6Rjzkfug foobar@botsin.space **password** botsin.space`

It's up to you to add this in your crontab :)
