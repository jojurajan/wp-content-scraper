import re
from urllib.request import build_opener
from bs4 import BeautifulSoup

class UrlOpener(object):

    def __init__(self, header_tuples=None):
        self.opener = build_opener()
        if header_tuples is None:
            # Chrome on macos
            self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')]
        else:
            self.opener.addheaders = [header_tuples]

    def openUrl(self, url):
        return self.opener.open(url).read()

class WPContentParser(object):

    def __init__(self, url_list_file, *args, **kwargs):
        self.fetch = UrlOpener()
        self.file_name = url_list_file

    def _parse_links(self, html_file, base_url, file_pointer, level):
        page_data = BeautifulSoup(html_file, features="html.parser")
        print(f'Encoding: {page_data.original_encoding}')
        href = ''
        for link in page_data.findAll('a'):
            try:
                href = link.get('href')
                print(f'Link: {href}')
                if self._is_valid(href):
                    if self._is_file(href):
                        print(f'Saving: {href}')
                        self._save_link(base_url, href, file_pointer)
                    else:
                        # Not required for Apache based servers
                        # if base_url in href:
                        #     page_url = href
                        # else:
                        #     page_url = base_url + href
                        page_url = base_url + href
                        print(f'Parsing Url: {page_url}')
                        self._parse_links(self.fetch.openUrl(page_url), page_url, file_pointer, level + 1)
                else:
                    print(f'Invalid Link')
            except:
                file_pointer.write('\n--> Error href' + (base_url + href) + '\n')

    def _save_link(self, base_url, href, file_pointer):
        link = base_url + href
        file_pointer.write(link + '\n')

    def _is_valid(self, link):
        if link is None:
            return False

        # TODO: Move this to a settings file.
        for invalid_directory in ['?', 'et_temp', 'wp-content', 'thumbs', 'revslider', 'htm', 'Parent Directory', '.com', '#']:
            if invalid_directory in link:
                return False

        return True

    def _is_file(self, link):

        if re.match(r'[a-zA-Z0-9\-_\/%.\+@]+(\d+x\d+)?\.(jpg|jpeg|bmp|gif|png|pdf|svg|zip|rar|7zip|txt|csv|json|xlsx|xls|xml|doc|docx|ppt|pptx|mp3|mp4|webp|php|bin)', link):
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
        print('\t' * indent, msg)


if __name__ == '__main__':
    WPContentParser('test.txt').get_links()
