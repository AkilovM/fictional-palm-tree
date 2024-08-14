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



Когда вы определяете функцию с ключевым словом async, Python создает корутину, которую можно запустить и управлять её выполнением с помощью await, 
а также планировать выполнение с помощью таких инструментов, как asyncio.create_task, await asyncio.gather.

Корутина (coroutine) — это объект, представляющий асинхронную задачу, которая может выполнять асинхронные операции, например, ввод-вывод, не блокируя основной поток выполнения.


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



# Пример 4: Выполняем 10 HTTP-запросов параллельно

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



# Пример неправильного использования async: пока выполняется реквест, запускается блокирующий код time.sleep. Пока он не выполнится, результат реквеста не будет обработан.

import time
import asyncio
import aiohttp

async def blocking_code():
    start = time.time()
    time.sleep(1)
    end = time.time()
    print('Blocking code time - ', end - start)

async def fetch_url(session, url):
    result = ''
    start = time.time()
    async with session.get(url) as response:
        result = await response.text()
    end = time.time()
    print('fetch url time - ', end - start)
    return result

async def async_request_and_sleep():
    url = 'https://example.com'
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url(session, url),    # 1.32
            blocking_code()             # 1.00
        ]
        results = await asyncio.gather(*tasks)

asyncio.run(async_request_and_sleep())



# Тест производительности - асинхронное чтение файлов.
# Read 1 files             0.0023   sec
# Read 10 files            0.0039   sec
# Read 100 files           0.0263   sec
# Read 1000 files          0.3006   sec
# Read 10000 files         3.3957   sec
# Read 100000 files       35.7291   sec

import time
import asyncio
import aiofiles

async def read_file(file_path):
    async with aiofiles.open(file_path, mode='r') as f:
        contents = await f.read()
        return contents

async def async_read_files(filepaths):
    start = time.time()
    tasks = [read_file(filepath) for filepath in filepaths]
    results = await asyncio.gather(*tasks)
    end = time.time()
    print(f'Read {len(filepaths)} files\t\t', end - start)

filepath = 'src/py_and_co/text_file.txt'
for i in range(6):
    filepaths = [filepath] * 10**i
    asyncio.run(async_read_files(filepaths))