import scrapy
from scrapy.selector import Selector

class DemoSpider(scrapy.Spider):
    name = "demo_spider"
    start_urls = ['https://www.baidu.com/']
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
