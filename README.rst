Установка
=========

Установка производится так же, как и любой другой джанго проект. Никаких библиотек не используется.

Тестовые данные
===============

Развернуть тестовые данные можно одинм из трех способов:

1. Можно восстановить .sql файлы. Они лежат в каталоге /static/files/sql.

2. Можно загрузить данные из fixtures. Они лежат в катлоге /photos/fixtures.

Сначала нужно загрузить файл auth.json:

::

	python manage.py loaddata photos/fixtures/auth.json

Затем файл photos.json:

::

	python manage.py loaddata photos/fixtures/photos.json

3. Можно сгенерировать новые данные. Для этого нужно запустить команду:

::

	python manage.py data_generator

Так как генерируется большое количество данных, это можно занять некоторое время. Сначала генерируются теги. Затем
пользователи, id которых берутся из файла /static/files/csv/test-photo.csv. Затем из этого же файла берутся
данные для генерации фоток. Затем генерируются связи между фотками и тегами. И в конце генерируются данные по лайкам
для фоток.

В каталоге site_vostok/settings нужно создать файл pswd.py и указать значения констант LOCAL_DB_NAME, LOCAL_DB_USER,
LOCAL_DB_PASS - это имя БД, пользователь и пароль от БД соответственно.
