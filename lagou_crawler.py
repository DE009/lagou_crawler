import random
import time
from time import sleep

import brotli
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import model
import sql


class Lagou():
    def __init__(self, driver_data_dir):
        self.baseurl = "https://www.lagou.com/" #网站主页
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'user_trace_token=20230515214657-e1721655-c00c-4e9f-bf47-c0ac4162a864; _ga=GA1.2.2004737564.1684158420; LGUID=20230515214658-e10a2f7e-58f6-4667-9ebb-778ab8e615f8; LG_HAS_LOGIN=1; hasDeliver=0; privacyPolicyPopup=false; RECOMMEND_TIP=true; index_location_city=%E4%B8%8A%E6%B5%B7; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; _gid=GA1.2.365109600.1684720575; __SAFETY_CLOSE_TIME__26121529=1; __lg_stoken__=9b569ec6b5f5320913befb61d30deade6d07fd5e1d33a116ad9386b90abbe2a76c4eb706c5bd6d538659ad80567aa120d7128664a3b6a8fb4dad3012cda060a81d0dee68b0c1; gate_login_token=v1####9ff717c8a0ab7cc5101c4c429c6c9da3cc897df14c36f28081d27bed45150b59; LG_LOGIN_USER_ID=v1####07b4772a074b526c4baec8da5a3f3401335f85ec4b50c4cc0665bc092c0c190f; WEBTJ-ID=20230522175808-18842e512ae163-0f4aec658608b8-26031a51-2073600-18842e512b015d; JSESSIONID=ABAAAECABIEACCA7758FCB28A237B52AC1C71C7957C8310; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1684720575,1684749490; sensorsdata2015session=%7B%7D; X_MIDDLE_TOKEN=5f15487e973cf94893ae7c85aa5b80a4; _putrc=F7DE079F1E16ED89123F89F2B170EADC; login=true; unick=%E5%BE%90%E7%90%86%E9%BE%99; X_HTTP_TOKEN=1344f2cedc091d81798257486170f7f69d1ff8d114; SEARCH_ID=d27f546533f8491fb4e5b70848bf9c6b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2226121529%22%2C%22first_id%22%3A%221881fab311066b-002a8df8576d1a-26031a51-2073600-1881fab3111666%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22113.0.0.0%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22%24device_id%22%3A%221881fab311066b-002a8df8576d1a-26031a51-2073600-1881fab3111666%22%7D; LGRID=20230522185839-e64000de-63f3-4099-b4ea-b014c2ff4593; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1684753120',
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            # 'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
        }
        self.Cookies = {}
        # self.Cookies = {'user_trace_token': '20230515214657-e1721655-c00c-4e9f-bf47-c0ac4162a864',
        #                 '_ga': 'GA1.2.2004737564.1684158420',
        #                 'LGUID': '20230515214658-e10a2f7e-58f6-4667-9ebb-778ab8e615f8', 'LG_HAS_LOGIN': '1',
        #                 'hasDeliver': '0', 'privacyPolicyPopup': 'false', 'RECOMMEND_TIP': 'true',
        #                 'index_location_city': '%E4%B8%8A%E6%B5%B7', 'showExpriedIndex': '1',
        #                 'showExpriedCompanyHome': '1', 'showExpriedMyPublish': '1',
        #                 '_gid': 'GA1.2.365109600.1684720575', '__SAFETY_CLOSE_TIME__26121529': '1',
        #                 '__lg_stoken__': '9b569ec6b5f5320913befb61d30deade6d07fd5e1d33a116ad9386b90abbe2a76c4eb706c5bd6d538659ad80567aa120d7128664a3b6a8fb4dad3012cda060a81d0dee68b0c1',
        #                 'gate_login_token': 'v1####9ff717c8a0ab7cc5101c4c429c6c9da3cc897df14c36f28081d27bed45150b59',
        #                 'LG_LOGIN_USER_ID': 'v1####07b4772a074b526c4baec8da5a3f3401335f85ec4b50c4cc0665bc092c0c190f',
        #                 'WEBTJ-ID': '20230522175808-18842e512ae163-0f4aec658608b8-26031a51-2073600-18842e512b015d',
        #                 'JSESSIONID': 'ABAAAECABIEACCA7758FCB28A237B52AC1C71C7957C8310',
        #                 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1684720575,1684749490',
        #                 'sensorsdata2015session': '%7B%7D', 'X_MIDDLE_TOKEN': '5f15487e973cf94893ae7c85aa5b80a4',
        #                 '_putrc': 'F7DE079F1E16ED89123F89F2B170EADC', 'login': 'true',
        #                 'unick': '%E5%BE%90%E7%90%86%E9%BE%99',
        #                 'X_HTTP_TOKEN': '1344f2cedc091d81798257486170f7f69d1ff8d114',
        #                 #'SEARCH_ID': 'd27f546533f8491fb4e5b70848bf9c6b',
        #                 'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2226121529%22%2C%22first_id%22%3A%221881fab311066b-002a8df8576d1a-26031a51-2073600-1881fab3111666%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%22113.0.0.0%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%2C%22%24device_id%22%3A%221881fab311066b-002a8df8576d1a-26031a51-2073600-1881fab3111666%22%7D',
        #                 'LGRID': '20230522185839-e64000de-63f3-4099-b4ea-b014c2ff4593',
        #                 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1684753120'}
        # self.proxies = {
        # }
        # 定义浏览器数据文件
        self.driver_data_dir = driver_data_dir

        # 构造数据库操作类
        self.job_dal = sql.JobDAL(model.Job())
        self.company_dal = sql.CompanyDAL(model.Company())
        self.review_dal = sql.ReviewDAL(model.Review())

    def _get_cookies(self):
        '''
        get cookies using selenium
        auto update self.Cookie
        Returns:
        '''
        print(self.Cookies)
        if self.Cookies != {}:
            return

        url = "https://www.lagou.com/"
        driver = self._get_driver()
        driver.get("https://passport.lagou.com/login/login.html")
        while True:
            print("Please login in lagou.com!", driver.current_url)
            sleep(3)
            # 成功登陆后，为request保存用户cookie，更新self.Cookies
            if driver.current_url == url:
                Cookies = driver.get_cookies()
                for k in Cookies:
                    self.Cookies.update({k['name']: k['value']})
                driver.close()
                break
        print(self.Cookies)

    # 创建selenium，driver对象
    def _get_driver(self):
        '''
        create a new selenium driver object with params
        Returns:
            driver :selenium driver object

        '''
        # 初始化selenium的driver，并能独立保存数据，持久化保存cookie，方便之后过反爬验证。
        service = Service('.\\chromedriver_win32\\chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.service = service
        options.add_argument("--user-data-dir=" + self.driver_data_dir)
        options.add_argument(f"--profile-directory=" + "Profile 2")
        driver = webdriver.Chrome(options=options)
        return driver

    def pass_verfication(self, url):
        '''
        using selenium simulate human behavior to pass crawler detection
        get the cookie returned for the next request
        update self.Cookies after get cookies
        Args:
            url (): the url that is being crawled now

        Returns:

        '''
        driver = self._get_driver()
        driver.get(url)
        while True:
            sleep(2)
            if driver.current_url == url or driver.current_url == self.baseurl:
                Cookies = driver.get_cookies()
                driver.close()
                break
            elif "verify" in driver.current_url:
                print("请手动过验证")
        for k in Cookies:
            print({k['name']: k['value']})
            self.Cookies.update({k['name']: k['value']})
        print(self.Cookies)

    # 返回所有具体岗位类别的首页urls，保存数据，并返回【类别id，url】
    def get_job_title_urls(self):
        '''
        Start from self.baseurl
        get job category infor and the corresponding category web url
        Write category infor to sql with DAL object

        Returns:
            job_title_urls() : list contain dict elements, each element contain job category_id in sql and the corresponding category web url
        '''
        content = self.get_pages(self.baseurl)
        result = []
        #从网页中获取需要的内容
        for category in [content.select('.menu_box')[0]]:   #这里只取了第一个category，若有需要可获取所有
            # categorys.append(category)
            # 遍历所有的子类以及具体的工作title
            for sub_category in category.select('.menu_sub>dl'):
                for job_title in sub_category.select('dd>a'):
                    if len(result) >= 20:
                        break
                    row = {}
                    row['category'] = category.select('.menu_main>.category-list>h2')[0].text.strip()
                    row['sub_category'] = sub_category.select('dt span')[0].text
                    row['job_title'] = job_title.select('h3')[0].text
                    row['jor_title_url'] = job_title['href']
                    if '其他' in row['job_title'] or '其它' in row['job_title']:
                        continue
                    result.append(row)
        # 写入数据库
        category_sql = sql.CategoryList(result)
        job_title_urls = category_sql.write_to_sql()
        return job_title_urls

    # 返回所有岗位类别下，所有岗位招聘信息的页面urls(默认只取1页，否则数据太多，时间太长，且增加反爬识别风险）
    def get_job_urls(self, job_title_urls, get_all=False, page_num=1):
        '''
        Get job detail web pages' urls and return
        Args:
            job_title_urls ():  list > dict { category_id : url }
            get_all (): whether to get data in  all pages exist in website
            page_num (): set the number of pages you want to crawl

        Returns:
            job_urls(): list contain dict elements, each element contain job category_id in sql and the job detail page's url under this category
        '''
        title_page_urls = []
        for title_url in job_title_urls:
            if get_all:
                # 从首页获取总页数
                first_soup = self.get_pages([title_url['job_title_url']])[0]
                page_num = first_soup.select('.totalNum')[0].text
            for page in range(1, int(page_num) + 1):
                row = {}
                row['category_id'] = title_url['category_id']
                row['title_page_url'] = title_url['job_title_url']  # + str(page)
                title_page_urls.append(row)
            print('title:{0} 下的所有页面urls获取完成'.format(title_url))
        print("完成所有title下，所有页面urls获取。")
        print('获取所有job的页面url')
        job_urls = []
        session = requests.session()
        for i in range(len(title_page_urls)):
            # 没两次，模拟过一次反爬验证
            if i % 2 == 0:
                self.pass_verfication(title_page_urls[i]['title_page_url'])

            print(title_page_urls[i]['title_page_url'])
            # 访问获取数据,获取一个job_title下，page中的内容，提取出所有岗位的内容
            job_urls_per_page = session.get(title_page_urls[i]['title_page_url'], headers=self.headers,
                                            cookies=self.Cookies)  # .select('.position_link')
            # 获取中间cookie：SEARCH_ID，用于下次访问（反爬功能）
            cookies = requests.utils.dict_from_cookiejar(job_urls_per_page.cookies)
            self.Cookies.update(cookies)
            print(cookies)
            print(self.Cookies)
            # 转为soup对象，提取岗位页面url
            job_urls_per_page = BeautifulSoup(job_urls_per_page.text, 'html5lib')
            print(job_urls_per_page)
            job_urls_per_page = job_urls_per_page.select('.position_link')
            print("已完成第{0}个title下job_url获取".format(i))
            #遍历存储当前page下的所有岗位url
            for job_page_url in job_urls_per_page:
                row = {
                    'category_id': title_page_urls[i]['category_id'],
                    'url': job_page_url['href']
                }
                job_urls.append(row)
            #随机等待，防止反爬
            time.sleep(random.randint(8, 15))

        return job_urls

    # 从岗位详情页面，获取岗位具体信息
    def get_job_data(self, soup, company_id, category_id):
        '''
        get job detail infor and write to sql , withe company id and category id as secondary index
        return job's id in sql (as secondary index in review sql )
        Args:
            soup ():  soup object generated with job detail page's content
            company_id ():  job's company's id in sql   (as a index )
            category_id (): job's category's id in sql  (as a index )

        Returns:
            job_id(): job's id in sql (as a index )

        '''
        job_name = soup.select('.position-head-wrap-position-name')[0].text
        salary = soup.select('.salary')[0].text
        job_request = soup.select('.job_request>h3>span')
        exp_req = job_request[1].text.replace('/', '').strip()
        edu_req = job_request[2].text.replace('/', '').strip()
        job_type = job_request[4].text.replace('/', '').strip()
        job_category = soup.select('.position-category-wrapper>.text')[0].text.replace('/', '').strip()
        labels = ';'.join([x.text for x in soup.select('.position-label>li')])
        detail = soup.select('.job_detail')
        job_advantage = detail[0].select('.job-advantage>p')[0].text
        job_desc = ''.join([x.text.replace('\n', '').replace('\t', '') for x in detail[0].select('.job-detail')])
        job_addr = ''.join([x.text.replace('\n', '').replace('\t', '') for x in detail[0].select('.work_addr>*')][:-1])
        print(job_name, salary, exp_req, edu_req, job_type, job_category, labels, job_advantage, job_desc, job_addr)
        job = model.Job(job_name, salary, exp_req, edu_req, job_type, job_category, labels, job_advantage, job_desc,
                        job_addr, company_id, category_id)
        self.job_dal.model = job
        job_id = self.job_dal.write_to_sql()
        return job_id

    # 从岗位具体页面，获取岗位评论信息
    def get_review_data(self, soup, job_id):
        '''
        Get job reviews in job detail pages , write to sql with job_id
        Args:
            soup (): soup object generated with job detail page's content
            job_id ():  job's id in sql (as a index )

        Returns:

        '''
        reviews = soup.select('.reviews-area>ul>li')
        for review in reviews:
            iden_desc = len(review.select('li')[0].select('.stars>i'))
            interviewer = len(review.select('li')[1].select('.stars>i'))
            company_env = len(review.select('li')[2].select('.stars>i'))
            tags = ';'.join([x.text.replace('\n', '').replace('\t', '') for x in review.select('.review-tags>.tag')])
            review_content = ';'.join(
                [x.text.replace('\n', '').replace('\t', '') for x in review.select('.review-content >div')])
            print(iden_desc, interviewer, company_env, tags, review_content)
            review_model = model.Review(iden_desc, interviewer, company_env, tags, review_content, job_id)
            self.review_dal.model = review_model
            self.review_dal.write_to_sql()

    # 从岗位详情页，获取岗位对应公司信息
    def get_company_data(self, soup):
        '''
        Get company infor from job detail pages ,write to sql
        return company 's id in sql (  as a  secondary index in job sql)
        Args:
            soup (): soup object generated with job detail page's content

        Returns:
            company_id():

        '''
        company_name = soup.select('.fl-cn')[0].text
        company_feature = soup.select('.c_feature')[0]
        bussiness_scope = company_feature.select('.icon-glyph-fourSquare')[0].next.next.text
        company_stage = company_feature.select('.icon-glyph-trend')[0].next.next.text
        company_scale = company_feature.select('.icon-glyph-figure')[0].next.next.text
        print(company_feature.select('.icon-glyph-home')[0].next.next)
        company_homepage = company_feature.select('.icon-glyph-home')[0].next['href']
        print(company_name, bussiness_scope, company_stage, company_scale, company_homepage)
        company = model.Company(company_name, bussiness_scope, company_stage, company_scale, company_homepage)
        self.company_dal.model = company
        company_id = self.company_dal.write_to_sql()
        return company_id

    # 封装的爬取网页，返回soup对象或response对象。
    def get_pages(self, url, soup=True):
        '''

        Args:
            url ():  page's url that will be crawled
            soup ():  whether return a soup object or a raw response object

        Returns:
            data(): data get from page, either a soup object or a response object
        '''
        print("爬取页面：", url)
        res = requests.get(url, headers=self.headers, cookies=self.Cookies, allow_redirects=True)
        if res.headers.get('Content-Encoding') == 'br':
            data = brotli.decompress(res.content)
        else:
            res.encoding = res.apparent_encoding
            data = res.text
        if soup:
            data = BeautifulSoup(data, 'html5lib')
        else:
            data = res
        # list
        return data

    def run(self):
        '''
        as a main func , run the whole crawler
        Returns:

        '''
        self._get_cookies()
        job_title_urls = self.get_job_title_urls()
        job_urls = self.get_job_urls(job_title_urls)
        print(job_urls)
        count = 0
        for url in job_urls:
            try:
                if count % 2 == 0:
                    self.pass_verfication(url['url'])
                count += 1
                print('当前爬取进度[{0}/{1}]'.format(count,len(job_urls)))
                job_content = self.get_pages(url['url'])
                company_id = self.get_company_data(job_content)
                job_id = self.get_job_data(job_content, company_id, url['category_id'])
                self.get_review_data(job_content, job_id)
                time.sleep(random.randint(8, 15))
            except Exception as e:
                print("发生错误：", e)


browser_data_dir = "C:\\Users\\19536\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
test = Lagou(browser_data_dir)
test.run()
