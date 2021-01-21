import scrapy
from scrapy.selector import Selector

class DemoSpider(scrapy.Spider):
    name = "demo_spider"
    start_urls = ['https://www.baidu.com/']
    allowed_domains = []


    custom_settings = {
        # 'LOG_FILE': logs_path + '/logs/NewsSpiderI_log.log',

        'CONCURRENT_REQUESTS': 100,
        # CONCURRENT_REQUESTS_PER_IP
        'DOWNLOAD_DELAY': 1.5,  # 自动节流器会把delay控制在DOWNLOAD_DELAY与AUTOTHROTTLE_MAX_DELAY之间的最优值
        'DOWNLOADER_MIDDLEWARES': {
            'spider_demo.middlewares.SpiderDemoDownloaderMiddleware': 543,
        },
        'SPIDER_MIDDLEWARES': {
            'spider_demo.middlewares.SpiderDemoSpiderMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'spider_demo.pipelines.SpiderDemoPipeline': 200,
        },
        'DOWNLOAD_TIMEOUT': 30,
        'RETRY_TIMES': 3,

    }

    def parse(self, response):
        print("hello world")
