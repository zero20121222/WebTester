# coding=utf-8
# Date=1/16/15
from time import sleep

__author__ = 'MichaelZhao'

from datetime import *

class DateTimes(object):
    @staticmethod
    def now(date_str=None, format_type=None):
        if date_str is None:
            return datetime.now()
        else:
            return DateTimes.str_to_datetime(date_str, format_type)

    @staticmethod
    def str_to_datetime(t_str, format_type=None):
        if format_type is None:
            return datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
        else:
            return datetime.strptime(t_str, format_type)

    @staticmethod
    def datetime_to_str(date_obj):
        if isinstance(date_obj, datetime):
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError("DateTime format to string failed, dateObj:%s", date_obj)

    @staticmethod
    def inc_days(date_obj, days):
        if isinstance(date_obj, datetime):
            return date_obj + timedelta(days=days)
        else:
            raise ValueError("DateTime inc %s failed, dateObj:%s", days, date_obj)

    @staticmethod
    def dec_days(date_obj, days):
        if isinstance(date_obj, datetime):
            return date_obj + timedelta(days=days)
        else:
            raise ValueError("DateTime dec %s failed, dateObj:%s", days, date_obj)

    @staticmethod
    def compare_dates(from_date, to_date):
        if not isinstance(from_date, datetime) or not isinstance(to_date, datetime):
            raise ValueError("DateTime compare failed, date1:%s, date2:%s", from_date, to_date)
        else:
            return to_date >= from_date

    @staticmethod
    def day_of_week(date_obj):
        '''
        今天是这周的第几天
        :param date_obj:
        :return:
        '''
        if not isinstance(date_obj, datetime):
            raise ValueError("DateTime is not dateObj, date_obj:%s", date_obj)
        else:
            return int(date_obj.strftime("%w"))

    @staticmethod
    def day_of_year(date_obj):
        '''
        今天是今年的第几天
        :param date_obj:
        :return:
        '''
        if not isinstance(date_obj, datetime):
            raise ValueError("DateTime is not dateObj, date_obj:%s", date_obj)
        else:
            return int(date_obj.strftime("%j"))

    @staticmethod
    def week_of_year(date_obj):
        '''
        今周是今年的第几周
        :param date_obj:
        :return:
        '''
        if not isinstance(date_obj, datetime):
            raise ValueError("DateTime is not dateObj, date_obj:%s", date_obj)
        else:
            return int(date_obj.strftime("%U"))