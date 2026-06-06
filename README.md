edu-spiders
===========

Spiders for crawling course information from various educational institutes.

Built with [Scrapy](https://scrapy.org/). Each spider scrapes course data
(id, title, description, credits, category) from a school's online catalog and
can output to CSV or index directly into Elasticsearch.

## Installation

    $ git clone git@github.com:rangertaha/edu-spiders.git
    $ cd edu-spiders
    $ pip install -r requirements.txt

## Execution

To view the list of spiders use the `list` command.

    $ scrapy list

    bhcc.mass.edu
    bu.edu
    emerson.edu
    extension.harvard.edu
    suffolk.edu
    umb.edu


To crawl the www.bu.edu site use the `bu.edu` spider. To output in *csv* format do the following.

* *-O* output file (overwrite), with an optional `:<format>` suffix

    $ scrapy crawl bu.edu -O data/bu.edu.csv:csv

Crawl output is written to the `data/` directory.
