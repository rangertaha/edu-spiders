edu-spiders
===========

Spiders for crawling course information from various educational institutes.



## Installation

    $ git clone git@github.com:rangertaha/edu-spiders.git
    $ cd edu-spiders
    $ pip install -r requirements.txt

## Execution

To view the list of spiders use the `list` command.

    $ scrapy list

    bhcc.mass.edu
    bu.edu


To crawl the www.bu.edu site use the `bu.edu` spider. To output in *csv* format do the following.

* *-o* output filename
* *-t* output format

    $ scrapy crawl bu.edu -t csv -o data/bu.edu.csv

