from HTMLParser import HTMLParser
from urllib2 import urlopen
from urllib import urlencode
import re, csv

class FlipSeekPubs(HTMLParser):
	
	def __init__(self):
		HTMLParser.__init__(self)
		self.flipSeekURL = 'http://www.flipseekpubs.com/publication/?i='
		self.getTitle = False
		self.countTitle = 0
		self.counter = 1
		
	def handle_starttag(self, tag, attrs):
		if tag == 'title':
			self.countTitle += 1
			if self.countTitle == 2:
				self.countTitle = 0
				self.getTitle = True
		
	def handle_data(self, data):
		if self.getTitle:
			print data.strip() + " (%s%s)" % (self.flipSeekURL,self.counter)
			
			new_file = open('FlipSeekPubsCrawledPublications.csv', 'a')
			csvWriter = csv.writer(new_file, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			csvWriter.writerow([data.strip(),"%s%s" % (self.flipSeekURL,self.counter)])
			new_file.close()
			 
			self.getTitle = False
		
	def run(self):
		while True:
			flipSeek = urlopen(self.flipSeekURL + "%s" % self.counter)
			
			data = flipSeek.read().decode('utf-8','replace')
			if not re.search('unavailable',data):
				self.feed(data)
				self.close()
			else:
				print "Unavailable: %s" % self.counter
			
			self.counter += 1	
			flipSeek.close()
		

if __name__ == '__main__':
	
	try:
	
		flipSeekPubs = FlipSeekPubs()
		flipSeekPubs.run()
	except KeyboardInterrupt:
		print "\nApplication Exits..."

			
	
	
