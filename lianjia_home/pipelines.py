# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

from scrapy.exceptions import DropItem


class FilterPipeline(object):
    def process_item(self, item, spider):
        item["area"] = re.findall(r"\d+\.?d*", item["area"])[0]
        item["unit_price"] = re.findall(r"\d+\.?\d*", item["unit_price"])[0]
        item["property"] = re.findall(r"\d+\.?\d*", item["property"])[0]
        if item["direction"] == "暂无数据":
            raise DropItem("房屋朝向无数据，抛弃此项目： %s" % item)
        return item


class CSVPipeline(object):
    index = 0
    file = None

    def open_spider(self, spider):
        self.file = open("home.csv", "a", encoding="utf-8")

    def process_item(self, item, spider):
        if self.index == 0:
            column_name = "name,type,area,direction,fitment,elevator,total_price,unit_price,property\n"
            self.file.write(column_name)
            self.index = 1

        home_str = item["name"] + "," + \
                   item["type"] + "," + \
                   item["area"] + "," + \
                   item["direction"] + "," + \
                   item["fitment"] + "," + \
                   item["elevator"] + "," + \
                   item["total_price"] + "," + \
                   item["unit_price"] + "," + \
                   item["property"] + "\n"
        self.file.write(home_str)
        return item
    def close_spider(self,spider):
        self.file.close()


class LianjiaHomePipeline:
    def process_item(self, item, spider):
        return item
