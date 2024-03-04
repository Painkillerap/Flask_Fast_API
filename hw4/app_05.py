# Задание №5

# � Создать программу, которая будет производить подсчет количества слов
#     в каждом файле в указанной директории и выводить результаты в консоль.
# � Используйте процессы.
# -----------------------

from multiprocessing import Process
import os
from pathlib import Path
import time


def count_word(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        count = len(text.split())
    print(f"{file_path.name} содержит {count} слов")
        # return count


# -----------------------
if __name__ == '__main__':

    print("Задание 5 / Многопроцессорный")
    processes = []
    start_time = time.time()
    dir_path = Path(os.getcwd() + "/upload")  # <-- рабочая папка для работы
    file_paths = [file_path for file_path in dir_path.iterdir() if file_path.is_file()]

    for file in file_paths:
        # thread = Thread(target=count_word, args=[file])
        process = Process(target=count_word, args=[file])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек (задание 5)")