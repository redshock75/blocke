import asyncio
import os
import time

PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

from pyppeteer import launch

import nest_asyncio

nest_asyncio.apply()
# ФИКС МЕДЛЕЕЕЫЕ ЗАПРОСЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def get_check(bank, d):
    data = {
               'DOCUMENT': '4252228616',
               'SENDER_CARD': '2314',
               'RECEIVER_CARD': '2511',
               'CODE': '212251',
               'AMOUNT': '1234.13',
               'TIME': '14.10.2024 13:38',
               'SENDER_NAME': 'Алексей Андреевич Ф.',
               'RECEIVER_NAME': 'Скам Скамыч Ф.',
               'RECEIVER_NUMBER': '+7 (993) 532-49-05',
           } | d
    with open(bank + '/1.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    for key, value in data.items():
        html_content = html_content.replace(key, str(value))
    html_content = html_content.replace('$URL', 'http://127.0.0.1:5000/' + bank)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(html_to_pdf(html_content))
    return open('check.pdf', 'rb').read()


async def html_to_pdf(html_content):
    browser = await launch(handleSIGINT=False,
                           handleSIGTERM=False,
                           handleSIGHUP=False)
    pages = await browser.pages()

    page = pages[0]
    await page.setContent(html_content)

    # Set the viewport size to ensure content is rendered
    await page.setViewport({'width': 1920, 'height': 1080})

    # Wait for any asynchronous content to load
    await page.waitForSelector("#p1")
    time.sleep(2)
    # Get the dimensions of the entire page
    dimensions = await page.evaluate('''() => {
        const element = document.getElementById('p1');
        return {
            width: element.offsetWidth,
            height: element.offsetHeight
        };
    }''')

    await page.pdf({
        'title': 'чек',
        'path': 'check.pdf',
        'width': dimensions['width'],
        'height': dimensions['height'],
        'printBackground': True,
        'margin': {
            'top': '0px',
            'right': '0px',
            'bottom': '0px',
            'left': '0px'
        }
    })

    await browser.close()