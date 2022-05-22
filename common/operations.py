import re
from functools import wraps
from time import time
import datetime
from pytz import timezone


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r took: %2.4f sec' % (f.__name__, te - ts))
        # print('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        return result

    return wrap


def clean_twitter_username(user):
    if not user:
        return
    return re.sub(r'\?s=.*', '', user.replace("/", "").replace("https://twitter.com/", "")
                  .replace("https:twitter.com", "").replace("@", "").strip())


def get_date():
    tz = timezone('US/Eastern')
    return str(datetime.datetime.now(tz).date()).replace("-", "")