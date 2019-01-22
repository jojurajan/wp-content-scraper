wp-content-scraper
==================

This script can be used to generate urls of images stored within the `wp-content/uploads/` of a WordPress server. This script uses **Python2.7** and it would be a good practice to use a virtualenv for this scraper.

###How to use the script

Install the required python libraries using the following command
```
pip install -r requirements.txt
```
As the libraries are getting installed,
```
Add the wp-content urls to be scraped into the test.txt file. (Sample urls are already present in the file. Remove them and add your urls.)
```
To run the script,
```
python scrape.py
```

###Output

The image links will be stored in files with the name `<site_name>_links.txt`.

You can now use your favourite Download manager to import the text files and download those images to your system.

P.S: ***This only works for Apache based WordPress sites.***
