Timatic Scraper
===============

TimaticScraper.py


First, change the folder path to where you want the files to be saved!

Timatic contains roughly 50,000 combinations of national and destination, and is
probably the most comprehensive Visa requirement database online.

This script simply download all country code combinations available on Timatic server.
The files will be saved as HTML and needs further processing.

Since this script does http requests repeatedly it is possible for Timatic to block your IP.

To resolve this, use Tor and set up Socks proxy server locally, then uncomment two lines
at the beginning of the script.


For convenience, a cache of Timatic files is included (Timatic Files.zip)



TimaticToSQLite.py

Simply get text from html files and put into SQLite data base for much faster access

For convenience, a Timatic DB is included (Timatic.db)



TimaticParser.py

Attempt to parse Timatic texts to get simple Yes/No visa requirement
