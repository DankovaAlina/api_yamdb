# **Описание проекта**

API для сервиса отзывов пользователей на различные произведения.
API поддерживает добавление новых отзывов от лица пользователя и добавление комментариев под отзывами других пользователей.

# **Стек технологий**

Python 3.9.6
Django 3.2
Django REST Framework 3.12.4

# **Как запустить проект**

### **Клонировать репозиторий и перейти в него в командной строке:**

```
git clone https://github.com/DankovaAlina/api_yamdb/
cd api_yamdb
```

### **Cоздать и активировать виртуальное окружение:**

```
python3 -m venv env
source env/bin/activate
```

### **Установить зависимости из файла requirements.txt:**

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

### **Выполнить миграции:**

```
python3 manage.py migrate
```

### **Заполнить Базу Данных:**

```
python3 manage.py add_db_csv
```

### **Запустить проект:**

```
python3 manage.py runserver
```


# **Примеры запросов для использования приложения**

### **Получение всех произведений**
GET-запрос
>*/api/v1/titles/*

### **Создание нового отзыва**
POST-запрос 
>*/api/v1/titles/{title_id}/reviews*

Payload:
application/json
```
{
"text": "string",
"score": 1
}
```

### **Получение всех отзывов**
GET-запрос
>*/api/v1/titles/{title_id}/reviews*

### **Создание нового комментария к отзыву**
POST-запрос 
>*/api/v1/titles/{title_id}/reviews/{review_id}/comments/*

Payload:
application/json
```
{
"text": "string"
}
```

# **Авторы**

@DankovaAlina @lagodmi @Konstantin624
