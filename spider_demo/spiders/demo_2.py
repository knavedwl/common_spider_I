import scrapy
from scrapy.selector import Selector
import copy
import logging
from spider_demo.items import SpiderDemoItem
class DemoSpider(scrapy.Spider):
    name = "demo_spider_2"
    start_urls = ['http://www.strongberry.cn/find_room.aspx']
    allowed_domains = []


    '''
    · settings文件是所有spider的公用配置文件
    · 建议每个spider有自己独立的配置，用custom_settings覆盖settings的设置
    '''
    custom_settings = {
        # 'LOG_FILE': logs_path + '/logs/NewsSpiderI_log.log',
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1.5,  # 初始下载延迟(单位：秒)。
        'AUTOTHROTTLE_MAX_DELAY': 10,  # 在高延迟情况下最大的下载延迟
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 100,  # 同一时间的请求量（并发量）
        'AUTOTHROTTLE_DEBUG': True,  # 起用 AutoThrottle 调试(debug)模式，展示每个接收到的 response。您可以通过此来查看限速参数是如何实时被调整的。
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,  # 同一域名的并发量
        'CONCURRENT_REQUESTS': 100,
        'DOWNLOAD_DELAY': 1.5,  # 自动节流器会把delay控制在DOWNLOAD_DELAY与AUTOTHROTTLE_MAX_DELAY之间的最优值
        'DOWNLOADER_MIDDLEWARES': {
            'spider_demo.middlewares.SpiderDemoIIDownloaderMiddleware': 543,
        },
        'SPIDER_MIDDLEWARES': {
            'spider_demo.middlewares.SpiderDemoIISpiderMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'spider_demo.pipelines.SpiderDemoPipeline': 200,
        },
        'DOWNLOAD_TIMEOUT': 30,
        'RETRY_TIMES': 3,
    }

    def parse(self, response):
        headers = eval(str(response.headers))
        meta = copy.deepcopy(response.meta)
        html = response.body.decode("utf-8")
        list = Selector(text=html).xpath("//a[@class='wow fadeInUp animated animated']").extract()
        for li in list:
            detail_href = "http://www.strongberry.cn/"+Selector(text=li).xpath(".//@href").extract_first()
            item = SpiderDemoItem()
            item["name"] = Selector(text=li).xpath("//div[@class='tit']/text()").extract_first()
            item["address"] = Selector(text=li).xpath("//div[@class='text']/p[2]/text()").extract_first()
            item["price"] = Selector(text=li).xpath("//div[@class='price']/em/text()").extract_first()+"元起"

            yield scrapy.Request(
                url=detail_href,
                headers=headers,
                meta={'item': item, "detail":True},
                callback=self.parse_detail,
                dont_filter=True)
        a = self.driver.find_elements_by_xpath("//div[@class='next fr']")
        if len(a) > 0:
            a.click()
            yield scrapy.Request(
                url=response.url,
                headers=headers,
                callback=self.parse,
                dont_filter=True)
        print("hello world")

        # 请求二级页面(详情页)，要封装一致的headers，主要是cookie的传递，避免反爬
        # yield scrapy.Request(
        #     url=detail_url,
        #     headers=headers,
        #     meta=meta,
        #     callback=self.parse_detail,
        #     dont_filter=True)

    def parse_detail(self,response):
        html = response.body.decode("utf-8")
        meta = copy.deepcopy(response.meta)
        item = meta["item"]
        list = Selector(text=html).xpath("//div[@class='wrapper']/div[2]/ul/li").extract()
        fitting = ""
        for li in list:
            name =Selector(text=li).xpath("//div[@class='name']/text()").extract()
            fitting = fitting + name +","
        fitting = fitting[0:-1]
        item["fitting"] = fitting


        list2 = Selector(text=html).xpath("//div[@class='item']").extract()
        # for li in list2:


        logging.info("进入二级页面")
