#!/usr/bin/python

import feedparser
import wget
import feedparser
import sqlite3
import time

RssUrlList = ['http://postitforward.tumblr.com/rss','http://for-war3-blog-blog.tumblr.com/rss']

sleep=3600/len(RssUrlList)

def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)

conn = sqlite3.connect('tumblr.db')

def DownloadVideo(rss_url):
    feeds = feedparser.parse(rss_url) 
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
        thisposttime=float(time.mktime(time.strptime(post.published[:-6],"%a, %d %b %Y %H:%M:%S")))
        if conn.execute("SELECT MAX(DATE) FROM %s"%table).next()[0] == thisposttime: 
            break
        if post.description.find("video_file") == -1:
            continue
        sourceadd= post.description.find("source src=")
        tumblradd= post.description[sourceadd:].find("tumblr_")
        typeadd = post.description[sourceadd:][tumblradd:].find("type=\"video")
        video_id=post.description[sourceadd:][tumblradd:][:typeadd-2]
        if video_id.find("/") !=-1:
            video_id=video_id[:video_id.find("/")]
        try:
            list(conn.execute("SELECT * FROM %s WHERE ADDRESS == '%s'"%(table,video_id)).next())
        except:
            print(post.title + ": " + post.link + post.published+"\n")
            wget.download("http://vt.tumblr.com/"+video_id+".mp4",rss_url[7:-4])
            print("\n")
            conn.execute("INSERT INTO %s (BLOG ,ADDRESS, DATE) VALUES ('%s','%s','%f')" % (table,rss_url,video_id,time.mktime(time.strptime(post.published[:-6],"%a, %d %b %Y %H:%M:%S"))))
            #wget.download(get_download_url("https://your.appspot.com/fetch.php?url="+post.link),rss_url[7:-4])
            conn.commit()
while(1):
    for rss_url in RssUrlList:
        print("Downloading "+rss_url)
        DownloadVideo(rss_url)
    print("Sleep "+str(sleep)+" seconds")
    time.sleep(sleep)
