# Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
#  Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
#  Программа должна использовать многопоточный, многопроцессорный и
# асинхронный подходы.
#  Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
#  Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.


import load_images
import asyncio
import aiohttp
import time
import os


async def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.read()
            start_time = time.time()
            filename = os.path.join(pathname, url.split("/")[-1])
            try:
                with open(filename, "wb") as f:
                    f.write(img)
                print(f"Загрузка картинки {filename.replace(pathname, '')} за {time.time() - start_time:.2f} секунды")
            except FileNotFoundError:
                print('Изображение не найдено!')


start_total_time = time.time()


async def main(url):
    tasks = []
    path = os.path.join(os.getcwd(), url.replace('https://', '').replace('.', '_').replace('/', ''))
    imgs = load_images.get_all_images(url)
    for img in imgs:
        task = asyncio.create_task(download(img, path))
        tasks.append(task)
    await asyncio.gather(*tasks)
    total_time = time.time() - start_total_time
    print(f"Общее время выполнения загрузки - {total_time:.2f} секунды")


if __name__ == "__main__":
    asyncio.run(main('https://gb.ru/'))
