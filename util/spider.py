from multiprocessing import Process
import scrapy
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Rule

from util.articleScraping import readArticle
from util.natural_language_processing import topic_clustering
from scrapy.contrib.linkextractors import LinkExtractor

texts = []

class Spider(scrapy.Spider):
    name = "spider"
    rules = Rule(LinkExtractor(deny="never_get"), follow=True)
    urls = set()

    def parse(self, response):

        global texts

        # navigazione url

        for url in response.xpath('//a/@href').extract():

            url = response.urljoin(url)

            if self.urls.__contains__(url):
              continue

            self.urls.add(url)

            keyowrds = readArticle(url, 'it')

            if len(keyowrds) > 0:
                texts.append(keyowrds)

            # stop crawler
            if len(texts) > 10:
                break

            yield scrapy.Request(url, callback=self.parse)


# Inizializzazione crawler
# Serve ad eseguire un crawler in un processo separato

class CrawlerScript:

    def __init__(self):
        self.crawler = CrawlerProcess(settings)

    def _crawl(self, allowed_domains, start_urls, lang):
        if lang == 'it':
            self.crawler.crawl(Spider(), allowed_domains=allowed_domains, start_urls=start_urls)
        #else:
            #self.crawler.crawl(Spider(), allowed_domains=allowed_domains, start_urls=start_urls)

        self.crawler.start()
        self.crawler.stop()

        topic_clustering(texts)

    def crawl(self, allowed_domains, start_urls, lang):
        p = Process(target=self._crawl, args=(allowed_domains, start_urls, lang))
        p.start()
        p.join()


myCrawler = CrawlerScript()

# crawler sulla lista di start_urls. la lista dei domini è necessaria per non naavigare le url verso altri domini
# rispetto ai siti inseriti

def crawlDomain(allowed_domains, start_urls, lang):

    myCrawler.crawl(allowed_domains, start_urls, lang)

