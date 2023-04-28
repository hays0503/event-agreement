import aiohttp
import asyncio
import json

def send_post(urls, events):
    '''
        Отправка данных на удалённый сервер
    '''
    # try:
    # except Exception as e:
    # #print("Ошибка==================",e)
    try:
        asyncio.run(get_http_response(
            urls=urls, events=events))
        return True
    except Exception as e:
        print("Что то пошло не по плану SendPost\n", e)
        return False


async def get_http_response(urls, events) -> dict:
    '''
        Отправка данных на удалённый сервер
    '''
    tasks = []
    events = json.dumps(events)
    async with aiohttp.ClientSession() as session:
        task = asyncio.ensure_future(session.post(url=urls, data=events, timeout=0))  # Создай
        tasks.append(task)  # Добавь в массив заданий
        await asyncio.gather(*tasks)  # Запусти все задание
        
#####################################################################################
