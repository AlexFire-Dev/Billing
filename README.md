_**Billing**_
------------


### **_conf.env_**
`location - deploy/conf.env`


~~~~
PYTHONBUFFEERED=1

QIWI_SECRET_KEY={{ Секретный ключ киви }}
QIWI_PUBLIC_KEY={{ Публичный ключ киви }}
QIWI_DB_VERSION={{ Приставка к названиям счетов }}

SECRET_KEY={{ Секретный ключ django  }}
DB_USER={{ Имя пользователя postgres }}
DB_PASSWORD={{ Пароль БД postgres }}
DB_HOST=db
DB_PORT=5432
DB_NAME={{ БД postgres }}
DEBUG=0

EMAIL_HOST={{ Хост smtp }}
EMAIL_PORT={{ Порт smtp }}
EMAIL_USER={{ Пользователь почты }}
EMAIL_PASSWORD={{ Пароль почты }}
~~~~

________