#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import scrapy
import hashlib
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from boss.items import BossItem


class Demo(scrapy.spiders.Spider):
    name = "demo"
    allowed_domains = ["www.zhipin.com"]
    start_urls = [
        "http://www.zhipin.com/job_detail/?query=前端&scity=101280600&source=1",
    ]
    url_set = set()
    url_over_set = set()

    def parse(self, response):
        # print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        #
        # current_url = response.url  # 爬取时请求的url
        # body = response.body  # 返回的html
        # unicode_body = response.body_as_unicode()  # 返回的html unicode编码
        # print unicode_body

        md5_obj = hashlib.md5()
        md5_obj.update(response.url)
        md5_url = md5_obj.hexdigest()
        hxs = HtmlXPathSelector(response)
        if md5_url in Demo.url_over_set:
            pass
        else:
            Demo.url_over_set.add(md5_url)
            #获取数据
            items = hxs.xpath('//div[@class="job-list"]/ul/li')  # select中填写查询目标，按scrapy查询语法书写
            for item in items:
                bossItem = BossItem()
                bossItem['jobName'] = item.xpath('./div[@class="job-primary"]/div[@class="info-primary"]/h3/a/text()').extract()[0];
                bossItem['salary'] = item.xpath('./div[@class="job-primary"]/div[@class="info-primary"]/h3/a/span/text()').extract()[ 0];
                bossItem['companyName'] =item.xpath('./div[@class="job-primary"]/div[@class="info-company"]//h3/a/text()').extract()[0];
                bossItem['city'] = item.xpath('./div[@class="job-primary"]/div[@class="info-primary"]/p/text()').extract()[0];
                bossItem['life'] = item.xpath('./div[@class="job-primary"]/div[@class="info-primary"]/p/text()').extract()[1];
                bossItem['education'] = item.xpath('./div[@class="job-primary"]/div[@class="info-primary"]/p/text()').extract()[2];
                bossItem['skill'] = item.xpath('./div[@class="job-tags"]/span/text()').extract();
                bossItem['time'] = item.xpath('./div[@class="job-time"]/span/text()').extract()[0];
                yield bossItem
            #完了后获取地址
            page_url = hxs.select('//div[@class="page"]/a/@href').extract()
            for url in page_url:
                if  not  'javascript' in url:
                    Demo.url_set.add(url)
            next_url = "http://"+Demo.allowed_domains[0]+Demo.url_set.pop();
            yield  Request(next_url,callback=self.parse)
