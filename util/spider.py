from multiprocessing import Process
import scrapy
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from util.articleScraping import readArticle
from util.natural_language_processing import topic_clustering

texts = []


class Spider(scrapy.Spider):
    name = "spider"
    lang = 'it'

    def parse(self, response):

        page = response.url

        global texts

        # Toppino per non analizzare le homepage

        link = page.replace("https://", "")
        link = link.replace("http://", "")

        if len(link.split("/")) > 1:

            keyowrds = readArticle(page, self.lang)

            if len(keyowrds) > 0:
                texts.append(keyowrds)

        # navigazione url

        for url in response.xpath('//a/@href').extract():
            url = response.urljoin(url)

            yield scrapy.Request(response.urljoin(url), callback=self.parse)


# Inizializzazione crawler
# Serve ad eseguire un crawler in un processo separato

class CrawlerScript:

    def __init__(self):
        self.crawler = CrawlerProcess(settings)

    def _crawl(self, allowed_domains, start_urls, lang):

        self.crawler.crawl(Spider(), allowed_domains=allowed_domains, start_urls=start_urls, lang=lang)

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

