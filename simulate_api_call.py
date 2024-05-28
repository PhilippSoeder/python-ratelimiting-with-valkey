import argparse
import datetime
from dateutil import relativedelta
import redis
import time


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--token", type=str)
    argparser.add_argument("--endpoint", type=str)
    argparser.add_argument("--monthly-limit", type=int)
    return argparser.parse_args()


def incr_cnt(valkey, token: str, endpoint: str) -> int:
    """
    Increments the counter for given token and endpoint combination.
    Counter will expire second day of next month.
    Could also expire directly on the first day of next month,
    but one day added to potentially add reporting.
    Returns the incremented counter.
    """
    current_month = get_current_month()
    expire = get_expire_unix_time()

    key = f"{current_month}#{endpoint}#{token}"

    # To cut down the number of round-trip transactions, pipeline() is used.
    with valkey.pipeline() as pipe:
        pipe.multi()
        pipe.incr(key)
        pipe.expireat(key, expire)
        results = pipe.execute()
    return results[0]


def is_monthly_limit_exceeded(cnt: int, monthly_limit: int) -> bool:
    return cnt > monthly_limit


def get_current_month() -> int:
    date = datetime.datetime.now()
    return date.month


def get_expire_unix_time() -> int:
    """ Returns the unix timestamp in seconts of the 2nd day of next month """
    expire = datetime.date.today() + relativedelta.relativedelta(months=1)
    expire = expire.replace(day=2)
    return int(time.mktime(expire.timetuple()))


if __name__ == "__main__":
    args = get_args()

    token = args.token
    endpoint = args.endpoint
    monthly_limit = args.monthly_limit

    valkey = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    cnt = incr_cnt(valkey, token, endpoint)

    if is_monthly_limit_exceeded(cnt, monthly_limit):
        print("monthly limit exceeded.")
    else:
        print("monthly limit not exceeded.")
