## 1. Install dependencies
```
pip install -r requirements.txt
```

## 2. Run broker RabbitMQ
```
docker run -d -p 5672:5672 rabbitmq
```

## 3. Run worker
```
celery -A lesson_11_celery worker -l INFO
```

## 4. Run celery beat
```
celery -A hilel12 beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## 5. Run Django web server
```
py manage.py runserver
or
python manage.py runserver
```