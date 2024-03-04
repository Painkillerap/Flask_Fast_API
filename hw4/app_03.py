# Задание №3

# � Написать программу, которая считывает список из 10 URL-адресов и одновременно
#    загружает данные с каждого адреса.
# � После загрузки данных нужно записать их в отдельные файлы.
# � Используйте асинхронный подход.
# -----------------------

import asyncio
import time
from pathlib import Path

import aiohttp

Path(Path.cwd() / 'upload').mkdir(exist_ok=True)

urls = ['https://gb.ru/',
        'https://google.com',
        'https://yandex.ru',
        'https://python.org',
        'https://mail.ru',
        'https://stepik.org',
        'https://vk.com',
        'https://yahoo.com',
        'https://pikabu.ru',
        'https://codelessons.ru',
        ]


async def download(url,start_time):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
    filename = 'task_3_async_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    Path(Path.cwd() / 'upload').mkdir(exist_ok=True)
    with open(f"./upload/{filename}", "w", encoding='utf-8') as f:
        f.write(text)
    print(f"Загрузка {url} составила {time.time() - start_time:.2f} сек (задание 1)")


async def main():
    task = []
    for url in urls:
        task.append(asyncio.create_task(download(url, start_time)))
    await asyncio.gather(*task)


# -----------------------
if __name__ == '__main__':
    print("Задание 3 / Асинхронный")
    start_time = time.time()

    asyncio.run(main())

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек (задание 3)")
