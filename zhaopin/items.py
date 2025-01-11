# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ZhaopinItem(scrapy.Item):
    name = scrapy.Field() # 职位名称
    salary = scrapy.Field() # 薪资水平
    title = scrapy.Field() # 学历
    ex = scrapy.Field() # 工作经验
    tags = scrapy.Field() # 职位标签
    company = scrapy.Field() # 公司
    company_tag = scrapy.Field() # 公司标签
    platform_id = scrapy.Field() # 平台，指招聘平台的id
    region_id = scrapy.Field() # 地区id
    job_id = scrapy.Field() # 工作id
    pass
