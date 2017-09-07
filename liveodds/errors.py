class TotalCornerTokenError(Exception):
    msg = 'Missing TotalCorner token, ' \
          'visit:http://www.totalcorner.com/page/api ' \
          'to obtain a token'

    def __str__(self):
        return self.msg


class LiveOddsBaseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class LiveOddsError(LiveOddsBaseError):
    def __init__(self, msg):
        super().__init__(msg)

    def __str__(self):
        return self.msg
