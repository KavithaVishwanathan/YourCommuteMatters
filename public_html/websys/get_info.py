import json
import sys
import urllib2
import feedparser
#import csv 

#from HTMLParser import HTMLParser
#from htmlentitydefs import name2codepoint

#class MyHTMLParser(HTMLParser):
#    def handle_starttag(self, tag, attrs):
#        if tag == 'table':
#            #self.IsTable = True
#            print 'Is a Table!!!'
#        else:
#            print "Start tag:", tag
#        for attr in attrs:
#            print "     attr:", attr
#    def handle_endtag(self, tag):
#        if tag == 'table':
#            self.IsTable = False
#            print 'Table Ends'
#        else:
#            print "End tag  :", tag
#    def handle_data(self, data):
#        print "Data     :", data
#    def handle_comment(self, data):
#        print "Comment  :", data
#    def handle_entityref(self, name):
#        c = name #unichr(name2codepoint[name])
#        print "Named ent:", c
#    def handle_charref(self, name):
#        if name.startswith('x'):
#            c = unichr(int(name[1:], 16))
#        else:
#            c = unichr(int(name))
#        print "Num ent  :", c
#    def handle_decl(self, data):
#        print "Decl     :", data

#parser = MyHTMLParser()

def main(Service,Type,Data):
    count = 0
    if Service == 'LIRR':
        urlData = "https://traintime.lirr.org/api/Departure?api_key=%3CYOUR_KEY%3E&loc=NYK" #% (key,busNo)
        webUrl = urllib2.urlopen(urlData)
        data = webUrl.read()
        jsonData = json.loads(data)
        TrainsData = jsonData["TRAINS"]
        for train in TrainsData:
            stops = train["STOPS"]
            train_id = train["TRAIN_ID"]
            track = train["TRACK"]
            timedep = train["ETA"]
            if Type == "1":
                if Data in stops:
                    if track != "":
                        count += 1
                        print "Train ",train_id," is in track ",track,", stops in ",Data," and departs at: ",timedep
                    else:
                        count += 1
                        print "Train ",train_id,", stops in ",Data," departing at: ",timedep,", but there is no track yet"
            elif Type == "2":
                if Data == train_id:
                    if track != "":
                        count += 1
                        print "Train ",train_id," is in track ",track," and departs at: ",timedep
                    else:
                        count += 1
                        print "Train ",train_id," departs at: ",timedep,", but there is not track yet"
        if count == 0:
            print "There is no information available yet"
#            print "Track: ",train["TRACK"]," for Train No ",train["TRAIN_ID"]
    #elif Service == 'NJT':
        #urlData = "https://www.njtransit.com/rss/RailAdvisories_feed.xml"
        #urlData = "http://198.177.2.186:8088/CooCooWeb.aspx?sid=NY"
        #urlData = "http://dv.njtransit.com/mobile/tid-mobile.aspx?sid=NY"
        #webUrl = urllib2.urlopen(urlData)
        #data = webUrl.read()
        #parser = HTMLParser()
        #parser.feed(data)
        #print data
        #feed = feedparser.parse( urlData )
        #print feed
        #print parser.


if __name__ == "__main__":
    main(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]))   