import json
import pymongo
from selenium import webdriver
from urllib.parse import urlencode

name=0
def save_to_mongo(result):
    MONGO_TABLE = 'toutiao'
    MONGO_DB='localhost'
    client = pymongo.MongoClient(MONGO_DB)
    db = client[MONGO_TABLE]
    if db['今日头条图片'].insert(result):
        print('存储内容：',result)

def get_page_index(offset):
    data={
		"aid": "24",
		"app_name": "web_search",
		"offset": offset,
		"format": "json",
		"keyword": "街拍",
		"autoload": "true",
		"count": "20",
		"en_qc": "1",
		"cur_tab": "1",
		"from": "search_tab",
		"pd": "synthesis",
		"timestamp": "1580559421609"
	}
    url='https://www.toutiao.com/api/search/content/?'+urlencode(data)
    print(url)
    browser=webdriver.Firefox()
    '''
    今天头条的内容是ajax动态加载的，因此要保持会话，否者打开的json网页会没有想要的内容。
    保持第一个referce窗口不关闭。
    '''
    browser.get('https://www.toutiao.com')#打开第一个窗口
    browser.implicitly_wait(2)#显示等待
    browser.execute_script('window.open()')#执行js代码,打开另外一个窗口
    #print(browser.window_handles)
    browser.switch_to.window(browser.window_handles[1])#转到第二个窗口（句柄）
    browser.get(url)#ajax网页
    response=browser.find_element_by_id('json')
    return response.text

def parse_page_index(html):
    data=json.loads(html)
    if 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    browser = webdriver.Firefox()
    browser.get(url)
    imgs = browser.find_elements_by_tag_name('img')
    global name
    dic={}
    for img in imgs:
        if img.get_attribute('src'):
            dic[str(name)]=img.get_attribute('src')
            name=name+1
        if img.get_attribute('href'):
            dic[str(name)]=img.get_attribute('href')
            name=name+1
    return dic
def main(offset):
    html=get_page_index(offset)
    for url in parse_page_index(html):
        if url==None:
            print('url=None')
        else:
            img=get_page_detail(url)
            save_to_mongo(img)

if __name__ == '__main__':
    page=2#爬取页数
    for offset in range(page):
        main(offset)


