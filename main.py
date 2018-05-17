from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from mangadl.spiders.lirescanmangalist import LireScanMangaListSpider


configure_logging()
runner = CrawlerRunner(get_project_settings())
mangas = []


def add_manga(item, response, spider):
    spider.logger.debug('Fetched Manga: %s', item['title'])
    mangas.append(item)


def display_manga_list(mangas):
    for index, manga in enumerate(mangas):
        print(' [%d] %s' % (index, manga['title']))


@defer.inlineCallbacks
def main():
    print('Fetching manga list...')
    manga_list_crawler = runner.create_crawler('lirescanmangalist')
    manga_list_crawler.signals.connect(add_manga, signal=signals.item_scraped)
    yield runner.crawl(manga_list_crawler)
    display_manga_list(mangas)
    chosen_manga_index = int(input('Input manga index : '))
    chosen_manga = mangas[chosen_manga_index]
    print(chosen_manga)
    yield runner.crawl('lirescanscrapmangaspider', **chosen_manga)
    reactor.stop()


if __name__ == '__main__':
    main()
    reactor.run()
