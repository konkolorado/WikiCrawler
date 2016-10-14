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
from urlparse import urlparse

class WordWrangler(object):
    def __init__(self, max_pages, init_url):
        self.rootname = self._name_from_url(init_url)
        self.words = self._load_dictionary()
        self.old_urls = self._load_old_urls()
        self.next_urls = self._load_next(init_url)

    def _name_from_url(self, url):
        """
        Extracts name from a url in the format www.name.ext
        """
        netloc = urlparse(url)[1]
        start = netloc.find('.') + 1
        end = netloc.find('.', start)
        return netloc[start:end]

    def _load_dictionary(self):
        """
        Checks if there is a pre-computed dictionary saved somewhere.
        If so, loads. Else, returns empty dict
        """
        return {}

    def _load_old_urls(self):
        """
        Checks if there is a file containing previously visited
        urls. If so, loads. Else, returns an empty set
        """
        return set([])

    def _load_next(self, init_url):
        """
        If init_url has already been visited, we want to
        continue where we left off. If it has not been visited,
        we want to start a search from this new url
        """
        if init_url in self.old_urls:
            # Load next list
            pass
        else:
            return [init_url]

def main():
    ww = WordWrangler(5, "https://docs.python.org/2/library/")

if __name__ == '__main__':
    main()
