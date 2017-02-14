#!/usr/bin/python

import feedparser
import wget
import urllib2
import feedparser
import sqlite3
import time
rss_url = 'http://abab.tumblr.com/rss'
feeds = feedparser.parse(rss_url)

def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
def get_download_url(url):
    response = urllib2.urlopen(url)
    dlurl = response.geturl()
    return dlurl

conn = sqlite3.connect('tumblr.db')

table=rss_url[7:-15].replace('-','')

try:
    conn.execute('''CREATE TABLE %s(BLOG TEXT, ADDRESS TEXT PRIMARY KEY, DATE REAL)'''% table)
    conn.execute("INSERT INTO %s (BLOG ,ADDRESS, DATE) VALUES ('%s','new','0')" % (table,rss_url))
#    conn.execute("SELECT * FROM TUMBLR WHERE BLOG == %s").next()
except:
    print("all ready exist.")
#    conn.execute('''CREATE TABLE(BLOG TEXT, ADDRESS TEXT PRIMARY KEY, DATE TEXT);''')
#    conn.execute("INSERT INTO %s (BLOG ,ADDRESS, DATE) VALUES ('rss_url','TEST','TEST')" % table)

mkdir(rss_url[7:-4])
for post in feeds.entries:
    print(post.title + ": " + post.link + post.published)
    thisposttime=float(time.mktime(time.strptime(post.published[:-6],"%a, %d %b %Y %H:%M:%S")))
    if conn.execute("SELECT MAX(DATE) FROM %s"%table).next()[0]>= thisposttime: 
        break
    try: 
        list(conn.execute("SELECT * FROM %s WHERE ADDRESS == '%s'"%(table,post.link)).next())
    except:
        wget.download(get_download_url("https://your.appspot.com/fetch.php?url="+post.link),rss_url[7:-4])
for post in feeds.entries:
    thisposttime=float(time.mktime(time.strptime(post.published[:-6],"%a, %d %b %Y %H:%M:%S")))
    if conn.execute("SELECT MAX(DATE) FROM %s"%table).next()[0]== thisposttime:
        break
    try:
        list(conn.execute("SELECT * FROM %s WHERE ADDRESS == '%s'"%(table,post.link)).next())
    except:
        conn.execute("INSERT INTO %s (BLOG ,ADDRESS, DATE) VALUES ('%s','%s','%f')" % (table,rss_url,post.link,time.mktime(time.strptime(post.published[:-6],"%a, %d %b %Y %H:%M:%S"))))
        conn.commit()

