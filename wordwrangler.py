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

class WordWrangler(object):
    def __init__(self, max_pages, init_url):
        print "Wrangler created"




def main():
    ww = WordWrangler(5, "www.wikipedia.org")

if __name__ == '__main__':
    main()
