# Задание №2

# � Написать программу, которая считывает список из 10 URL-адресов и одновременно
#    загружает данные с каждого адреса.
# � После загрузки данных нужно записать их в отдельные файлы.
# � Используйте процессы.
# -----------------------

import time
from multiprocessing import Process
from pathlib import Path

import requests

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


def download(url, start_time):
    response = requests.get(url)
    filename = 'task_2_process_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    Path(Path.cwd() / 'upload').mkdir(exist_ok=True)
    with open(f"./upload/{filename}", "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Загрузка {url} составила {time.time() - start_time:.2f} сек (задание 2)")


# -----------------------
if __name__ == '__main__':

    print("Задание 2 / Многопроцессорный")
    processes = []
    start_time = time.time()

    for url in urls:
        process = Process(target=download, args=(url, start_time))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек (задание 2)")
