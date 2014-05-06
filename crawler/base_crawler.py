import random
import time

class BaseCrawler(object):

    def _sleep(self, period):
        assert period in ['short', 'long']
        d = 10 if period == 'long' else 3
        sleep_time = random.randint(0, 100) % d
        time.sleep(sleep_time)

