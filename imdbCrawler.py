# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import argparse
from collections import OrderedDict
import json
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106"
}
HOST = "http://www.imdb.com/"
URL = "https://www.imdb.com/chart/top?ref_=nv_mv_250"

parser = argparse.ArgumentParser(description="IMDB Top 250 Movies Data Extractor")
parser.add_argument("-p", "--parallelThreads", action="store", dest="parallelThreads", type=int, default=1,
                    help="Thread count to crawl url in parallel (1-25)")
parser.add_argument("-r", "--includeMovieRanking", action="store_true", dest="ranking", default=False,
                    help="include movie ranking")
parser.add_argument("-t", "--includeMovieTitle", action="store_true", dest="title", default=False,
                    help="include movie title")
args = parser.parse_args()

urls = []

response = requests.get(URL, headers=HEADERS)
dom = html.fromstring(response.text)
dom.make_links_absolute(HOST)
elements = dom.xpath('//td[@class="titleColumn"]//a')
for i, el in enumerate(elements):
    urls.append(el.attrib["href"])

# limit parallel threads between 1 and 25
if args.parallelThreads > 25:
    args.parallelThreads = 25
if args.parallelThreads < 1:
    args.parallelThreads = 1

def get_Details(url):
    response = requests.get(url, headers=HEADERS)
    dom = html.fromstring(response.content)
    dom.make_links_absolute(HOST)
    data = OrderedDict()
    elements = dom.xpath('//a[contains(@href, "/chart/top?ref_=tt_awd")]//text()')
    data.update({"imdb_position": elements[0].split("#")[1].strip()}) if elements else data.update(
        {"imdb_position": ""})
    if args.title:
        elements = dom.xpath('//meta[@property="og:title"]/@content')
        data.update({"title": elements[0].split('(')[0].strip()}) if elements else data.update({"title": ""})
    elements = dom.xpath('//span[@itemprop="ratingValue"]//text()')
    data.update({"rating": elements[0]}) if elements else data.update({"rating": ""})
    elements = dom.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a//text()')
    data.update({"director": elements}) if elements else data.update({"director": ""})
    elements = dom.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[3]/a//text()')
    data.update({"writer": elements}) if elements else data.update({"writer": ""})
    elements = dom.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[4]/a//text()')
    data.update({"stars": elements[:-1]}) if elements else data.update({"stars": ""})
    elements = dom.xpath('//*[@id="titleDetails"]/div[h4="Release Date:"]/text()')
    data.update({"release_date": elements[1].strip()}) if elements else data.update({"release_date": ""})
    elements = dom.xpath('//div[@class="poster"]//img/@src')
    data.update({"moview_poster_url": elements}) if elements else data.update({"moview_poster_url": ""})
    return data


with ThreadPoolExecutor(max_workers=args.parallelThreads) as executor:
    results = executor.map(get_Details, urls)
    res = sorted(results, key=lambda i: int(i['imdb_position']))
    if not args.ranking:
        for item in res:
            del item["imdb_position"]
    file_path = "imdbTop250MoviesCrawlResults.json"
    with open(file_path, "w") as f:
        f.write(json.dumps(res))
