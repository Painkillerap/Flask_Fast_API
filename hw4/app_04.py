# Задание №4

# � Создать программу, которая будет производить подсчет количества слов
#     в каждом файле в указанной директории и выводить результаты в консоль.
# � Используйте потоки.
# -----------------------

import os
import time
from pathlib import Path
from threading import Thread


def count_word(file_path: Path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        count = len(text.split())
    print(f"{file_path.name} содержит {count} слов")
        # return count


# -----------------------
if __name__ == '__main__':

    print("Задание 1 / Многопоточный")
    threads = []
    start_time = time.time()
    dir_path = Path(os.getcwd() + "/upload")  # <-- рабочая папка для работы
    file_paths = [file_path for file_path in dir_path.iterdir() if file_path.is_file()]

    threads = []
    for file in file_paths:
        # thread = threading.Thread(target=count_word, args=[file])
        thread = Thread(target=count_word, args=[file])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек (задание 4)")
