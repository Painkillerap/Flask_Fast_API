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


import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import time


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Извлечение изображений"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)
    return urls


def download(url, pathname):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    start_time = time.time()
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, url.split("/")[-1])
    progress = tqdm(response.iter_content(
        1024), f"Загрузка {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    try:
        with open(filename, "wb") as f:
            for data in progress.iterable:
                f.write(data)
                progress.update(len(data))
        time_list.append(
            f"Загрузка картинки {filename.replace(pathname, '')} за {time.time()-start_time:.2f} секунды")
    except FileNotFoundError:
        print('Изображение не найдено!')


def run(url):
    path = os.path.join(os.getcwd(), url.replace(
        'https://', '').replace('.', '_').replace('/', ''))
    imgs = get_all_images(url)
    start_total_time = time.time()
    for img in imgs:
        download(img, path)
    total_time = time.time() - start_total_time
    for i in range(len(time_list)):
        print(time_list[i])
    print(f"Общее время выполнения загрузки - {total_time:.2f} секунды")


time_list = []

if __name__ == "__main__":
    run('https://gb.ru/')