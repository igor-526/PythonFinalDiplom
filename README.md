# Дипломный проект
## Описание
Проект реализует взаимодействие между продавцами товара и их покупателями посредством API

## Инструкция по запуску
```
pip install -r requirements.txt
docker compose up
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## API Endpoints
| Описание                 | Метод | EndPoint                | Данные                                                                          |
|--------------------------|-------|-------------------------|---------------------------------------------------------------------------------|
| Регистрация пользователя | POST  | /auth/users/            | email <br> password <br> type(shop/buyer)                                       |
| Вход пользователя        | POST  | /auth/token/login/      | email <br> password                                                             |
| Импорт товаров           | POST  | /api/v1/partner/update/ | Headers:Authorization - Token \<auth token> <br/> Form-data:update - file.yaml* |

*пример файла для импорта товаров можно найти в папке "to_import"
