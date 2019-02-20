# -*- coding: utf-8 -*-
import scrapy
from azichan.items import AzichanItem
from scrapy_splash import SplashRequest
import re

class AzichanSpiderSpider(scrapy.Spider):
    name = 'azichan_spider'
    allowed_domains = ['azichan.com']
    start_urls = ['http://www.azichan.com/allnotice/list.htm?page=1&']

    def parse(self, response):
        orgNum = response.xpath("//div[@class='orgNum']").extract_first()
        number = int(re.findall("\d+", orgNum)[0])
        page = int(number/10) + 1
        asset_list = response.xpath("//div[@class='mb15 trdate_list_table']//div[@class='orgsList']")
        for i_item in asset_list:
            items = []
            azichan_item = AzichanItem()
            aa = i_item.xpath(".//@onclick").extract_first()
            aaa = re.findall("\d+", aa)
            azichan_item['id'] = aaa[0]
            azichan_item['title'] = i_item.xpath(".//div[@class='trdate_title']/p/text()").extract_first()
            azichan_item['date'] = i_item.xpath(".//div[@class='trdate_title']/span/text()").extract_first()
            azichan_item['transferor'] = i_item.xpath(".//div[@class='trdate_traders'][1]/p[1]/text()").extract_first()
            azichan_item['transferee'] = i_item.xpath(".//div[@class='trdate_traders'][2]/p[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='trdate_assets']/p/text()").extract_first()
            azichan_item['assets'] = "".join(content.split())
            bbb = re.findall(r"'(.+?)'", aa)
            azichan_item['detailUrl'] = 'http://www.azichan.com' + bbb[0]
            items.append(azichan_item)
            for azichan_item in items:
                yield SplashRequest(url=azichan_item['detailUrl'], meta={'item_1': azichan_item}, callback=self.parse_detail)

        i = 1
        while i < page+1:
            i += 1
            next_link = str(i) + '&'
            if i < page+1:
                url = "http://www.azichan.com/allnotice/list.htm?page=" + next_link
                data = {
                    'UM_distinctid': '1682b5645b560c-0fa5ab68fb23dc-4c312e7e-1fa400-1682b5645b64a8',
                    'CNZZDATA1259305347': '1284175877-1546914911-%7C1547001829',
                    'WEB_signKey': '40be0dd9f153c500937f5f326ba5a648',
                    'WEB_niceName': '%E5%93%88%E5%93%88%E5%93%88',
                    'WEB_id': 'fafb7b2736ede60b',
                    'referer': 'http%3A//www.azichan.com/allnotice/list.htm%3Fpage%3D1%26'
                }
                yield scrapy.Request(url=url, cookies=data, callback=self.parse)

    def parse_detail(self, response):
        azichan_item = response.meta['item_1']
        q = response.xpath("//div[@class='debtRightInfo']/em[2]/text()").extract_first()
        azichan_item['debetNumber'] = re.findall("\d+",q)[0]
        azichan_item['debetIntroduction'] = response.xpath("//div[@class='plr50 copyProfile']").extract_first()
        yield azichan_item
