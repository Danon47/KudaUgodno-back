# API сервис для веб-сайта "Куда Угодно"
## Технические требования:
* * * 
- python 3.11+ дополнительная библиотека:
  * python-dotenv 1.0.1+
- postgreSQL 17.2+ дополнительная библиотека: 
  * psycopg2 2.9.10+
- django 5.1.6+ дополнительные библиотеки:
  * phonenumbers 8.13.52+
  * django-phonenumber-field 8.0.0+
  * django-cors-headers 4.6.0+
  * django-allauth 65.4.0+
  * dj-rest-auth 7.0.1+
  * social-auth-app-django 5.4.2+
- drf 3.15.2+ дополнительная библиотека:
  * djangorestframework-simplejwt 5.4.0+
- drf-spectacular 0.28.0+
- gunicorn 23.0.0+
- celery 5.4.0+ дополнительная библиотека: 
  * django-celery-beat 2.7.0+
- redis 5.2.1+
- pytest 8.3.4 дополнительные библиотеки: 
  * pytest-django 4.10+
  * factory-boy 3.3.3+
- pillow 11.0.0+

Перед началом создайте файл .env и внесите необходимые данные из файла [.env.sample](.env.sample)

Сервис запущен с помощью CI/CD, локально без внесений изменение в файл docker-compose.yaml его не запустить. 
Необходимо закомментировать 43 строку

(#  - default)

Запустить команду 
``` bash
docker compose up -d --build
```

## Ссылки на контуры
* * * 
- Дев контур: [https://anywhere-dev.god-it.ru/](https://anywhere-dev.god-it.ru/)
- Дев документация в которой описаны все методы API*: [https://anywhere-dev.god-it.ru/api/v1/docs](https://anywhere-dev.god-it.ru/api/v1/docs)
- Дев Django админка: [https://anywhere-dev.god-it.ru/admin](https://anywhere-dev.god-it.ru/admin)
  * админ создаётся автоматически, логин и пароль из GitLab Variables 


- Тест контур: [https://anywhere-test.god-it.ru/](https://anywhere-test.god-it.ru/)
- Тест документация в которой описаны все методы API*: [https://anywhere-test.god-it.ru/api/v1/docs](https://anywhere-test.god-it.ru/api/v1/docs)
- Тест Django админка: [https://anywhere-test.god-it.ru/admin](https://anywhere-test.god-it.ru/admin)
  * админ создаётся автоматически, логин и пароль из GitLab Variables


(*) - Дев и Тест контуры работают 24 часа (после деплоя на сервер). Необходимо сначала выполнить успешный деплой (в ручную с помощью запуска пайплайна или же в коммите в конце указать PushMe!)