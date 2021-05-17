#!/usr/bin/env python3

import os
from urllib.parse import urlparse
import requests
import lxml.html


def etl_main() -> None:
    """
    Scraping version of ETL: Extracting, Transformation, Loading.
    """
    output_directory = './out-directory'
    input_parameters = [
        {
            'http://127.0.0.1/index-01.html': None,
            'http://127.0.0.1/index-02.html': {'method': 'head'},
            'http://127.0.0.1/index-03.html': {'xpath': '//*'}, },
        {
            'http://127.0.0.1/index-04.html': {'filename': 'filename-04.txt'},
            'http://127.0.0.1/index-05.html': {'method': 'put', 'xpath': '//*'},
            'http://127.0.0.1/index-06.html': {'fixext': 'txt'}, },
    ]

    # Extracting.
    extracted_parameters = scraping_parameters(
        data=input_parameters)
    extracted_data = scraping_extracting(data=extracted_parameters)

    # Transformation.
    transformed_data = scraping_transformation(data=extracted_data)

    # Loading.
    loading_result = scraping_loading(
        directory=output_directory, data=transformed_data)

    print(loading_result)


def scraping_parameters(data: list = None) -> list:
    """
    Generator of the list of dict elements from the input list of dict.

    The key as the URL.
    Fills in and corrects all values: method, url, xpath, file name.

    Example:
        r = scraping_parameters([{
            'http://127.0.0.1/info.html': {'method': 'put', }, }, ])
    """
    if data is None:
        return None
    r = list()
    for item in data:
        n = {}
        for k, v in item.items():
            i = {
                'method': (v if v is not None else {}).get('method', 'GET'),
                'url': k,
                'xpath': (v if v is not None else {}).get('xpath', '//*'),
                'filename': (v if v is not None else {}).get('filename', None),
            }
            if i['filename'] is None:
                i['filename'] = os.path.basename(urlparse(k).path)
            if i['filename'] in ['', ]:
                i['filename'] = 'index.html'
            fixext = (v if v is not None else {}).get('fixext', None)
            if fixext is not None:
                i['filename'] = os.path.splitext(i['filename'])[0] + "." + fixext
            n[k] = i
        if len(n.keys()) > 0:
            r.append(n)
    if len(r) > 0:
        return r
    return None


def scraping_http_extracting(
        method: str ='GET',
        url: str = 'http://127.0.0.1/index.html'):
    """
    Extracting from HTTP.

    Example:
        print(scraping_extracting('GET', 'http://127.0.0.1/index.html', '//*'))
    """
    try:
        result = requests.request(method=method, url=url).text
    except:
        return None
    return result


def scraping_extracting(data: list = None) -> list:
    """
    Scraping extracting from HTTP.

    Example:
        print(scraping_extracting(
            scraping_extracting_parameters([{
                'http://127.0.0.1/info.html': {'method': 'put', }, }, ])))
    """
    if data is None:
        return None
    for item in data:
        for k, v in item.items():
            v['extraction result'] = scraping_http_extracting(
                method=v['method'], url=v['url'])
    if len(data) > 0:
        return data
    return None


def scraping_transformation(data: list = None) -> list:
    """
    Data XPath transformation.
    """
    if data is None:
        return None
    for item in data:
        for k, v in item.items():
            try:
                tree = lxml.html.document_fromstring(v['extraction result'])
                xscraping = tree.xpath(v['xpath'])
            except:
                xscraping = None
            del v['extraction result']  # free memory
            v['transformation result'] = xscraping
    if len(data) > 0:
        return data
    return None


def send_data_to_file(filename: str = 'f.txt', data: str = 'text') -> str:
    """
    Text to file.

    Example:
        send_data_to_file('filename2.txt', 'Info string')
    """
    if (filename is not None) and (data is not None):
        with open(file=filename, mode='w', newline='') as out_file:
            out_file.write(data)
            out_file.close()
        return "Ok"
    return "Empty None"


def scraping_loading(directory: str = './out', data: list = None) -> str:
    """
    Sends the cleared data from the list of dict items to files in the folder.
    """
    if data is None:
        return "Empty None"
    for item in data:
        for k, v in item.items():
            v['loading'] = send_data_to_file(
                filename=os.path.join(directory, v['filename']),
                data="".join(v['transformation result']))
    if len(data) > 0:
        return data
    return "Empty Zero"


if __name__ == '__main__':
    etl_main()
