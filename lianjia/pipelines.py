# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import pymongo
from lianjia.model import LianjiaInfo


class MongoPipeline(object):
    def process_item(self, item, spider):
        LianjiaInfo.create(url=item['url'],
                           region1=item['region1'],
                           region2=item['region2'],
                           community=item['community'],
                           deal_time=item['deal_time'],
                           deal_length=item['deal_length'],
                           total_price=item['total_price'],
                           unit_price=item['unit_price'],
                           style=item['style'],
                           floor=item['floor'],
                           size=item['size'],
                           orientation=item['orientation'],
                           build_year=item['build_year'],
                           decoration=item['decoration'],
                           property_time=item['property_time'],
                           elevator=item['elevator'],
                           info=item['info'])
        return item
