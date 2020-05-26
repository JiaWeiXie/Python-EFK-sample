# Python EFK sample

## Use

```shell
$ docker-compose up -d --build

$ docker-compose logs -f

$ docker-compose logs -f fluentd
```

- kibana `http://127.0.0.1:5601/`

```shell
$ pipenv install

$ pipenv shell

(venv)$ python main.py
```


### Django logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'fluent.handler.FluentRecordFormatter',
            'format': {
                'host': '%(hostname)s',
                'where': '%(module)s.%(funcName)s',
                'lineno': '%(lineno)d',
                'type': '%(levelname)s',
                'pathname': '%(pathname)s',
            }
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'fluentd': {
            'level': 'WARNING',
            'class': 'myapp.logging.handler.MyFluentdHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['fluentd', 'console'],
            'level': 'WARNING',
        },
    },
}
```


## Reference

- [EFK stack](https://github.com/giefferre/EFK-stack)
- [docker.elastic.co](https://www.docker.elastic.co/)
- [fluent-logger-python](https://github.com/fluent/fluent-logger-python)
- [fluentd](https://docs.fluentd.org/v/0.12/container-deployment/docker-compose)
- [django-fluentd](https://github.com/jayfk/django-fluentd)
- [Django logging](https://docs.djangoproject.com/en/3.0/topics/logging/)
- [Python logging logrecord-attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)
- [Python logging formatter-objectss](https://docs.python.org/3/library/logging.html#formatter-objectss)