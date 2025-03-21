# Request

{{method}} {{path}} {{http_version}}\
{{headers}}
{{body}}

GET / HTTP/1.1

# Response
{{http_version}} {{status_code}}\
{{headers}}
{{body}}

## Status codes
100 - 599
- 100 - 199 - информационные коды
- 200 - 299 - success-коды
    - 200 OK - стандартный success-code
    - 201 Created - успешно создан новый ресурс
- 300 - 399 - редиректы
    - 301 Moved permanently - ресурс переехал навсегда
    - 307 Temporary Redirect - ресурс переехал временно
- 400 - 499 - клиентские ошибки
    - 401 - не авторизован
    - 403 - нет прав на контент/контент запрещен
    - 404 - запрашиваем ресурс, который не существует
    - 405 - недоступен текущий HTTP-метод
    - 415 - передан неверный тип контента
- 500 - 599 - серверные ошибки
    - 500 Internal Server Error - общая ошибка сервера

## Method
- GET
    - Получить некоторый ресурс от сервера
- POST
    - Создать некоторый ресурс на сервере
- DELETE
    - Удалить некоторый ресурс на сервере
- PATCH
    - Частично обновить ресурс на сервере
- PUT
    - Полностью обновить ресурс на сервере

## Headers
{{key}}: {{value}}

Содержат полезную метаинформацию
- Откуда сделан запрос (ОС, браузер)
    - User-Agent  
- Какой язык ответа предпочтителен
    - Accept-Language
- Какой контент передается в запросе
    - Content-Type
- Кем сделан запрос*
    - Cookies

## Body
Не все методы поддерживают body\
body - произвольная текстовая информация

- Текст
    - Content-Type: plain/text
- HTML-страницы
    - Content-Type: text/html
- JSON-объект
    - Content-Type: application/json
- Закодированный объект
    - Файл (изображение/музыка/видео)

## Path
2 части: путь до ресурса + параметры ресурса

?{{key1}}={{value1}}&{{key2}}={{value2}}

GET /articles?topic=python&count=100 HTTP/1.1

/articles - путь до ресурса
?topic=python&count=100 - параметры
