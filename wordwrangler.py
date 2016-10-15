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

NOTES
pip install lxml
pip install requests
pip install bs4
For use with wikipedia only
"""

import urllib2
import cPickle as pk
import urlparse
from lxml import html
from bs4 import BeautifulSoup
import re
import os

class WordWrangler(object):
    def __init__(self, max_pages, init_url):
        self.max_pages = max_pages
        self.rootname = self._name_from_url(init_url)
        self.init_url = init_url

        self.words = self._load_dictionary()
        self.old_urls = self._load_old_urls()
        self.next_urls = self._load_next(init_url)

    def _name_from_url(self, url):
        """
        Extracts name from a url in the format www.name.ext
        """
        netloc = self._get_url_netloc(url)
        start = netloc.find('.') + 1
        end = netloc.find('.', start)
        return netloc[start:end]

    def _get_url_netloc(self, url):
        return urlparse.urlparse(url)[1]

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
            self.old_urls.add(curr_url)

            htmlpage = self._make_url_request(curr_url)
            if htmlpage == "":
                continue

            pagecontents, pagelinks = self._scrape_html(htmlpage)
            self._add_links_to_next(pagelinks)
            self._add_content_to_words(pagecontents)
            visited += 1

    def _make_url_request(self, url):
        try:
            response = urllib2.urlopen(url)
        except ValueError:
            return ""
        return response.read()

    def _scrape_html(self, page):
        """
        Scrapes an html page and returns a string containing
        all the words on the page and a list of any urls found
        """
        raw_text = self._get_html_text(page)
        clean_text = self._clean_text(raw_text)

        links = self._get_links(page)
        return clean_text, links

    def _get_html_text(self, page):
        soup =  BeautifulSoup(page, "lxml")
        words = soup.find_all("div", class_="mw-body-content")
        return words[0].get_text()

    def _clean_text(self, raw_text):
        """
        Removes oddball characters such as brackets, periods, empty
        spaces, etc.
        """
        return ' '.join(re.findall(r"[\w']+", raw_text))

    def _get_links(self, page):
        """
        Finds all the links on the html page by finding the
        href instances
        """
        links = []
        netloc = self._get_url_netloc(self.init_url)
        for l in html.fromstring(page).xpath('//a/@href'):
            if l.startswith("http"):
                links.append(l)
            elif l.startswith("/wiki"):
                links.append("http://" + netloc + l)
        return links

    def _add_links_to_next(self, links):
        """
        Adds a list of links to the set of next_urls
        """
        links = list(set(links) - self.old_urls)
        self.next_urls.extend(links)

    def _add_content_to_words(self, pagecontents):
        """
        Takes a space delimited string of the words on the page
        and adds them to the words dictionary
        """
        for word in pagecontents.split():
            if not word.isdigit():
                self.words[word] = self.words.get(word, 0) + 1

def main():
    ww = WordWrangler(5, "https://en.wikipedia.org/wiki/Bogosort")
    ww.begin_wrangling()
    ww.save_progress()

if __name__ == '__main__':
    main()
