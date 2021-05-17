import json
import unittest
from lxml import etree


from scraping_sites_directory import (
    scraping_parameters, scraping_http_extracting, scraping_extracting,
    scraping_transformation, send_data_to_file, scraping_loading)


class TestScrapingSitesDirectory(unittest.TestCase):

    do_debug_pprint = True

    def debug_print(self, data_in, data_out):
        print("in:", data_in)
        print("out:", data_out)
    
    def debug_pprint(self, data_in, data_out):
        import pprint
        print("in:")
        pprint.pprint(data_in)
        print("out:")
        pprint.pprint(data_out)

    def test_scraping_parameters_empty_data(self):
        """
        Check that it can accept an empty value of the input data-parameter.
        """
        result = scraping_parameters()
        self.assertEqual(result, None)

        result = scraping_parameters(None)
        self.assertEqual(result, None)

        result = scraping_parameters(data=None)
        self.assertEqual(result, None)

        data_none = None
        result = scraping_parameters(data=data_none)
        self.assertEqual(result, None)

        data_none = []
        result = scraping_parameters(data=data_none)
        self.assertEqual(result, None)

        data_none = [{}, {}, {}, ]
        result = scraping_parameters(data=data_none)
        self.assertEqual(result, None)

    def test_scraping_parameters_one_data(self):
        """
        Check that it can accept an One value of the input data-parameter.
        """
        result = scraping_parameters(data=[
            {}, {}, {}, {"y": None, }, ])
        self.assertEqual(result, [{'y': {
            'method': 'GET', 'url': 'y', 'xpath': '//*', 'filename': 'y'}}])

    def test_scraping_http_extracting_ifconfigme_encoding(self):
        result = scraping_http_extracting(
            method='GET', url='https://ifconfig.me/encoding')
        self.assertEqual(result, 'gzip, deflate')

    def test_scraping_parameters_none_value(self):
        """
        Test with key and none value.
        """
        result = scraping_parameters(data=[
            {'http://127.0.0.1/a-index-01.html': None, },
            {'http://127.0.0.1/a-index-01.html': None, },
            {'http://127.0.0.1/b/index-02.html': None,
             'http://127.0.0.1/c/d/index-03.html': None, }, ])
        compare_out = [
            {'http://127.0.0.1/a-index-01.html': {
                'method': 'GET', 'url': 'http://127.0.0.1/a-index-01.html',
                'xpath': '//*', 'filename': 'a-index-01.html'}, },
            {'http://127.0.0.1/a-index-01.html': {
                'method': 'GET', 'url': 'http://127.0.0.1/a-index-01.html',
                'xpath': '//*', 'filename': 'a-index-01.html'}, },
            {'http://127.0.0.1/b/index-02.html': {
                'method': 'GET', 'url': 'http://127.0.0.1/b/index-02.html',
                'xpath': '//*', 'filename': 'index-02.html'},
             'http://127.0.0.1/c/d/index-03.html': {
                 'method': 'GET', 'url': 'http://127.0.0.1/c/d/index-03.html',
                 'xpath': '//*', 'filename': 'index-03.html'}, }, ]
        if self.do_debug_pprint:
            self.debug_pprint(data_in=result, data_out=compare_out)
        self.assertEqual(result, compare_out)

    def test_scraping_parameters_none_value_key_with_parameters(self):
        """
        Test with key and none value.
        """
        result = scraping_parameters(data=[
            {'http://127.0.0.1': None, },
            {'http://127.0.0.1/': None, },
            {'http://127.0.0.1/e/info-04.php': None, },
            {'http://127.0.0.1/f/g/info-05.php?v=utf-8&index=7': None, }, ])
        compare_out = [
            {'http://127.0.0.1': {
                'method': 'GET', 'url': 'http://127.0.0.1',
                'xpath': '//*', 'filename': 'index.html'}, },
            {'http://127.0.0.1/': {
                'method': 'GET', 'url': 'http://127.0.0.1/',
                'xpath': '//*', 'filename': 'index.html'}, },
            {'http://127.0.0.1/e/info-04.php': {
                'method': 'GET', 'url': 'http://127.0.0.1/e/info-04.php',
                'xpath': '//*', 'filename': 'info-04.php'}, },
            {'http://127.0.0.1/f/g/info-05.php?v=utf-8&index=7': {
                'method': 'GET', 'url': 'http://127.0.0.1/f/g/info-05.php?v=utf-8&index=7',
                'xpath': '//*', 'filename': 'info-05.php'}, }, ]
        if self.do_debug_pprint:
            self.debug_pprint(data_in=result, data_out=compare_out)
        self.assertEqual(result, compare_out)

    def test_scraping_parameters_method_xpath(self):
        """
        Test witk key and dict value: method, xpath.
        """
        result = scraping_parameters(data=[
            {'http://127.0.0.1/index-06.html': {'method': 'head'}, },
            {'http://127.0.0.1/index-07.html': {'xpath': '//html/*'}, },
            {'http://127.0.0.1/index-08.html': {
                'method': 'put', 'xpath': '//api/*'}, }, ])
        compare_out = [
            {'http://127.0.0.1/index-06.html': {
                'method': 'head', 'url': 'http://127.0.0.1/index-06.html',
                'xpath': '//*', 'filename': 'index-06.html'}, },
            {'http://127.0.0.1/index-07.html': {
                'method': 'GET', 'url': 'http://127.0.0.1/index-07.html',
                'xpath': '//html/*', 'filename': 'index-07.html'}, },
            {'http://127.0.0.1/index-08.html': {
                'method': 'put', 'url': 'http://127.0.0.1/index-08.html',
                'xpath': '//api/*', 'filename': 'index-08.html'}, }, ]
        if self.do_debug_pprint:
            self.debug_pprint(data_in=result, data_out=compare_out)
        self.assertEqual(result, compare_out)

    def test_scraping_parameters_filename(self):
        """
        Test witk key and dict value: filename.
        """
        result = scraping_parameters(data=[
            {'http://127.0.0.1/': {
                'filename': 'filename-09.txt', }, },
            {'http://127.0.0.1/h/index-05.html': {
                'filename': 'filename-10.txt', 'method': 'head'}, },
            {'http://127.0.0.1/i/j/info-06.php?v=utf-8&index=7': {
                'filename': 'filename-11.txt', 'xpath': '//html/*'}, },
            {'http://127.0.0.1/k/index-07.html': {
                'filename': 'filename-12.txt', 'method': 'head'}, },
            {'http://127.0.0.1/l/m/n/info-08.php?v=utf-8&index=5': {
                'filename': 'filename-13.txt', 'xpath': '//html/*'}, }, ])
        compare_out = [
            {'http://127.0.0.1/': {
                'method': 'GET', 'url': 'http://127.0.0.1/',
                'xpath': '//*', 'filename': 'filename-09.txt'}, },
            {'http://127.0.0.1/h/index-05.html': {
                'method': 'head', 'url': 'http://127.0.0.1/h/index-05.html',
                'xpath': '//*', 'filename': 'filename-10.txt'}, },
            {'http://127.0.0.1/i/j/info-06.php?v=utf-8&index=7': {
                'method': 'GET', 'url': 'http://127.0.0.1/i/j/info-06.php?v=utf-8&index=7',
                'xpath': '//html/*', 'filename': 'filename-11.txt'}, },
            {'http://127.0.0.1/k/index-07.html': {
                'method': 'head', 'url': 'http://127.0.0.1/k/index-07.html',
                'xpath': '//*', 'filename': 'filename-12.txt'}, },
            {'http://127.0.0.1/l/m/n/info-08.php?v=utf-8&index=5': {
                'method': 'GET', 'url': 'http://127.0.0.1/l/m/n/info-08.php?v=utf-8&index=5',
                'xpath': '//html/*', 'filename': 'filename-13.txt'}, }, ]
        if self.do_debug_pprint:
            self.debug_pprint(data_in=result, data_out=compare_out)
        self.assertEqual(result, compare_out)

    def test_scraping_parameters_filename_fixext(self):
        """
        Test witk key and dict value: filename, fixext.
        """
        result = scraping_parameters(data=[
            {'http://127.0.0.1/': {
                'filename': 'filename-14.txt', }, },
            {'http://127.0.0.1/h/index-09.html': {
                'filename': None, 'method': 'head', 'fixext': 'jpeg'}, },
            {'http://127.0.0.1/i/j/info-10.php?v=utf-8&index=7': {
                'filename': 'filename-15.txt', 'xpath': '//html/*', 'fixext': 'png'}, },
            {'http://127.0.0.1/k/index-11.html': {
                'filename': 'filename-16.txt', 'method': 'head', 'fixext': 'info'}, },
            {'http://127.0.0.1/l/m/n/info-12.php?v=utf-8&index=5': {
                'filename': 'filename-17.txt', 'xpath': '//html/*', 'fixext': 'pdf'}, }, ])
        compare_out = [
            {'http://127.0.0.1/': {
                'method': 'GET', 'url': 'http://127.0.0.1/',
                'xpath': '//*', 'filename': 'filename-14.txt'}, },
            {'http://127.0.0.1/h/index-09.html': {
                'method': 'head', 'url': 'http://127.0.0.1/h/index-09.html',
                'xpath': '//*', 'filename': 'index-09.jpeg'}, },
            {'http://127.0.0.1/i/j/info-10.php?v=utf-8&index=7': {
                'method': 'GET', 'url': 'http://127.0.0.1/i/j/info-10.php?v=utf-8&index=7',
                'xpath': '//html/*', 'filename': 'filename-15.png'}, },
            {'http://127.0.0.1/k/index-11.html': {
                'method': 'head', 'url': 'http://127.0.0.1/k/index-11.html',
                'xpath': '//*', 'filename': 'filename-16.info'}, },
            {'http://127.0.0.1/l/m/n/info-12.php?v=utf-8&index=5': {
                'method': 'GET', 'url': 'http://127.0.0.1/l/m/n/info-12.php?v=utf-8&index=5',
                'xpath': '//html/*', 'filename': 'filename-17.pdf'}, }, ]
        if self.do_debug_pprint:
            self.debug_pprint(data_in=result, data_out=compare_out)
        self.assertEqual(result, compare_out)

    def test_scraping_extracting_none_value(self):
        """
        Check that it can accept an empty value of the input data-parameter.
        """
        result = scraping_extracting()
        self.assertEqual(result, None)

        result = scraping_extracting(None)
        self.assertEqual(result, None)

        result = scraping_extracting(data=None)
        self.assertEqual(result, None)

        result = scraping_extracting(data=[])
        self.assertEqual(result, None)

    def test_scraping_extracting_ifconfigme_encoding(self):
        """
        Checking the operation of a request in ifconfig.me
        with the control of its encoding.
        """
        result = scraping_extracting(
            data=scraping_parameters(
                data=[{'https://ifconfig.me/encoding': None, }, ]))
        compare_out = "gzip, deflate"
        if self.do_debug_pprint:
            self.debug_print(data_in=result, data_out=compare_out)
        self.assertEqual(
            result[0]['https://ifconfig.me/encoding']['extraction result'],
            compare_out)

    def test_scraping_transformation_facebook_check_id(self):
        """
        Checking the operation of a request in facebook
        with the control of its ID.
        """
        result = scraping_transformation(
            data=scraping_extracting(
                data=scraping_parameters(
                    data=[{
                        'https://www.facebook.com/': {
                            'xpath': '//*[@id="facebook"]'}, }, ])))
        compare_out = "facebook"
        if self.do_debug_pprint:
            self.debug_print(data_in=result, data_out=compare_out)
        self.assertEqual(
            ";".join(
                [x.get("id")
                 for x in result[0]['https://www.facebook.com/'][
                     'transformation result']]),
            compare_out)

    def test_send_data_to_file_empty_data(self):
        """
        Test sending data to a file with empty parameters and data,
        in which the file should not be created.

        TODO: Check for missing file, successful if it is missing
        """
        filename = None
        data_none = None
        compare_out = "Empty None"

        self.assertEqual(
            send_data_to_file('./out/filename-18.txt', data=None),
            compare_out)
        self.assertEqual(
            send_data_to_file('./out/filename-19.txt', data=data_none),
            compare_out)
        self.assertEqual(
            send_data_to_file(None, 'Info string'),
            compare_out)
        self.assertEqual(
            send_data_to_file(None, None),
            compare_out)
        self.assertEqual(
            send_data_to_file(filename=filename, data=None),
            compare_out)
        self.assertEqual(
            send_data_to_file(filename=None, data=data_none),
            compare_out)
        self.assertEqual(
            send_data_to_file(filename=filename, data=data_none),
            compare_out)

    def test_scraping_loading(self):
        """
        """
        site_url = 'https://www.songtexte.com/songtext/pink-floyd/another-brick-in-the-wall-b9615ee.html'
        xpath = '//*[@id="main"]/div/div/div//*[@class="lyricsContainer"]/div/text()'
        filename = 'Pink-Floyd--Another-brick-in-the-wall.txt'

        result = scraping_loading(
            directory='.',
            data=scraping_transformation(
                data=scraping_extracting(
                    data=scraping_parameters(
                        data=[{site_url: {
                            'xpath': xpath, 'filename': filename,
                        }, }, ]))))
        self.assertEqual(result[0][site_url]['loading'], 'Ok')

        with open(
            'test_scraping_sites_directory-another-brick-in-the-wall.txt',
            mode='r') as in_file:
            compare_out = in_file.read()
            in_file.close()
        with open(filename, mode='r') as in_file:
            compare_in = in_file.read()
            in_file.close()

        if self.do_debug_pprint:
            self.debug_print(data_in=compare_in, data_out=compare_out)
        self.assertEqual(compare_in, compare_out)


if __name__ == '__main__':
    unittest.main()
