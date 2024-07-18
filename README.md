# Минисервис по поиску запчастей на Django / FastAPI


## Описание проекта<a name="description"></a>
Тестовое задание по поиску информации о запчастях. Cоздано на чистом Django и FastAPI.


### Используемый стек<a name="stack"></a>

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![FastAPI][FastAPI-badge]][FastAPI-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Docker][Docker-badge]][Docker-url]

### Системные требования
- Python 3.10+;


### Установка проекта локально в контейнерах Docker <a name="local-install"></a>

1. **Склонировать репозиторий:**

   ```bash
   git clone https://github.com/VitaliyDrozdov/bibinet_test
   cd bibinet_test


2. **Подготавливаем бэкенд к работе**:

*Копируем файл*  .env.example с новым названием .env и заполняем его необходимыми данными:

```shell
cp .env.example .env
```
*Запускаем docker контейнеры*

```shell
docker compose up
```

*Наполняем БД данными*:
```shell
docker docker exec -it bibibnet_new-backend-1 /bin/bash
python manage.py migrate
python manage.py generate_marks_models
python manage.py generate_part
exit
```


## После запуска контейнеров сервисы будут доступны по адресам:

*Для Djnago*
```http://localhost:8000/django/```

*Для FastAPI*
 ```http://localhost:9000/fastapi/```



## Примеры запросов:
- Список марок машин:
``` GET /django/mark/ ```

- Список моделей:
``` GET /django/model/ ```

- Список запчастей:
``` GET /django/parts/ ```

- Поиск запчатей через json request (Django):
``` POST django/search/part/ ```

- Поиск запчатей через json request (FastAPI):
``` POST fastapi/search_v2/part/ ```


Пример результата поиска
```{
"response": [
{
"mark": {
"id": 1,
"name": "Honda",
"producer_country_name": "Япония"
},
"model": {
"id": 2,
"name": "Accord"
},
"name": "Бампер передний",
"json_data": {
"is_new_part": true,
"color": "красный",
"count": 4
},
"price": 2300
}
],
"count": 1,
"summ": 2300
}
```


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white


[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white

[Docker-url]: https://www.postgresql.org/

[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[FastAPI-url]: https://fastapi.tiangolo.com/

[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
