#-*-coding:utf-8-*-
__author__ = 'cchen'


class Fetcher(object):
    session = None
    proxy = None

    def get(self, url, *kwargs):
        raise NotImplementedError

    def get_json(self, url, **kwargs):
        raise NotImplementedError

    def find(self, *args):
        raise NotImplementedError

    def find_all(self, *args):
        raise NotImplementedError

    def source_code(self):
        raise NotImplementedError

    def build(self, source_page, *args, **kwargs):
        raise NotImplementedError
