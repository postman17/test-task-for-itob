Тестовое задание Python (ITOB)

 

Необходимо реализовать систему выполнения заданий на перевозку.

 

Сценарий использования системы:

    В системе могут зарегистрироваться грузоотправители и перевозчики. Грузоотправитель публикует задание на перевозку и указывает его стоимость
    Перевозчик видит список заданий на перевозку, доступных для исполнения.
    Перевозчик выбирает задание для исполнения, при этом перевозчику на счёт зачисляется стоимость задания за вычетом комиссии.
    У одного задания может быть только один исполнитель. 

 

Мы хотим увидеть в реализации:

    Надёжность работы под высокой нагрузкой.
    Точность операций с деньгами.
    Устойчивость к основным типам атак.

 

Технологии, которые должны быть задействованы:

    Python 3
    Flask
    SQLAlchemy (Declarative)
    SQLite (встроенный в приложение)
    Jinja2 Templates
    WTForms
    jQuery (желательно, но возможно использование альтернативных решений)

Список может быть расширен по усмотрению кандидата, но с обязательным использованием технологий, перечисленных выше.

 

Дополнительные требования:

    Проект должен содержать SQL-скрипты для развертывания базы данных и наполнения ее тестовыми данными.
    Пользовательские данные должны валидироваться перед сохранением в БД.
    


###Установка
```
make db-init
make migrate
make upgrade
make import-data
```
###>Юзеры
```
qwerty@mail.ru - qwerty
zxcv@mail.ru - zxcv
```