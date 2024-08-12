'''
Зачем нужно асинхронное программирование?

Оно позволяет выполнять множество задач одновременно, не блокируя выполнение программы, 
что особенно полезно при работе с вводом-выводом (например, сетевыми запросами, файловыми операциями).



В каких задачах используется?

Сетевые приложения - Чаты, веб-сервера, клиенты, API.
Работа с базами данных - Асинхронные драйверы для баз данных позволяют обрабатывать запросы к БД без блокировки основного потока.
Веб-скрейпинг - Одновременное выполнение множества HTTP-запросов для ускорения процесса сбора данных.
Игры и симуляции - Управление игровыми циклами и событиями без блокировок.



Какая польза от асинхронного программирования если нужно сделать только один реквест (или прочитать только один файл)?

Ожидание ответа можно совмещать с выполнением других задач (если они есть).



Подойдёт ли обычный requests.get в asyncio?

Нет.



Библиотеки Python для асинхронного программирования:
- asyncio
- aiohttp
- aiofiles



TODO Нужно проверить - асинхрон подойдет только для БД, реквестов, файлов. То есть только там где есть стадия ожидания результатов. 
Если в асинхроне выполнять долгую затратную вычислительную операцию, то в этот момент другие операции выполняться не будут.

TODO Добавить пример с БД.

'''


# Пример 1: Асинхронный HTTP-запрос

import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    urls = [
        'https://example.com',
        'https://httpbin.org/get',
        'https://python.org'
    ]
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            print(f'Response length: {len(result)}')

asyncio.run(main())



# Пример 2: Асинхронное чтение файлов

import asyncio
import aiofiles

async def read_file(file_path):
    async with aiofiles.open(file_path, mode='r') as f:
        contents = await f.read()
        return contents

async def main():
    #file_paths = ['file1.txt', 'file2.txt', 'file3.txt']
    subfolder_path = 'src/py_and_co/'
    file_paths = ['text_file.txt', 'text_file.txt', 'text_file.txt']
    
    tasks = [read_file(subfolder_path + file_path) for file_path in file_paths]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        print(result)

asyncio.run(main())



# Пример 3: Асинхронные задержки и таймеры

import asyncio

async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    await asyncio.gather(
        say_after(1, 'Hello'),
        say_after(2, 'World')
    )

asyncio.run(main())



# Замерим время и попробуем сделать 10 запросов параллельно

import time
import requests
import asyncio
import aiohttp

def noasync_requestsget_1request():
    start = time.time()
    requests.get('https://example.com')
    end = time.time()
    print('NO Async, requests.get(), 1 request - ', end - start) #  ~ 0.32 sec

def noasync_requestsget_10requests():
    urls = ['https://example.com'] * 10
    start = time.time()
    for url in urls:
        requests.get(url)
    end = time.time()
    print('NO Async, requests.get(), 10 requests - ', end - start) #  ~ 3.27 sec

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def async_aiohttpsession_urls(urls):    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

def async_aiohttp_1request():
    urls = ['https://example.com']
    start = time.time()
    asyncio.run(async_aiohttpsession_urls(urls))
    end = time.time()
    print('Async, aiohttp.ClientSession, 1 request -  ', end - start) #  ~ 0.33 sec

def async_aiohttp_10requests():
    urls = ['https://example.com'] * 10
    start = time.time()
    asyncio.run(async_aiohttpsession_urls(urls))
    end = time.time()
    print('Async, aiohttp.ClientSession, 10 requests -  ', end - start) #  ~ 0.33 sec  (10 запросов по времени заняли как 1 запрос)