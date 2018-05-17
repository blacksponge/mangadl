# -*- coding: utf-8 -*-

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MangadlPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print('*' * 80)
        print(info)
        yield scrapy.Request(item['image'], meta={'item': item})

    def file_path(self, request, response=None, info=None):
        return '%s/%s/%s.jpg' % (
            request.meta['item']['manga'],
            request.meta['item']['chapter'],
            request.meta['item']['page']
        )
