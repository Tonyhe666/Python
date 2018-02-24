# _*_ coding:utf-8 _*_
import requests
from bs4 import BeautifulSoup
import os

class Mzitu():
    def __init__(self):
        self.headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        self.url = 'http://www.mzitu.com/all/'

    def request(self, url):
        return requests.get(url, self.headers)

    def download_img(self,img_url, referer):
        print u"正在下载..." + img_url
        path = img_url[-17:-10]
        path = str(path).replace("/",'-')
        self.mkdir(path)
        name = img_url[-9:-4]
        is_file_exist = os.path.isfile(name + '.jpg')
        if is_file_exist:
            print name + u"存在，返回"
            return
        httpheader = self.headers
        httpheader["Referer"] = referer
        img = requests.get(img_url, headers=httpheader)
        f = open(name + '.jpg', "ab")
        f.write(img.content)
        f.close()

    def mkdir(self,path):
        path = path.strip()
        is_exist = os.path.exists(os.path.join('/Users/heliang/rafotech/mzitu', path))
        if not is_exist:
            os.makedirs(os.path.join('/Users/heliang/rafotech/mzitu', path))
            os.chdir(os.path.join('/Users/heliang/rafotech/mzitu', path))
            return True
        else:
            os.chdir(os.path.join('/Users/heliang/rafotech/mzitu', path))
            return False

    def start(self):
        start_html = self.request(self.url)
        # print start_html.text
        Soup = BeautifulSoup(start_html.text, 'lxml')
        all_a = Soup.find('div', class_='all').find_all('a')
        for a in all_a:
            href = a['href']
            html = self.request(href)
            # print html.text
            html_soup = BeautifulSoup(html.text, 'lxml')
            pagenavi = html_soup.find('div', class_='pagenavi')
            if pagenavi:
                url_a_list = pagenavi.find_all('a')[1:-1]
                for url_a in url_a_list:
                    # print url_a['href']
                    img_html = self.request(url_a['href'])
                    # print img_html.text
                    img_Soup = BeautifulSoup(img_html.text, 'lxml')
                    main_image = img_Soup.find('div', class_='main-image')
                    if main_image:
                        img_url = main_image.find('img')['src']
                        self.download_img(img_url,url_a['href'])
spider = Mzitu()
spider.start()




