import os
import json
import csv
from datetime import datetime
from pathlib import Path
from webbrowser import get
from playwright.sync_api import sync_playwright
from zhaopin.constant import zhilian_region_code,cookies,get_job_code
import scrapy
from scrapy.selector import Selector

# 设定爬取的职位代码
zhilian_job_code = get_job_code('房地产/建筑')

class ZhaopinItem:
    def __init__(self):
        self.name = ''
        self.salary = ''
        self.title = ''
        self.ex = ''
        self.tags = ''
        self.company = ''
        self.company_tag = ''
        self.platform_id = ''
        self.region_id = ''
        self.job_id = ''
        self.location = ''

    def __setitem__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            raise KeyError(f"Key '{key}' not found in ZhaopinItem.")

    def __getitem__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise KeyError(f"Key '{key}' not found in ZhaopinItem.")

    def to_dict(self):
        return {
            'name': self.name,
            'salary': self.salary,
            'title': self.title,
            'ex': self.ex,
            'tags': self.tags,
            'company': self.company,
            'company_tag': self.company_tag,
            'platform_id': self.platform_id,
            'region_id': self.region_id,
            'job_id': self.job_id,
            'location': self.location
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

# 转换为 Playwright 格式的 Cookies 列表
def format_cookies_for_playwright(raw_cookies, domain):
    cookies_list = []
    for name, value in raw_cookies.items():
        cookies_list.append({
            "name": name,
            "value": value,
            "domain": domain,  # 需要替换为实际域名
            "path": "/",       # 通常路径为 "/"
        })
    return cookies_list

def get_ignore_list():
    ignore_list = set()  # 使用 set 加速查找
    data_folder = "datas_fangdichan"
    
    # 遍历数据文件夹及其所有子文件夹中的文件
    for root, _, files in os.walk(data_folder):
        for file_name in files:
            try:
                # 从文件名中解析 region_code, job_code 和 page
                if file_name.endswith(".json"):  # 只处理 .json 文件
                    base_name, _ = os.path.splitext(file_name)  # 去掉扩展名
                    region_code, job_code, page = base_name.split('_', maxsplit=2)
                    
                    # 添加到 ignore_list
                    ignore_list.add((region_code, job_code, str(page)))
            except ValueError as ve:
                print(f"错误: 文件 '{file_name}' 名称无法解析为有效的 region_code, job_code 和 page.")
                print(ve)
                continue
    
    return ignore_list
def get_rendered_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            java_script_enabled=True,
        )
        if cookies:
            context.add_cookies(cookies = format_cookies_for_playwright(cookies, domain="www.zhaopin.com"))
        page = context.new_page()
        try:
            page.goto(url, wait_until='networkidle', timeout=60000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.wait_for_timeout(1800)
            return page.content()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            browser.close()

def extract_job_data(rendered_html):
    job_list = Selector(text=rendered_html).xpath('//div[@class="joblist-box__iteminfo"]')
    job_items = []
    
    if job_list:
        for job in job_list:
            item = ZhaopinItem()
            item['name'] = job.xpath('.//a[contains(@class, "jobinfo__name")]//text()').get(default='').strip()
            item['salary'] = job.xpath('.//p[contains(@class, "jobinfo__salary")]//text()').get(default='').strip()
            tags = job.xpath('.//div[contains(@class, "jobinfo__tag")]//text()').getall()
            item['tags'] = ','.join(tag.strip() for tag in tags if tag.strip())
            item['company'] = job.xpath('.//a[contains(@class, "companyinfo__name")]//text()').get(default='').strip()
            company_tags = job.xpath('.//div[@class="companyinfo__tag"]//text()').getall()
            item['company_tag'] = ','.join(tag.strip() for tag in company_tags if tag.strip())
            item['location'] = job.xpath('.//div[@class="jobinfo__other-info-item"]//span/text()').get(default='').strip()
            item['ex'] = job.xpath('.//div[@class="jobinfo__other-info-item"][2]//text()').get(default='').strip()
            item['title'] = job.xpath('.//div[@class="jobinfo__other-info-item"][3]//text()').get(default='').strip()
            item['platform_id'] = 'some_region_code'
            item['region_id'] = 'some_job_code'
            item['job_id'] = 'some_page_id'
            job_items.append(item)
    return job_items

def save_to_json(job_items, region_sn, job_sn, page):
    # 生成保存的文件夹和文件名
    folder_name = f"datas_fangdichan"
    os.makedirs(folder_name, exist_ok=True)
    filename = os.path.join(folder_name, f"{zhilian_region_code[region_sn][1]}_{zhilian_job_code[job_sn][1]}_{page}.json")

    with open(filename, 'a', encoding='utf-8') as file:
        for item in job_items:
            json.dump(item.to_dict(), file, ensure_ascii=False, indent=4)
            file.write('\n')

    print(f"数据已保存到 {filename}")

def save_breakpoint(region_sn, job_sn, page, breakpoint_file="breakpoint.json"):
    breakpoint_data = {
        'region_sn': region_sn,
        'job_sn': job_sn,
        'page': page
    }
    with open(breakpoint_file, 'w', encoding='utf-8') as file:
        json.dump(breakpoint_data, file, ensure_ascii=False, indent=4)
    print("断点已保存")

def load_breakpoint(breakpoint_file="breakpoint.json"):
    if Path(breakpoint_file).exists():
        with open(breakpoint_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None

# 主逻辑
def main():
    choice = input("请输入1或2：\n1. 继续上次断点\n2. 从头开始\n")
    if choice == '1':
        # 读取断点信息，如果存在就从断点处继续
        breakpoint = load_breakpoint()
    
        region_sn = breakpoint['region_sn'] if breakpoint else 0
        job_sn = breakpoint['job_sn'] if breakpoint else 0
        page = breakpoint['page'] if breakpoint else 1
    else:
        region_sn = 0
        job_sn = 0
        page = 1

    base_url = "https://www.zhaopin.com/sou/"

    ignore_list = get_ignore_list()

    try:
        for region_sn in range(0, len(zhilian_region_code)):
            for job_sn in range(0, len(zhilian_job_code)):
                for page in range(1, 11):
                    if (zhilian_region_code[region_sn][1], zhilian_job_code[job_sn][1], str(page)) in ignore_list:
                        print(f"跳过已忽略的地区：{zhilian_region_code[region_sn][1]},职位：{zhilian_job_code[job_sn][1]},页码：{page}")
                        continue
                    
                    url = base_url + zhilian_region_code[region_sn][1] + "/" + zhilian_job_code[job_sn][1] + "/p" + str(page)
                    rendered_html = get_rendered_html(url)

                    if rendered_html:
                        job_items = extract_job_data(rendered_html)
                        if job_items:
                            save_to_json(job_items, region_sn, job_sn, page)
                            print(f"第 {region_sn} 个地区，第 {job_sn} 个职位，第 {page} 页数据抓取完成")
                        else:
                            print(f"第 {region_sn} 个地区，第 {job_sn} 个职位，第 {page} 页无数据")
                    else:
                        print(f"第 {region_sn} 个地区，第 {job_sn} 个职位，第 {page} 页抓取失败")
                        save_breakpoint(region_sn, job_sn, page)
                        return  # 出现错误时保存断点并退出
    except Exception as e:
        print(f"发生异常: {e}")
        save_breakpoint(region_sn, job_sn, page)

if __name__ == '__main__':
    main()
    
