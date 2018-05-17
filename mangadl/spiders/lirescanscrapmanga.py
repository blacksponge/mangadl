import scrapy
import copy


class LireScanScrapMangaSpider(scrapy.Spider):
    name = 'lirescanscrapmangaspider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'mangadl.pipelines.MangadlPipeline': 1
        }
    }

    def start_requests(self):
        url = 'http://m.lirescan.net'
        manga_url = getattr(self, 'url', '')
        item = {
            'manga': getattr(self, 'title', '')
        }
        yield scrapy.Request(
            url + manga_url, self.parse, meta={'item': item})

    def parse(self, response):
        for option in response.css('select#chapitres option'):
            item = dict(response.meta['item'])
            item['chapter'] = option.css('::text').extract_first()
            yield response.follow(
                option.css('::attr(value)').extract_first(),
                self.parse_pages, meta={'item': item})

    def parse_pages(self, response):
        for option in response.css('select#pages option'):
            item = dict(response.meta['item'])
            item['page'] = option.css('::text').extract_first()
            yield response.follow(
                option.css('::attr(value)').extract_first(),
                self.parse_image, meta={'item': item})

    def parse_image(self, response):
        item = response.meta['item']
        item['image'] = response.urljoin(response.css('img#image_scan::attr(src)').extract_first())
        yield item
