"""
Things Crawler needs to do:
0) Load words dictionary (pickled) into memory
1) Load URLS it has already visited into memory
2) Load "next" URL to visit
    - this can be either a parameter or loaded into memory from an
    external file which keeps track of the URLs queue
3) Execute GET, add URL to visited set
4) Parse response
5) Update words dictionary
6) If MAX_PAGES is met, enter quit phase
7) Quit phase should:
    - repickle words dictionary
    - write visited URLs to file
    - write "next" URLs queue to file
"""

import urllib2
import cPickle as pk
import urlparse
import os

class WordWrangler(object):
    def __init__(self, max_pages, init_url):
        self.max_pages = max_pages
        self.rootname = self._name_from_url(init_url)
        self.words = self._load_dictionary()
        self.old_urls = self._load_old_urls()
        self.next_urls = self._load_next(init_url)

    def _name_from_url(self, url):
        """
        Extracts name from a url in the format www.name.ext
        """
        netloc = urlparse.urlparse(url)[1]
        start = netloc.find('.') + 1
        end = netloc.find('.', start)
        return netloc[start:end]

    def _load_dictionary(self):
        """
        Checks if there is a pre-computed dictionary saved somewhere.
        If so, loads. Else, returns empty dict
        """
        datafile = self.rootname + ".words"
        if self._file_exists(self.rootname, datafile):
            return self._unpickle_data(self.rootname, datafile)
        else:
            self._make_dir()
            return {}

    def _load_old_urls(self):
        """
        Checks if there is a file containing previously visited
        urls. If so, loads. Else, returns an empty set
        """
        datafile = self.rootname + ".old"
        if self._file_exists(self.rootname, datafile):
            return self._unpickle_data(self.rootname, datafile)
        else:
            self._make_dir()
            return set([])

    def _load_next(self, init_url):
        """
        If init_url has already been visited, we want to
        continue where we left off. If it has not been visited,
        we want to start a search from this new url
        """
        datafile = self.rootname + ".old"
        if init_url in self.old_urls and \
           self._file_exists(self.rootname, datafile):
                return self._unpickle_data(self.rootname, datafile)
        else:
            return [init_url]

    def _file_exists(self, directory, filename):
        if os.path.exists(directory + "/" + filename):
            return True
        return False

    def _make_dir(self):
        if not os.path.exists(self.rootname):
            os.makedirs(self.rootname)

    def _unpickle_data(self, directory, filename):
        instream = open(directory + "/" + filename, 'rb')
        data = pk.load(instream)
        instream.close()
        return data

    def _pickle_data(self, data, directory, filename):
        outsteam = open(directory + "/" + filename, "wb")
        pk.dump(data, outstream)
        outstream.close()

    def save_progress(self):
        # pickle dictionary
        # pickle next_urls
        # pickle old_urls
        return None

    def begin_wrangling(self):
        """
        Has the crawler start issuing page requests in a BFS search
        through self.next_urls
        """
        visited = 0
        while visited < self.max_pages and len(self.next_urls) != 0:
            curr_url = self.next_urls.pop(0)
            htmlpage = self._make_url_request(curr_url)
            print htmlpage
            pagecontents = self._scrape_html(htmlpage)

    def _make_url_request(self, url):
        return urllib2.urlopen(url).read()

    def _scrape_html(self, page):
        """
        Scrapes an html page and returns a string containing
        all the words on the page. Any urls found during
        scraping will be added to self.next_urls
        """
        return ""

def main():
    ww = WordWrangler(5, "https://en.wikipedia.org/wiki/Bogosort")
    ww.begin_wrangling()
    ww.save_progress()

if __name__ == '__main__':
    main()
