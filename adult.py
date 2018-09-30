import asyncio
import os
import re
import multiprocessing
from multiprocessing import cpu_count

from pyppeteer import launch
import requests
from pyquery import PyQuery as pq

# todo 多进程

sao_url = 'https://www.dj666666.com/saomai----55----1.html'
cuimian_url = 'https://www.dj666666.com/ziweicunmian----56----1.html'

tast_dict = []
run_dict = []

def main(url, dict):
    home_r = requests.get(url)
    doc = pq(home_r.text)

    for nav_page in doc('.page_link a')[1:-1]:
        nav_page_r = requests.get(pq(nav_page).attr('href'))
        page_doc = pq(nav_page_r.text)
        for mname in page_doc('.mname').items():
            # 加入多进程
            tast_dict.append((mname.attr('href'), dict))


def tast(args):
    for arg in args:
        asyncio.get_event_loop().run_until_complete(download(arg[0], arg[1]))


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


async def download(url, dict):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector('#myMusic')
    music_url = await page.Jeval('#myMusic', 'el => el.getAttribute("src")')
    music_r = requests.get(music_url)
    parentDir = './consequent/' + dict
    path = parentDir + '/' + validateTitle(await page.Jeval('.player h1', 'el => el.innerText')) + '.m4a'
    if not os.path.isdir(parentDir):
        os.makedirs(parentDir)

    with open(path, 'wb') as f:
        f.write(music_r.content)
        f.close()

    print('done')

if __name__ == '__main__':
    main(sao_url, 'sao')
    main(cuimian_url, 'cuimian')
    cpu_number = cpu_count()
    run_dict = [[] for i in range(cpu_number)]
    for index, value in enumerate(tast_dict):
        run_dict[index % 4].append(value)

    for i in range(cpu_number):
        p = multiprocessing.Process(target=tast, args=(run_dict[i],))
        p.start()

