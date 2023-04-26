from aiohttp import web


async def post_func(request):
    #########################################
    # Обработчик входящих подключений
    body = await request.json()

    print("Принял сообщение=>", body)

    
    # пустое сообщение обрабатываем
    if len(body['messages']) == 0:
        return web.json_response({"Ответ": "сообщения нет, нечего обрабатывать"})
    #########################################
    # Обработка включение контролера от упр сервера
    response_body = post_server_response(body)
    #########################################
    return web.json_response(response_body)


def post_server_response(body: any):

    try:
        if(body["type"]=="read"):
            response_body = "Ответ"
        
        return response_body

    except AttributeError:
        return {"status":"Эмулятор еще не запущен","code":500}

def new_document(body:any):
    pass