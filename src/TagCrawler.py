# coding=utf-8
# encoding: utf-8
__author__ = 'pok'
import urllib
import urllib2


class Crawler:
    """
        Tool class for fetching pages from http://www.yidianzixun.com/*
    """

    def __init__(self):
        header = [('Host', 'www.yidianzixun.com'),
                  ('Referer', 'http://www.yidianzixun.com/'),
                  ('User-Agent',
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36'),
                  ('Cookie',
                   'uid=-1277158634; JSESSIONID=WE1QHX4tFo2WR88-n_GdMQ; userid=8636144; guest=true; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1411277158,1411277383,1411277410,1411277424; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1411277424; order=')
        ]
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        opener.addheaders = header
        urllib2.install_opener(opener)


    def fetch(self, url):
        try:
            return urllib2.urlopen(url).read()
        except Exception, e:
            print e
            return None


def collectRoot():
    """
        This function mainly collect the root tags from http://www.yidianzixun.com/
            Return:
                the list of the root tags
    """

    return ['数码控', 'IT民工', '财经迷', '创业者', '美食控', '养生控', '时尚达人', '旅行爱好者', '军事爱好者', '电影迷', '体育迷', '情感专家']


def collectTag(tag):
    """
    This function mainly collects the sub-tag of the root tags in http://www.yidianzixun.com/.
       Param:
            tag is the root tag of http://www.yidianzixun.com/
            such like 数码控, IT民工 and so on.
         Return:
            the list of the sub-tags
    """

    data = '{"gender":-1,"roles":["' + tag + '"],"ans":[]}'
    url = 'http://www.yidianzixun.com/api/q/?path=home|channel-qa&data='
    data = urllib.quote(data)
    url += data
    c = Crawler()
    content = c.fetch(url)
    print content


def test():
    root = collectRoot()
    for t in root:
        collectTag(t)


if __name__ == '__main__':
    test()