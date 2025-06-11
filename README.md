# dds_webproject

Инструкция по установке и запуску проекта

1. Клонирование репозитория: 
    git clone https://github.com/skumwo/dds_webproject.git
    cd your-repo

2. Создание виртуального окружения: 
    1) python -m venv .venv    
    2) Linux/Mac: source .venv/bin/activate или
    Windows: .venv\Scripts\activate 

3. Установка зависимостей: 
    pip install -r requirements.txt

5. Миграции базы данных: 
    python manage.py migrate

6. Создание администратора: 
    python manage.py createsuperuser

7. Перейдите в браузере по адресу:
http://127.0.0.1:8000

   Посмотреть: https://dds-webproject.onrender.com/