from enum import Enum
from functools import partial
from dacite import Config, from_dict
from cryptomarket.dataclasses.report import Report


def intercept_report(callback):
    return partial(intercept_report_, callback=callback)


def intercept_report_(err, response, callback):
    if err:
        callback(err, None)
        return
    reports = from_dict(data_class=Report, data=response,
                        config=Config(cast=[Enum]))
    callback(None, reports)
