# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import csv

from zhaopin.util.logger import Logger

class ZhaopinPipeline:
    def __init__(self):
        # 打开文件并写入表头
        self.file = open('D:\\01 代码\\01 Python\\zhaopin\\zhaopin\\output\\output.csv', 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['name', 'salary', 'company', 'title', 'ex', 'tags', 'company_tag', 'platform_id', 'region_id', 'job_id'])
        Logger.info('Pipeline启动,文件成功打开')

    def process_item(self, item, spider):
        # 写入数据行
        self.writer.writerow([
            item.get('name'),
            item.get('salary'),
            item.get('company'),
            item.get('title'),
            item.get('ex'),
            ';'.join(item.get('tags', [])),
            ';'.join(item.get('company_tag', [])),
            item.get('platform_id'),
            item.get('region_id'),
            item.get('job_id')
        ])
        return item

    def close_spider(self, spider):
        # 关闭文件
        self.file.close()
        Logger.info('文件成功关闭')
        
