"""
失败了，因为无法在headless chrome 中获取 audio，报错 element unsupported resource
"""
from pyppeteer import launch
import asyncio

path = './consequent/laoliang/'



async def here():
    browser = await launch(headless=False, autoClose=False)
    page = await browser.newPage()
    # page.on('response', handle_finish)
    await page.goto('https://open.weixin.qq.com/connect/qrconnect?appid=wxf9181b2f5d92cafa&redirect_uri=https://sss'
                    '.qingting.fm/account/wechat-passport.html&response_type=code&scope=snsapi_login&state=https'
                    '://www.qingting.fm/user#wechat_redirect')
    await page.waitForSelector('._2Z3e img')
    await page.goto('https://www.qingting.fm/channels/231968/1')
    await page.waitForSelector('._2k3q')
    links = await page.JJ('._2k3q')
    # get page range
    maxPage = await page.evaluate('(el) => el.innerText', links[-1])

    for page_index in range(int(maxPage)):
        await page.goto('https://www.qingting.fm/channels/231968/{}'.format(page_index + 1))
        links = await page.JJeval('.XT9D ._-_jo', 'nodes => nodes.map(n => n.href)')
        for link in links:
            await page.goto(link)
            await page.click('._3eC9')
            mediaResponse = await page.waitForResponse(lambda res: 'content-type' in res.headers and res.headers['content-type'] == 'audio/mpeg')
            print(await mediaResponse.status)

        # 遍历每一个链接
        """
        mediaResponse = await page.waitForResponse(lambda res: 'content-type' in res.headers and res.headers['content-type'] == 'audio/mpeg')
        print(await mediaResponse.buffer())
        """


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(here())


