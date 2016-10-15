# WikiCrawler
A bot that crawls thru some of Wikipedia pages and records words and their frequencies.

## Dependencies
Requires the lxml and bs4 libraries. It should work if you simple execute the install script, alternatively install each library via command line

## Usage
Feed an int into the first parameter of WordWrangler indicating the number of pages to comb through and a string into the second parameter telling the bot where to begin searching. From then on it will operate a BFS search through the links it encounters, taking care to not revisit the same link twice.

## Notes
This bot should only be used with Wikipedia, the reason being that it looks for div tags with class=mw-body-content to get its content. Also,  there are some Wikipedia specific link semantics in get_links. Although these can hypothetically be changed to match other sites. Also, cannot guarantee this bot stays on English only pages -- will have to do further link processing to ensure English only.
