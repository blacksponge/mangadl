import scrapy
from scrapy import signals


class LireScanMangaListSpider(scrapy.Spider):
    name = 'lirescanmangalist'
    start_urls = ['http://m.lirescan.net']

    def parse(self, response):
        for option in response.css('select#mangas option'):
            manga_url = option.css('::attr(value)').extract_first()
            manga = {
                'url': manga_url,
                'title': option.css('::text').extract_first()
            }
            yield manga
