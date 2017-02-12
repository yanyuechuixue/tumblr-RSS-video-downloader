import feedparser
import wget
import urllib2
import feedparser

rss_url = 'http://sexy-a-g.tumblr.com/rss'
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




mkdir(rss_url[7:-4])
for post in feeds.entries:
    print(post.title + ": " + post.link)
    wget.download(get_download_url("https://wordpressbak-1094.appspot.com/fetch.php?url="+post.link),rss_url[7:-4])


