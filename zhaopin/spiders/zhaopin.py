from playwright.async_api import async_playwright
import scrapy
from ..items import ZhaopinItem
from ..constant import zhilian_job_code, zhilian_region_code, cookies
from ..util.logger import ClassMethodLogging,MethodLogging,Logger
from ..util.breakpoint import ZhilianBP
from twisted.internet.threads import deferToThread
from scrapy.http import HtmlResponse

class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://www.zhaopin.com',
        },
        'COOKIES_ENABLED': True,
        'COOKIES': cookies
    }

    def __init__(self):
        super().__init__()
        self.my_logger = Logger()
        self.bp = ZhilianBP()
        self.cnt = 0
        
        # 从断点文件加载状态
        saved_state = self.bp.load_breakpoint()
        if saved_state:
            self.current_region_code = self.bp.region_code
            self.current_job_code = self.bp.job_code
            self.current_page = self.bp.page
        else:
            self.current_region_code = 0
            self.current_job_code = 0
            self.current_page = 1

    @staticmethod
    async def get_rendered_html(url):
        with async_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=False, args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ])
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
                viewport={"width": 1920, "height": 1080},
                locale="zh-CN",
                java_script_enabled=True,
            )
            page = await context.new_page()
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=60000)
                # 模拟滚动加载
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                await page.wait_for_timeout(3000)  # 等待页面渲染
                rendered_html =  page.content()
                return rendered_html
            except Exception as e:
                print(f"Error: {e}")
                return None
            finally:
                 await browser.close()

    def start_requests(self):
        # 手动使用 Twisted deferToThread 将异步操作同步化
        while self.current_region_code < len(zhilian_region_code):
            region_code = zhilian_region_code[self.current_region_code][1]

            while self.current_job_code < len(zhilian_job_code):
                job_code = zhilian_job_code[self.current_job_code][1]

                url = f'https://www.zhaopin.com/sou/{region_code}/{job_code}/p{self.current_page}'
                self.my_logger.info(f'开始爬取地区{region_code}职位{job_code}第{self.current_page}页')

                # 在一个线程中运行异步的 get_rendered_html
                deferred = deferToThread(self.get_rendered_html, url)
                deferred.addCallback(self._on_html_rendered, url)

                self.current_job_code += 1
                self.current_page = 1

            self.current_region_code += 1
            self.current_job_code = 0
            
            yield deferred

    def _on_html_rendered(self, rendered_html, url):
        if rendered_html:
            yield HtmlResponse(
                url=url,
                body=rendered_html,
                encoding='utf-8',
                request=None  # 不需要发起新请求
            )

    async def parse(self, response):
        # 使用 Playwright 渲染页面
        rendered_html =  self.get_rendered_html(response.url)
        
        if rendered_html:
            # 使用 Scrapy 解析渲染后的 HTML
            job_list = scrapy.Selector(text=rendered_html).xpath('//div[@class="joblist-box__item clearfix"]')
            if job_list:
                for job in job_list:
                    item = ZhaopinItem()
                    item['name'] = job.xpath('.//a[@class="jobinfo__name"]//text()').get(default='').strip()
                    item['salary'] = job.xpath('.//span[@class="jobinfo__salary"]//text()').get(default='').strip()
                    item['company'] = job.xpath('.//a[@class="company__name"]//text()').get(default='').strip()
                    
                    tags = job.xpath('.//div[@class="jobinfo__other-info"]//span//text()').getall()
                    item['title'] = tags[0] if len(tags) > 0 else ''
                    item['ex'] = tags[1] if len(tags) > 1 else ''
                    item['tags'] = ','.join(tags[2:]) if len(tags) > 2 else ''
                    
                    company_tags = job.xpath('.//div[@class="company__tags"]//span//text()').getall()
                    item['company_tag'] = ','.join(company_tags)
                    
                    item['platform_id'] = response.meta['region_code']
                    item['region_id'] = response.meta['job_code']
                    item['job_id'] = response.meta['page']
                    
                    self.cnt += 1
                    self.my_logger.info(f'数据{self.cnt}准备保存')
                    yield item
            else:
                self.my_logger.error('未爬取到任何职位信息')


    @ClassMethodLogging
    def close(self, reason):
        if reason == 'finished':
            self.my_logger.info('爬虫正常结束')
            self.bp.clear_breakpoint()
        else:
            self.my_logger.info(f'爬虫因{reason}关闭')