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
from multiprocessing import Process
import time
import os

processes = []


def run(url):
    path = os.path.join(os.getcwd(), url.replace('https://', '').replace('.', '_').replace('/', ''))
    imgs = load_images.get_all_images(url)
    start_total_time = time.time()
    for img in imgs:
        process = Process(target=load_images.download, args=(img, path))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    total_time = time.time() - start_total_time
    for i in range(len(load_images.time_list)):
        print(load_images.time_list[i])
    print(f"Общее время выполнения загрузки - {total_time:.2f} секунды")


if __name__ == "__main__":
    run('https://gb.ru/')

