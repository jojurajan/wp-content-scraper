import re
import urllib2
from BeautifulSoup import BeautifulSoup


class UrlOpener(object):

    def __init__(self, header_tuples=None):
        self.opener = urllib2.build_opener()
        # TODO: Create a randomization method for the user agent.
        if header_tuples is None:
            self.opener.addheaders = [('User-agent', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16')]
        else:
            self.opener.addheaders = [header_tuples]

    def openUrl(self, url):
        return self.opener.open(url).read()


class WPContentParser(object):

    def __init__(self, url_list_file, *args, **kwargs):
        self.fetch = UrlOpener()
        self.file_name = url_list_file

    def _parse_links(self, html_file, base_url, file_pointer, level):
        page_data = BeautifulSoup(html_file)
        href = ''
        for link in page_data.findAll('a'):
            try:
                href = link.get('href')
                if self._is_valid(href):
                    if self._is_file(href):
                        self._save_link(base_url, href, file_pointer)
                    else:
                        # Not required for Apache based servers
                        # if base_url in href:
                        #     page_url = href
                        # else:
                        #     page_url = base_url + href
                        page_url = base_url + href
                        self._parse_links(self.fetch.openUrl(page_url), page_url, file_pointer, level + 1)
            except:
                file_pointer.write('\n--> Error href' + (base_url + href) + '\n')

    def _save_link(self, base_url, href, file_pointer):
        if not re.match(r'[a-zA-Z0-9\-_\/%.\+@]+([0-9]+x[0-9]+).(jpg|jpeg|bmp|gif|png)', href):
            # Not required for Apache based servers
            # if base_url in href:
            #     link = href
            # else:
            #     link = base_url + href
            link = base_url + href
            file_pointer.write(link + '\n')

    def _is_valid(self, link):
        if link is None:
            return False

        # TODO: Move this to a settings file.
        for invalid_directory in ['et_temp', 'wp-content', 'thumbs', 'htm', 'zip', 'doc', 'db', 'Parent Directory', '.com', '#']:
            if invalid_directory in link:
                return False

        return True

    def _is_file(self, link):
        # TODO: Move this to a settings file.
        for ext in ['jpg', 'png', 'jpeg', 'gif', 'bmp']:
            if ext in link.lower():
                return True

        return False

    def get_links(self):
        with open(self.file_name, 'r') as link_file:
            for directory_url in link_file.readlines():
                site_name = directory_url.split('/')[2]
                self._write('Scraping ' + site_name)
                with open(site_name + '_links.txt', 'w') as out_file:
                    self._parse_links(self.fetch.openUrl(directory_url), directory_url.strip('\n'), out_file, level=1)

    def _write(self, msg, indent=0):
        print '\t' * indent, msg


if __name__ == '__main__':
    WPContentParser('test.txt').get_links()
