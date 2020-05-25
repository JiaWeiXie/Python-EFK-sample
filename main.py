import time
import logging

from fluent import sender, event, handler
from handler import MyFluentdHandler

custom_format = {
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',
  'lineno': '%(lineno)d',
  'type': '%(levelname)s',
  'pathname': '%(pathname)s'
}


def custom():
    logging.basicConfig(level=logging.INFO)
    l = logging.getLogger('fluent.custom')
    h = MyFluentdHandler()
    formatter = handler.FluentRecordFormatter(custom_format)
    h.setFormatter(formatter)
    l.addHandler(h)
    l.info({
    'from': 'EE',
    'to': 'FF'
    })


def handle():
    logging.basicConfig(level=logging.INFO)
    l = logging.getLogger('fluent.handle')
    h = handler.FluentHandler('app', host='127.0.0.1', port=24224)
    formatter = handler.FluentRecordFormatter(custom_format)
    h.setFormatter(formatter)
    l.addHandler(h)
    l.info({
    'from': 'CC',
    'to': 'DD'
    })

def base():
    logger = sender.FluentSender('app', host='127.0.0.1', port=24224)
    cur_time = int(time.time())
    logger.emit_with_time('AA', cur_time, {'from': 'AA', 'to':'BB'})

def main():
    # base()
    # handle()
    custom()
    


if __name__ == "__main__":
    main()