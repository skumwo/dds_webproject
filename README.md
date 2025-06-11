# dds_webproject

Инструкция по установке и запуску проекта

1. Клонирование репозитория: 
    1) git clone https://github.com/skumwo/dds_webproject.git
    2) cd dds_webproject

2. Создание виртуального окружения: 
    1) python -m venv .venv    
    2) Linux/Mac: source .venv/bin/activate или
    Windows: .venv\Scripts\activate 

3. Установка зависимостей: 
    pip install -r requirements.txt

4. Миграции базы данных: 
    python manage.py migrate

5. Создание администратора: 
    python manage.py createsuperuser

6. Перейдите в браузере по адресу:
http://127.0.0.1:8000

Посмотреть сайт: https://dds-webproject.onrender.com/