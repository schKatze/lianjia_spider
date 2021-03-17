#!/user/bin/python3
# -*- coding = utf-8 -*-
# @Time : 2021/3/16
# @Author : 郑煜辉
# @File : home
from scrapy import Request
from scrapy.spiders import Spider
from lianjia_home.items import LianjiaHomeItem


class HomeSpider(Spider):
    name = 'home'


    def start_requests(self):
        url = "https://su.lianjia.com/ershoufang/"
        yield Request(url)

    def parse(self, response, **kwargs):
        list_selecotr = response.xpath("//li/div[@class='info clear']")
        for one_selecotr in list_selecotr:
            try:
                name = one_selecotr.xpath("div[@class='address']/"
                                          "div[@class='houseInfo']"
                                          "/a/text()").extract_first()
                other = one_selecotr.xpath("div[@class='address']/"
                                           "div[@class='houseInfo']"
                                           "/text()").extract_first()
                other_list = other.split("|")
                type = other_list[1].strip(" ")
                area = other_list[2].strip(" ")
                direction = other_list[3].strip(" ")
                fitment = other_list[4].strip(" ")
                elevator = other_list[5].strip(" ")
                price_list = one_selecotr.xpath("div[@class='priceInfo']//span/text()")
                total_price = price_list[0].extract()
                unit_price = price_list[1].extract()
                item = LianjiaHomeItem()
                item["name"] = name.strip(" ")
                item["type"] = type
                item["area"] = area
                item["direction"] = direction
                item["fitment"] = fitment
                item["elevator"] = elevator
                item["total_price"] = total_price
                item["unit_price"] = unit_price
                url = one_selecotr.xpath("div[@class='title]/a/@href").extract_first()
                yield Request(url, meta={"item": item}, callback=self.property_parse)

            except:
                pass

            if self.current_page == 1:
                self.total_page = response.xpath("//div[@class='page-box house-lst-page-box']" "//@page-data").re("\d+")
                self.total_page = int(self.total_page[0])
            self.current_page += 1
            if self.current_page <= self.total_page:
                next_url = "https://su.lianjia.com/ershoufang/pg%d" % (self.current_page)
                return Request(next_url)


    def property_parse(self,response):
        property = response.xpath("//div[@class = 'base']/div[@class = 'content']/ul/li[12]/text()").extract_first()
        item = response.meta["item"]
        item["property"] = property
        yield item