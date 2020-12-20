class Governer
    def __init__(self, max_count, period):
        """rate = count/period"""
        self.max_count = max_count
        self.count = 0
        self.period = period

    def request(self):
        if self.count >= self.max_count:
            return False

        if self.timer is None:
            # start timer
            return


