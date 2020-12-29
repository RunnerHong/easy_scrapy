#!/usr/bin/env python
# @Time    : 2020/12/29 10:00
# @Author  : 洪英杰
# @Python  : 3.7.5
# @File    : easy_scrapy
# @Project : easy_scrapy
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "easy"

    def start_requests(self):
        url = 'http://www.cnstats.org/tjgb/'
        yield scrapy.Request(url=url, callback=self.parse)
        for i in range(2, 729):
            next_url = f'{url}/index_{i}.html'
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse(self, response):
        paths = response.xpath('/html/body/div/div[2]/ul/li/a')
        for path in paths:
            url = path.css('a::attr(href)').get()
            if url is not None:
                yield response.follow(url, callback=self.parse_data)

    def parse_data(self, response):
        title = response.xpath('/html/body/article/div[1]/ul/p[1]').css(
            'p::text').get()
        value = response.xpath('/html/body/article/div[1]/ul/ul').re(
            r'\d+(?:\.\d+)?亿元')[0]
        yield {
            'title': title,
            'value': value
        }