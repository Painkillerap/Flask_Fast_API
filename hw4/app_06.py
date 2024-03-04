# Задание №6

# � Создать программу, которая будет производить подсчет количества слов
#     в каждом файле в указанной директории и выводить результаты в консоль.
# � Используйте асинхронный метод.
# -----------------------

import asyncio
import os
from pathlib import Path
import time


async def count_word(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        count = len(text.split())
    # print(f"{file_path.name} содержит {count} слов")
        return count


async def count_directory(file_paths):
    for file in file_paths:
        print(file.name, await count_word(file))


# -----------------------
if __name__ == '__main__':
    print("Задание 6 / Асинхронный")
    start_time = time.time()
    dir_path = Path(os.getcwd() + "/upload")  # <-- рабочая папка для работы
    file_paths = [file_path for file_path in dir_path.iterdir() if file_path.is_file()]

    asyncio.run(count_directory(file_paths))

    print(f"Полное завершение работы: {time.time() - start_time:.2f} сек (задание 6)")