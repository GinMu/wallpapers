import scrapy
import os
from wallpapers.items import WallpapersItem
url = 'http://wallpaperswide.com/girls-desktop-wallpapers.html'
host = 'http://wallpaperswide.com'
class WallPapersSpider(scrapy.Spider):
    name = 'wallpapers_spider'
    start_urls = ['http://wallpaperswide.com/girls-desktop-wallpapers.html']
    def parse(self, response):
        pages = response.xpath('//div[@class="pagination"]/a[last()-1]/text()').extract()[0]
        for page in range(int(pages)):
            p = str(page + 1)
            full_url = url + '/page/' + p
            yield scrapy.Request(full_url, callback=self.parse_category)

    def parse_category(self, response):
        hrefs = response.xpath('//ul[@class="wallpapers"]/li/div/div/a/@href')
        for href in hrefs:
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_detail)


    def parse_detail(self, response):
        url = response.xpath('//div[@class="wallpaper-resolutions"]/a[text()="1920x1080"]/@href').extract()
        if len(url) == 0:
            url = response.xpath('//div[@class="wallpaper-resolutions"]/a[text()="1920x1200"]/@href').extract()

        if len(url) != 0:
            item = WallpapersItem()
            item['image_urls'] = host + url[0]
            return item
