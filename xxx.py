import requests
from lxml import etree

url = 'http://www.shouhuola.com/user/answer.html'
url1 = 'http://www.shouhuola.com/user/answer/all/2.html'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'PHPSESSID=ilqobu9geu3062q6jndcmfjk84; Hm_lvt_268b203e39c04a46e95ebd118fa9138a=1608511417,1608540606,1608614917,1608770029; Hm_lpvt_268b203e39c04a46e95ebd118fa9138a=1608770213',
    'Host': 'www.shouhuola.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3776.400 QQBrowser/10.6.4212.400',
}
res = requests.get(url, headers=headers).text

html = etree.HTML(res)

href = html.xpath('//*[@id="list-container"]/div[1]/section/div[2]/h2/a/@href')
print(len(href))
for i in href:
    print(i)

