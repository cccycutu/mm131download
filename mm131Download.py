import requests
import os
from bs4 import BeautifulSoup


# https://www.mm131.net/xinggan/{htmlMark}.html
def getHtml(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
               "Referer": "https://www.mm131.net"
               }
    html = requests.get(url, headers=headers)
    html.encoding = html.apparent_encoding
    return html


def getSoup(html):
    return BeautifulSoup(html.text, "html.parser")


def getTitle(soup):
    title = soup.title.contents[0]
    return str(title)


def getAllPage(soup):
    allPage = soup.select('body > div.content > div.content-page > span:nth-child(1)')[0].string[1:-1]
    return allPage


def makedir(title):
    try:
        os.mkdir(title)
    except:
        print(f"提示：{title}文件夹已存在")
        # print(f"{title} folder is exist!")
        return


def downloadPic(title, allPage, htmlMark):
    print(f"当前下载: {htmlMark + ' ' + title[0:-14]} 共{allPage}张")
    for number in range(1, int(allPage) + 1):
        picUrl = f"https://img1.hnllsy.com/pic/{htmlMark}/{number}.jpg"
        pic = getHtml(picUrl)
        with open(f"{title[0:-14]}/{number}.jpg", "wb+") as f:
            f.write(pic.content)
            print(f"下载进度:{number}/{allPage}")
            # print(f"{number}.jpg download successful!")
    print(f"{htmlMark} {title[0:-14]} 下载完成！\n")
    text_create(f'{title[0:-14]}/url.txt', f"https://www.mm131.net/xinggan/{htmlMark}.html")


def text_create(name, msg):
    file = open(name, 'w')
    file.write(msg)
    file.close()


def main():
    list1 = []
    for mark in list1:
        htmlMark = str(mark)
        try:
            html = getHtml(f"https://www.mm131.net/xinggan/{htmlMark}.html")
            soup = getSoup(html)
            title = getTitle(soup)
            allPage = getAllPage(soup)
            makedir(f"{title[0:-14]}")
        except:
            # continue
            print('fail')
        # print('done')
        downloadPic(title, allPage, htmlMark)


if __name__ == '__main__':
    main()
