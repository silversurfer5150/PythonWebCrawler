#**********************************************************#
#-------------A Web Crawler written in Python -------------#
#-------------For Fun !    --------------------------------#
#-------------Author: Will Edwards ------------------------#
#-------------Version 1.0, August 2016        -------------#
#-------------^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^-------------#
#----------------------------------------------------------#

#**********************************************************#

# Beautiful Soup library is used to parse the html , urllib2 is used to request the HTML
from bs4 import BeautifulSoup

#Other dependencies
import urllib2
import json
import datetime
import time
from time import strftime
import logging
import SimpleHTTPServer
import SocketServer
"""
For documentation of the webbrowser module,
see http://docs.python.org/library/webbrowser.html
"""
import webbrowser

class pythonWebCrawler():
    def __init__(self):
        logger = logging.getLogger('pythonWebCrawler')
        hdlr = logging.FileHandler('pythonWebCrawler.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr) 
        logger.setLevel(logging.DEBUG)

        # get today's date in different formats for operations later in service
        todaysDate = (strftime("%Y-%m-%d"))

        logger.info('Service Starting...Crawling the Web \n')
        # Log run date and expiry date
        logger.info("Running on : " + todaysDate  + '\n')

        url = 'https://en.wikipedia.org/wiki/Fire'
        logger.info('Crawling %s \n', url)

        # This condition returns an error if the url request is unsuccessful
        try:
            # Pull in data
            data = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print ('Cannot open url...\n')
            logger.error('Cannot open url...\n\n\n')
        # array to be used as read buffer
        l = []
        # string for all page data
        s = ''
        # Read from buffer and join array into string
        for line in data.readlines():
            l.append(line)
        s = '\n'.join(l)

        # convert string into HTML object for parsing
        soup = BeautifulSoup(s, 'html.parser')

        #create new node ready for crawled content
        newNode = soup.new_tag("div")
        heading = soup.find('h1')
        newNode.append(soup.new_tag("br"))
        #add crawled heading
        newNode.append(heading)
        paragraph = soup.find('p')
        newNode.append(soup.new_tag("br"))
        #add crawled paragraph
        newNode.append(paragraph)

        for img in soup.find_all('img'):
            #add crawled images
            newNode.append(img)
            newNode.append(soup.new_tag("br"))

        self.outputToFile(newNode)

    #Python implicitly passes the object to method calls, but you need to explicitly declare the parameter (self) for it.
    def outputToFile(self,newNode):
        print 'Outputting to file'
        # load the file
        with open('output.html') as output:
            s = output.read() 
            outputSoup = BeautifulSoup(s, 'html.parser')
            targetTag = outputSoup.find('div', { 'id' : 'newContent' })
            #remove all existing HTML content from target tag to indicate new crawled content
            for child in targetTag.children:
                child.replaceWith('')

            #add new content to existing target tag
            targetTag.append(newNode)

        # save the file again
        with open('output.html', 'w') as outf:
            outf.write(str(outputSoup))
        self.serveContent()

    def serveContent(self):

        url = 'http://localhost:8000/output.html'

        # Open URL in new window, raising the window if possible.
        webbrowser.open_new(url)
#Initilize instance of Crawler            
crawler = pythonWebCrawler()
