# site-scraping-to-directory
Scraping texts from the list of sites to the output directory into separate text files

## install
* Install Python 3.x: https://www.python.org/about/gettingstarted/
* Getting files (in console):
```shell script
$ wget https://raw.githubusercontent.com/AssaToolex/site-scraping-to-directory/main/scraping_sites_directory.py
$ wget https://raw.githubusercontent.com/AssaToolex/site-scraping-to-directory/main/requirements.txt
$ pip install -r requirements.txt
```

## Add custom parameters
Inside the scraping_sites_directory.py file, change this input_parameters:
```shell script
$ nano scraping_sites_directory.py
```

## run
In console:
```shell script
$ python scraping_sites_directory.py
```

## run unittests
If you want, download the full version of the repository (https://github.com/AssaToolex/site-scraping-to-directory) and run the tests:
```shell script
$ pip install -r requirements-test.txt
$ pytest
```
