# -*- coding: utf-8 -*-
import scrapy

from lianjia.items import LianjiaItem

class Lianjiaspider(scrapy.Spider):
    name = 'lianjia1'
    allowed_domains = ['sz.lianjia.com']
    start_urls = []

    # 抓取区域
    regions = { 'baoanqu':'宝安区',
                'nanshanqu':'南山区',
               # 'futianqu':'福田区',
               #  'bihai1': '碧海',
               # 'xixiang': '西乡',
               # 'baoanzhongxin': '宝安中心',
               # 'xinan': '新安',
               # 'qianhai': '前海',
               # 'nantou':'南头',
               # 'nanshanzhongxin':'南山中心',
               }

    # 每个区域抓取多少页
    Crawlpages = 100

    for region in list(regions.keys()):
        if (len(region) == 0):
            for i in range(1, Crawlpages + 1):
                start_urls.append('https://sz.lianjia.com/chengjiao/pg' + str(i) + "/")
        else:
            for i in range(1, Crawlpages + 1):
                start_urls.append('https://sz.lianjia.com/chengjiao/' + region + '/pg' + str(i) + "/")

    def parse(self, response):
        li_item = response.xpath('//ul[@class="listContent"]')
        for li in li_item:
            # hrefs = li.xpath('//a[@class="img"]/@href').extract() #这样会少没图片的房子
            hrefs = li.xpath('//div[@class="info"]//div[@class="title"]//a/@href').extract()
            for href in hrefs:
                yield scrapy.Request(url=href, callback=self.more, dont_filter=True)

    def more(self, response):
        item = LianjiaItem()
        info1 = ''
        #链接地址
        item['url'] = response.url
        # 地区
        area1 = response.xpath('//section[1]/div[1]/a[3]/text()').extract()[0]
        item['region1'] = area1.replace("二手房成交", "")
        area2 = response.xpath('//section[1]/div[1]/a[4]/text()').extract()[0]
        item['region2'] = area2.replace("二手房成交", "")
        # 小区名
        community = response.xpath('//title/text()').extract()[0]
        item['community'] = community[:community.find(" ", 1, len(community))]
        # 成交时间
        deal_time = response.xpath('//div[@class="wrapper"]/span/text()').extract()[0]
        item['deal_time'] = deal_time.replace("成交", "").strip()
        # 成交周期
        item['deal_length'] = response.xpath('//div[@class="msg"]/span[2]/label/text()').extract()[0]
        # 总价
        item['total_price'] = response.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()[0]
        # 单价
        item['unit_price'] = response.xpath('//div[@class="price"]/b/text()').extract()[0]

        # 户型
        introContent = response.xpath('//div[@class="content"]/ul/li/text()').extract()
        item['style'] = introContent[0].strip()
        # 楼层
        item['floor'] = introContent[1].strip()
        # 大小
        item['size'] = introContent[2].strip().replace("㎡","")
        # 朝向
        item['orientation'] = introContent[6].strip()
        # 建成年代
        item['build_year'] = introContent[7].strip()
        # 装修情况
        item['decoration'] = introContent[8].strip()
        # 产权年限
        item['property_time'] = introContent[12].strip()
        # 电梯配备
        item['elevator'] = introContent[13].strip()
        # 其他周边等信息
        infos = response.xpath('//div[@class="content"]/text()').extract()
        if len(infos) != 0:
            for info in infos:
                info = "".join(info.split())
                info1 += info
            item['info'] = info1
        else:
            item['info'] = '暂无信息'
        return item
