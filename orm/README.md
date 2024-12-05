# ORM

ORM - Object Relation Mapping

По сути - утилита которая приводит таблицы в БД к Python-объектам

Можно:
- Делать CRUD-операции
- Задавать структуру БД
- Определять отношения м-ду сущностями БД
- Делать запросы в БД (в том числе и в "сыром" виде)

User.all() -> "select * from users"
User.create({...}) -> "insert (?, ...) table users values (?, ...)"
User.filter(email="email2@gmil.com")