# -*- coding: utf-8 -*-
import logging
import time
import datetime

# datetime to str 格式设置
import calendar
from dateutil.relativedelta import relativedelta

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'  # '2015-12-30 15:31:55'\
# 系统中结束时间的默认值 UNIX_TIME
END_UNIX_TIME = 1861891200

logger = logging.getLogger(__name__)


def getTodayStr():
    """
    获取当日的时间字符串2015/06/09
    :return:
    """
    today = datetime.date.today()
    todaystr = today.strftime("%Y-%m-%d")
    return todaystr


def getNowStr():
    """
    获取当前时间字符串 '2015-12-30 15:31:55'
    :return:
    """
    now = datetime.datetime.now()
    nowstr = now.strftime(TIME_FORMAT)
    return nowstr


def strToTime(str):
    """
    字符串转时间
    :param str:
    :return:
    """
    return time.strptime(str, '%Y-%m-%d %H:%M:%S')


def strToDateTime(str):
    """
    字符串转时间
    :param str:
    :return:
    """
    return datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')


def dateTimeToStr(data_time):
    """
    字符串转时间
    :param str:
    :return:
    """
    return data_time.strftime('%Y-%m-%d %H:%M:%S')


def dateToStr(data_time):
    """
    转换成日期字符串
    :param data_time:
    :return:
    """
    return data_time.strftime('%Y-%m-%d')


def strToDate(str):
    """
    字符串转时间
    :param str:
    :return:
    """
    return datetime.datetime.strptime(str, '%Y-%m-%d')


def compareDateTime(data1, data2):
    """
    datetime时间比较
    :return:
    """
    return data1 > data2


def compareDateTimeStr(dataStr1, dataStr2):
    """
     字符 时间 比较
    :return:
    """
    return datetime.datetime.strptime(dataStr1, '%Y-%m-%d %H:%M:%S') > datetime.datetime.strptime(dataStr2,
                                                                                                  '%Y-%m-%d %H:%M:%S')


def get_now_unix_time():
    """
        :return:获取时间戳
    """
    return int(time.time())


def get_now_zero_unix_time():
    """
        :return:获取当前零点时间
    """
    return int(strToSec(secToStr(time.time(), "%Y-%m-%d 00:00:00")))


def secToStr(sec, format=TIME_FORMAT):
    """
    秒转时间字符串
    :param sec: 1453729810
    :return:
    """
    return time.strftime(format, time.localtime(sec))


def strToSec(str, format=TIME_FORMAT):
    """
    时间字符串转秒
    :param str: 2016-01-25 01:01:01
    :return:
    """
    return time.mktime(time.strptime(str, format))


def get_minutes_between_two_unix_time(unix_begin, unix_end):
    """
    获取两个unix时间戳之间差异的分钟数
    :param unix_begin:
    :param unix_end:
    :return:
    """
    fmt = "%Y-%m-%d %H:%M"
    diff_sec = strToSec(secToStr(unix_end, fmt), fmt) - strToSec(secToStr(unix_begin, fmt), fmt)
    return int(diff_sec / 60)


EPOCH = datetime.datetime(1970, 1, 1)


def datetime2timestamp(dt, convert_to_utc=False):
    '''
    Converts a datetime object to UNIX timestamp in milliseconds.
    '''
    if isinstance(dt, datetime.datetime):
        if convert_to_utc:  # 是否转化为UTC时间
            dt = dt + datetime.timedelta(hours=-8)  # 中国默认时区
        timestamp = (dt - EPOCH).total_seconds()
        return long(timestamp)
    return dt


def timestamp2datetime(timestamp, convert_to_local=False):
    '''
    Converts UNIX timestamp to a datetime object.
    '''
    if isinstance(timestamp, (int, long, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local:  # 是否转化为本地时间
            dt = dt + datetime.timedelta(hours=8)  # 中国默认时区
        return dt
    return timestamp


def add_month2(date):
    # number of days this month
    month_days = calendar.monthrange(date.year, date.month)[1]
    candidate = date + datetime.timedelta(days=month_days)
    # but maybe we are a month too far
    if candidate.day != date.day:
        # go to last day of next month,
        # by getting one day before begin of candidate month
        return candidate.replace(day=1) - datetime.timedelta(days=1)
    else:
        return candidate


def add_month(date, delta=1, cycle_id='month'):
    if cycle_id == 'month':
        return date + relativedelta(months=delta)
    if cycle_id == 'year':
        return date + relativedelta(years=delta)
    if cycle_id == 'day':
        return date + relativedelta(days=delta)


def get_last_day(date, bill_cycle_id='month'):
    """
    获取当日/月 日期最后一天
    :param bill_cycle_id:
    :param date:
    :return:
    """
    if bill_cycle_id == 'day':
        last_day = datetime.datetime(date.year, date.month, date.day)
    else:
        _, last_day_num = calendar.monthrange(date.year, date.month)
        last_day = datetime.datetime(date.year, date.month, last_day_num)
    one_day_delta = datetime.timedelta(days=1)
    last_day = last_day + one_day_delta
    return last_day


def get_next_hour(date):
    """
    获取当前时刻的下一个整点小时
    :param date:
    :return:
    """
    cur_day = datetime.datetime(date.year, date.month, date.day, date.hour)
    one_hour_delta = datetime.timedelta(hours=1)
    next_hour = cur_day + one_hour_delta
    return next_hour


def get_next_day(date):
    """
    获取当天的下一天凌晨
    :param date:
    :return:
    """
    cur_day = datetime.datetime(date.year, date.month, date.day)
    one_day_delta = datetime.timedelta(days=1)
    next_day = cur_day + one_day_delta
    return next_day


def get_now_month_day(date):
    """
    获取当天的下一天凌晨
    :param date:
    :return:
    """
    cur_day = datetime.datetime(date.year, date.month, 1)
    return cur_day


def get_next_year(date):
    """
    获取当天的下一天凌晨
    :param date:
    :return:
    """
    return datetime.datetime(date.year + 1, 1, 1)


def get_month_duration(start_time, end_time, bill_cycle='month'):
    logger.info('start_time: %s, end_time: %s, bill_cycle: %s', start_time, end_time, bill_cycle)
    n = 0
    if bill_cycle == 'day':
        delta_date = relativedelta(days=1)
    else:
        delta_date = relativedelta(months=1)
    while end_time > start_time:
        n += 1
        end_time -= delta_date
    next_time = end_time + delta_date
    logger.info('next_time: %s, start_time: %s, end_time: %s', next_time, start_time, end_time)
    all_five_minutes = (next_time - end_time).total_seconds() / 60 / 5
    rest_five_minutes = (next_time - start_time).total_seconds() / 60 / 5
    logger.info('all: %s, rest: %s', all_five_minutes, rest_five_minutes)
    x = rest_five_minutes * 1.0 / all_five_minutes
    n -= 1
    logger.info('n: %s, x: %s, x+n: %s', n, x, x + n)
    if bill_cycle in ('month', 'day'):
        return x + n
    if bill_cycle == 'year':
        return (x + n) * 1.0 / 12


def create_time_7_24_1(add_time):
    """
        跟你讲创建时间推算
        24小时 7天 1个月的时间
    :param add_time:
    :return:
    """
    if isinstance(add_time, str):
        add_time = strToDateTime(add_time)
    date_now = datetime.datetime.now()
    before_day = date_now - datetime.timedelta(days=1)
    before_day7 = date_now - datetime.timedelta(days=7)
    before_month = date_now - datetime.timedelta(days=30)
    # 比较一下,取小的
    start_time_24h = compareDateTime(add_time, before_day) and add_time or before_day
    start_time_7d = compareDateTime(add_time, before_day7) and add_time or before_day7
    start_time_1m = compareDateTime(add_time, before_month) and add_time or before_month
    datetime_dict = {
        'add_time': dateTimeToStr(add_time),
        'start_time': dateTimeToStr(start_time_1m),  # 默认24h
        'end_time': dateTimeToStr(datetime.datetime.now()),
        'start_time_24h': dateTimeToStr(start_time_24h),
        'start_time_7d': dateTimeToStr(start_time_7d),
        'start_time_1m': dateTimeToStr(start_time_1m),
    }
    return datetime_dict


MAX_TIMESTAMP = datetime2timestamp(datetime.datetime.max)


class TimeHandle(object):
    def __init__(self):
        self.now = datetime.datetime.now()

    def get_now_datetime(self):
        return self.now

    def get_now_str(self):
        return self.now.strftime('%Y-%m-%d %H:%M:%S')

    def get_today_str(self):
        """
        获取今天的时间字符串 2017-12-24
        :return:
        """
        now_date = self.now
        today_str = now_date.strftime('%Y-%m-%d')
        return today_str

    def get_today_start_timestamp(self):
        """
        获取今天凌晨开始的时间戳(秒为单位)1514044800
        :return:
        """
        now_date = self.now
        today_start_timestamp = int(
            time.mktime(datetime.datetime(now_date.year, now_date.month, now_date.day).timetuple()))
        return today_start_timestamp

    def get_yesterday_str(self):
        """
        获取昨天的时间字符串2017-12-23
        :return:
        """
        now_date = self.now
        yesterday_str = (now_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        return yesterday_str

    def get_yesterday_start_timestamp(self):
        """
        获取昨天凌晨开始的时间戳1513958400
        :return:
        """
        yesterday_str = self.get_yesterday_str()
        yesterday_y, yesterday_m, yesterday_d = map(int, yesterday_str.split('-'))
        yesterday_start_timestamp = int(
            time.mktime(datetime.datetime(yesterday_y, yesterday_m, yesterday_d).timetuple()))
        return yesterday_start_timestamp

    def get_seven_days(self):
        """
        获取七日后时间字符串 2018-01-01
        :return:
        """
        now_date = self.now
        seven_days_str = (datetime.datetime(now_date.year, now_date.month, now_date.day) + datetime.timedelta(days=8))\
            .strftime('%Y-%m-%d %H:%M:%S')
        return seven_days_str

    def get_this_month_start_datetime(self):
        """
        获取本月开始的datetime(2017,12,1,0,0,0)
        :return:
        """
        now_date = self.now
        this_month_start_datetime = datetime.datetime(now_date.year, now_date.month, 1)
        return this_month_start_datetime

    def get_this_month_start_str(self):
        """
        获取本月第一天时间字符串2017-12-01
        :return:
        """
        this_month_start_datetime = self.get_this_month_start_datetime()
        this_month_start_str = this_month_start_datetime.strftime('%Y-%m-%d')
        return this_month_start_str

    def get_this_month_start_timestamp(self):
        """
        获取本月开始时间戳（绝大部分场景下，等效于上月结束时间戳）1512057600
        :return:
        """
        this_month_start_datetime = self.get_this_month_start_datetime()
        this_moth_start_timestamp = int(time.mktime(this_month_start_datetime.timetuple()))
        return this_moth_start_timestamp

    def get_this_month_str(self):
        """
        获取本月的时间字符串 2018-03
        :return:
        """
        this_month_start_datetime = self.get_this_month_start_datetime()
        this_month_str = this_month_start_datetime.strftime('%Y-%m')
        return this_month_str

    def get_last_month_start_datetime(self):
        """
        获取上月开始的datetime(2017,11,1,0,0,0)
        :return:
        """
        this_month_start_datetime = self.get_this_month_start_datetime()
        last_month_end_datetime = this_month_start_datetime - datetime.timedelta(days=1)
        last_month_start_datetime = datetime.datetime(last_month_end_datetime.year, last_month_end_datetime.month, 1)
        return last_month_start_datetime

    def get_last_month_start_str(self):
        """
        获取上月第一天的时间字符串 2017-11-01
        :return:
        """
        last_month_start_datetime = self.get_last_month_start_datetime()
        last_month_start_str = last_month_start_datetime.strftime('%Y-%m-%d')
        return last_month_start_str

    def get_last_month_str(self):
        """
        获取上月的时间字符串 2017-11
        :return:
        """
        last_month_start_datetime = self.get_last_month_start_datetime()
        last_month_start_str = last_month_start_datetime.strftime('%Y-%m')
        return last_month_start_str

    def get_last_month_start_timestamp(self):
        """
        获取上月开始的时间戳 1509465600
        :return:
        """
        last_month_start_datetime = self.get_last_month_start_datetime()
        last_month_start_timestamp = int(time.mktime(last_month_start_datetime.timetuple()))
        return last_month_start_timestamp

    def get_last_month_end_str(self):
        """
        获取上月最后一天date： 2018-02-28
        :return:
        """
        this_month_start_datetime = self.get_this_month_start_datetime()
        last_month_end_datetime = this_month_start_datetime - datetime.timedelta(days=1)
        last_month_end_str = last_month_end_datetime.strftime('%Y-%m-%d')
        return last_month_end_str


if __name__ == '__main__':
    mytime = TimeHandle()
    print mytime.get_today_str()
    print mytime.get_today_start_timestamp()
    print mytime.get_yesterday_str()
    print mytime.get_yesterday_start_timestamp()
    print mytime.get_this_month_start_datetime()
    print mytime.get_this_month_start_str()
    print mytime.get_this_month_start_timestamp()
    print mytime.get_last_month_start_datetime()
    print mytime.get_last_month_start_str()
    print mytime.get_last_month_start_timestamp()
    print mytime.get_seven_days()
    # ddd = datetime.datetime.now()
    # print get_now_month_day(ddd)
    # print datetime.datetime.now() - datetime.timedelta(days=1)

    # print  getTodayStr()
    # print strToTime(getTodayStr() + " 00:00:00")
    # print strToDateTime(getTodayStr() + " 00:00:00")
    # print compareDateTime(datetime.datetime.now(), strToDateTime("2015-12-24 00:00:00"))
    # print datetime2timestamp(datetime.datetime.now())
    # print timestamp2datetime(time.time())
    # print MAX_TIMESTAMP


    # print(add_month(ddd))
    # print str(dateTimeToStr(ddd))
    # time.sleep(30)
    # print str(int(time.time()))
    # print str(dateTimeToStr(ddd))
