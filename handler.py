from __future__ import print_function

import traceback

from fluent import handler, sender


class MyFluentdHandler(handler.FluentHandler):
    """An log handler that sends all incoming logs to a fluentd instance"""

    def __init__(self, *args, **kwargs):
        self.config = self._load_settings()

        super().__init__(
            **self.config
        )

    def _load_settings(self):
        """load configuration from settings.py and return a dict"""
        print("loading config")
        config = {
            "host": '127.0.0.1',
            "port": 24224,
            "tag": 'app'
        }

        return config

    def has_string_message(self, record):
        """checks if the record has a massage with type str. This is true when the logger is called like this:
         logger.debug("foo")."""
        if isinstance(record.msg, str):
            return True
        return False

    def add_string_to_record(self, record):
        """adds the string in msg.record to a dictionary"""
        record.msg = {"message": record.msg}
        return record

    def has_exception(self, record):
        """returns True if the record has a exc_info"""
        if record.exc_info:
            return True
        return False

    def add_exception_to_record(self, record):
        """adds a traceback (and a message if it is not defined) to record.msg"""
        tb = traceback.format_exception(*record.exc_info)

        if isinstance(record.msg, dict):
            record.msg.update("traceback", tb)
        elif self.has_string_message(record):
            record = self.add_string_to_record(record)
            record.msg.update("traceback", tb)
        else:
            record.msg = {
                "message": record.getMessage(),
                "traceback": tb
            }

        return record

    def emit(self, record):
        #As of fluent-logger v 0.3.3 logged exceptions have no information. Make sure to add a message
        #and to add traceback information if available
        if self.has_exception(record):
            record = self.add_exception_to_record(record)

        #As of fluent-logger v 0.3.3 logs with a plain string as message don't get converted.
        #That's a problem, because logs in the format of logger.debug("foobar") just have no message.
        #convert record.msg to a dict containing the message
        if self.has_string_message(record):
            record = self.add_string_to_record(record)

        data = self.format(record)
        _sender = self.sender
        return _sender.emit_with_time('python',
                                      sender.EventTime(record.created)
                                      if _sender.nanosecond_precision
                                      else int(record.created),
                                      data)