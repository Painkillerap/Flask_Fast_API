# Задание №7 - Домашнее задание

# Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
# Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# Массив должен быть заполнен случайными целыми числами от 1 до 100.
# При решении задачи нужно использовать многопоточность, многопроцессорность и асинхронность.
# В каждом решении нужно вывести время выполнения вычислений.

from threading import Thread  # <- многопоточность
from multiprocessing import Process  # <- многопроцессорность
import asyncio  # <- асинхронность

import random
import multiprocessing
import time

COUNT = 10_000_000  # количество чисел
PROCESS_NUM = 16  # количество потоков/процессов

summ_thread = []  # список для записи сумм для многопоточности
summ_process = multiprocessing.Value('i', 0)  # переменная для записи сумм при многопроцессорности
summ_async = []  # список для записи сумм для асинхронности


# создание списка случайных чисел от 1 до 100
def create_list(count):
    list_num = []
    for i in range(count):
        list_num.append(random.randint(1, 100))
    return list_num


# создание списка индексов срезов исходного списка на заданное кол-во потоков/процессов
# (procs - количество запускаемых потоков или процессов)
def create_index_list(procs):
    sizeSegment = COUNT // procs  # кол-во элементов в одном потоке/процессе
    index_list = []  # список срезов списка для потоков/процессов
    index_start = 0
    for i in range(procs):
        if i < (procs - 1):
            index_list.append([index_start, index_start + sizeSegment - 1])
            index_start += sizeSegment
        else:
            index_list.append([index_start, COUNT - 1])
    return index_list


# простой подсчет чисел в списке
def summ_func(list_num):
    summ = 0
    for i in list_num:
        summ += i
    return summ


# подсчет чисел в списке для многопоточности
def summ_thread_func(list_num):
    summ = 0
    for i in list_num:
        summ += i
    summ_thread.append(summ)


# подсчет чисел в списке для многопроцессорности
def summ_process_func(list_num, summ_proc):
    summ = 0
    for i in list_num:
        summ += i
    with summ_proc.get_lock():
        summ_proc.value += summ


# подсчет чисел в списке для асинхронности
async def summ_async_func(list_num):
    summ = 0
    for i in list_num:
        summ += i
    summ_async.append(summ)


# перебор списков для асинхронности
async def count_list(list_, index_):
    for index_block in index_:
        await summ_async_func(list_[index_block[0]:index_block[1] + 1])


# -----------------------
if __name__ == '__main__':
    test_list = create_list(COUNT)
    index_list = create_index_list(PROCESS_NUM)  # список срезов индексов для многозадачности
    print(f"\nСписок случайных чисел от 1 до 100 количеством {COUNT:_} чисел - сформирован...")

    # -----------------------
    # Синхронный способ
    print("\nИтерация 0 / Синхронный метод")
    start_time = time.time()
    summ = summ_func(test_list)
    print(f"Результат: {summ:_},  время работы: {time.time() - start_time:.5f} сек")

    # -----------------------
    # Многопоточность
    print(f"\nИтерация 1 / Многопоточность (кол-во потоков: {PROCESS_NUM})")
    start_time = time.time()
    threads = []  # <- список потоков

    for index_block in index_list:
        thread = Thread(target=summ_thread_func, args=[test_list[index_block[0]:index_block[1] + 1]])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    summ_1 = sum(summ_thread)  # <- итоговая сумма с потоков

    print(f"Результат: {summ_1:_},  время работы: {time.time() - start_time:.5f} сек")

    # -----------------------
    # Многопроцессорность
    print(f"\nИтерация 2 / Многопроцессорность (кол-во процессов: {PROCESS_NUM})")
    start_time = time.time()
    processes = []  # <- список процессов

    for index_block in index_list:
        process = Process(target=summ_process_func, args=[test_list[index_block[0]:index_block[1] + 1], summ_process])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    summ_2 = summ_process.value  # <- итоговая сумма с процессов

    print(f"Результат: {summ_2:_},  время работы: {time.time() - start_time:.5f} сек")

    # -----------------------
    # Асинхронность
    print(f"\nИтерация 3 / Асинхронность (кол-во процессов: {PROCESS_NUM})")
    start_time = time.time()

    asyncio.run(count_list(test_list, index_list))

    summ_3 = sum(summ_async)  # <- итоговая сумма с асинхронных процессов

    print(f"Результат: {summ_3:_},  время работы: {time.time() - start_time:.5f} сек")
    print()