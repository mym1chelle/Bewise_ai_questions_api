# Задача 1: Сервис вопросов

## Сборка

1. [Установить Docker](https://www.docker.com)
2. [Установить Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. Клонировать проект в локальную директорию:
```
https://github.com/mym1chelle/Bewise_ai_questions_api
```
4. Переименовать файл `.env.example` в `.env`
5. В директории клонированного проекта запусть сбор образов и запуск контейнеров Docker:

```
docker compose up --build
```

## Работа с API

Перейти по ссылке на страницу с документацией к API
```
http://localhost:8000/docs#/
```
На этой странице содержится информация:
* о эндпоинтах и типах запросов к ним
* о параметрах для запросов, их типах и ограничения
* о результатах запросов в случае успешного выполнения или ошибок