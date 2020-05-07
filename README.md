#Imdb_web_scrap

Script is tested with python2.7

pip install requests
pip install lxml

Usage: imdbCrawler.py [-h] [-p PARALLELTHREADS] [-r] [-t]

IMDB Top 250 Movies Data Extractor

optional arguments:
  -h, --help            show this help message and exit
  -p PARALLELTHREADS, --parallelThreads PARALLELTHREADS
                        Thread count to crawl url in parallel (1-25)
  -r, --includeMovieRanking
                        include movie ranking
  -t, --includeMovieTitle
                        include movie title


Example:
python imdbCrawler.py -p 25

it will crawl with 25 parallel threads and dump json file as name <imdbTop250MoviesCrawlResults.json> in thew same directory where the script is run.

Example:
python imdbCrawler.py -p 10 -t -r

it will crawl with 10 parallel threads and dump json file (including title and ranking) as name <imdbTop250MoviesCrawlResults.json> in thew same directory where the script is run.
