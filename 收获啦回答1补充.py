#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/3 21:02
# @Author  : 卡卡
import json
import time
import requests
from lxml import etree
from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400',
}


def req(url):
    response = requests.get(url=url, headers=headers).content.decode('utf-8')
    html = etree.HTML(response)
    # with open('问题回答11.html','w',encoding='utf-8') as f:
    #     f.write(response)

    return html


def find_one(url):
    # 定义一个空列表，用来接收每页中回答数为0的问题
    lis = []
    # url = "http://www.shouhuola.com/c-17"

    response = requests.get(url=url, headers=headers)
    # print(response.content.decode('utf-8'))

    html = etree.HTML(response.content.decode('utf-8'))
    # print(html)
    num_list = html.xpath('//*[@id="body"]/div[2]/div[1]/div/div[1]/div[4]/section')
    # print(len(num_list))
    for num in num_list:
        zero_qt = num.xpath('./div[1]/div[1]/text()')[0]
        zero_str = zero_qt.strip()
        if zero_str == '1':
            # 搜索链接
            title_href = num.xpath('./div[2]/h2/a/@href')[0]
            title = num.xpath('./div[2]/h2/a/text()')[0]
            # print(zero_str,title,title_href)
            lis.append([title_href, title])
    return lis


# print(find_one())


'使用csdn网站返回相应的问题解答字符串'


def csdn_text(problem_title):
    """
    :return:   返回csdn的第一个问题回答的文字信息
    """
    # csdn_url = f'https://so.csdn.net/so/search/s.do?q={problem_title}&t=blog&o=&s=&l=&f=&viparticle='  # 博客分类链接
    # print(csdn_url)
    # csdn_html = req(csdn_url)

    # 问题的第一个回答链接 first_por_url
    # first_por_url = csdn_html.xpath('//div[@class="search-list-con"]/div/dl[3]/a/@href')[0]

    url = f'https://so.csdn.net/api/v2/search?q={problem_title}&t=blog&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&platform=pc'
    # print(url)

    href_dic = requests.get(url=url,headers=headers).json()
    href = href_dic['result_vos'][0]['url']

    # first_por_url = csdn_html.xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/div/div[1]/div/div[1]/a/@href')[0]
    # print(first_por_url)

    # 返回的搜索问题页
    response_pro = req(href)

    # with open('csdn搜索.html', 'w', encoding='utf-8') as f:
    #     f.write(html)

    # 提取问题回答页的内容
    article_list_text = response_pro.xpath('//div[@id="content_views"]//text()')

    # 去掉空格
    '换行处理没有处理成功，即使成功格式也显得难看'
    article_text_kong = [i.replace('\\n', '').replace(' ', '') for i in article_list_text]
    # article_text = ''.join(article_text_kong).replace('\n','')
    article_text = ''.join(article_text_kong)
    # print(article_text)

    lis = ['千锋','黑马','传智','兄弟连','达内','拉勾教育','CSDN','微信','微信公众号','qq群','qq','QQ']

    # 返回一个文档字符串
    for i in lis:
        if i in article_text:
            article_text = article_text.replace(i,'')

    return article_text

    # with open('问题回答.txt','w',encoding='utf-8') as f:
    #     f.write(article_text)


# 填写收获啦
def fill_in(problem_url, pro_answer):
    # 收获啦回答
    driver = webdriver.Chrome()

    driver.maximize_window()

    # 访问url
    driver.get(problem_url)

    # 点击写回答
    driver.find_element_by_xpath('//*[@id="body"]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/button[1]').click()
    time.sleep(5)

    # 出现新的界面，进行登陆

    '  zp'
    # driver.find_element_by_xpath('//*[@id="popusername"]').send_keys('xxxxxx)
    # driver.find_element_by_xpath('//*[@id="poppassword"]').send_keys('xxxxxx')

    driver.find_element_by_xpath('//*[@id="submit"]').click()
    time.sleep(5)

    # 再次单击写回答
    driver.find_element_by_xpath('//*[@id="body"]/div[2]/div[2]/div[2]/div/div[2]/div/div/div/button[1]').click()
    time.sleep(1)
    # 找到搜索框
    # inputElement = driver.find_element_by_xpath('//*[@id="verifycode"]')  # 截取搜索框元素
    # inputElement.screenshot("inputElement.png")
    # 调用查找方法，返回一段字符串
    text = pro_answer

    # driver.find_element_by_xpath('/html/body').click()
    # time.sleep(5)
    # with open('sdsd.html','w',encoding='utf-8') as fp:
    #     fp.write(driver.page_source)
    # print(driver.page_source)

    # 访页面中第一个iframe
    driver.switch_to.frame(1)

    # 将找到的内容传递上去
    driver.find_element_by_xpath('/html/body/p').send_keys(text)

    # driver.execute_script('document.getElementsByTagName("p")[0].innerHTML={}'.format(text))
    # time.sleep(5)

    # 切回原来的页面
    driver.switch_to.default_content()
    # 点击发布
    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="ajaxsubmitasnwer"]').click()

    # driver.save_screenshot('验证码.png')
    time.sleep(10)
    driver.quit()


if __name__ == '__main__':
    # for page in range(150,1,-1):
    for page in range(1,300):
        url = f'http://www.shouhuola.com/c-17/all/{page}.html'
        zero_list = find_one(url)
        for info_list in zero_list:
            problem_url = info_list[0]
            problem_title = info_list[1]
            # 有的页面执行点击会找不到点击位置，使用异常处理
            try:
                # 问题回答
                pro_answer = csdn_text(problem_title)

                # 收获啦填写
                fill_in(problem_url, pro_answer)

            # 不能成功执行点击发布的连接
            except:
                print('============================')
                print(info_list)
                with open('未解决问题网址和链接.txt', 'a', encoding='utf-8') as f:
                    f.write(str(info_list) + '\n')
                print('============================')
