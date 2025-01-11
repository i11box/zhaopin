import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

# 初始化浏览器
driver = webdriver.Edge()  # 确保您已经安装了对应的驱动
driver.get('https://www.zhaopin.com/sou/jl682/kw01500O80EO062NO0AF8G/p1')

shop_name = '职位信息'  # 请根据需要设置文件名
num_pages = 5  # 设置要爬取的页数

with open(f'{shop_name}.csv', mode='w', encoding='utf-8', newline='') as f:
    csv_writer = csv.DictWriter(f, fieldnames=['职位名称', '职位属性','经验要求'])
    csv_writer.writeheader()

    for page in range(1, num_pages + 1):
        driver.implicitly_wait(3)  # 等待页面加载
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 滚动到底部
        time.sleep(3)  # 等待加载

        # 获取所有职位列表项
        lis = driver.find_elements(By.CLASS_NAME, 'joblist-box__item clearfix')
        if not lis:
            print("未找到职位列表项，检查页面结构或调整等待时间。")
            break

        for li in lis:
            try:
                # 职位名称
                job_name = li.find_element(By.CLASS_NAME, 'jobinfo__name').text if li.find_element(By.CLASS_NAME, 'jobinfo__name') else "名称未找到"
                
                # 职位属性
                job_type = li.find_element(By.CLASS_NAME, 'jobinfo-box__item-tag').text if li.find_element(By.CLASS_NAME, 'jobinfo-box__item-tag') else "属性未找到"
                
                # 经验要求
                job_ex = li.find_elements(By.CLASS_NAME, 'jobinfo__other-info-item')[2].text if len(li.find_elements(By.CLASS_NAME, 'jobinfo__other-info-item')) > 2 else "经验要求未找到"
                
                # # 其他字段
                # job_area = li.find_element(By.CSS_SELECTOR, '.position-card__city-name').text if li.find_element(By.CSS_SELECTOR, '.position-card__city-name') else "地点未找到"
                # education = li.find_elements(By.CSS_SELECTOR, '.position-card__tags__item')[1].text if len(li.find_elements(By.CSS_SELECTOR, '.position-card__tags__item')) > 1 else "学历未找到"
                # salary = li.find_element(By.CSS_SELECTOR, '.position-card__salary').text if li.find_element(By.CSS_SELECTOR, '.position-card__salary') else "薪资未找到"
                # company_name = li.find_element(By.CSS_SELECTOR, '.position-card__company_name').text if li.find_element(By.CSS_SELECTOR, '.position-card__company_name') else "公司名称未找到"
                
                # # 公司行业、规模、性质
                # company_tabs_items = li.find_elements(By.CSS_SELECTOR, '.position-card__company__tabs-item')
                # company_industry = company_tabs_items[0].text if len(company_tabs_items) > 0 else "行业未找到"
                # company_guimo = company_tabs_items[1].text if len(company_tabs_items) > 1 else "规模未找到"
                # company_type = company_tabs_items[2].text if len(company_tabs_items) > 2 else "性质未找到"
                
                # 将数据写入CSV 文件
                csv_writer.writerow({
                    '职位名称': job_name,
                    '职位属性': job_type,
                    '地点': job_area,
                    '学历': education,
                    '薪资': salary,
                    '公司名称': company_name,
                    '公司行业': company_industry,
                    '公司性质': company_type,
                    '公司规模': company_guimo,
                    '经验要求': job_ex
                })
            except Exception as e:
                print(f"处理职位时出错: {e}")

# 关闭浏览器
driver.quit()