import requests

from .config import totalcorner_API_URL
from .errors import LiveOddsError, TotalCornerTokenError


class totalcorner():
    """
    Wrapper class for totalcorner API_URL
    """
    def __init__(self, token):
        """
        :param token: TotalCorner API token, Required.
        """
        if not token:
            raise TotalCornerTokenError

        self.token = token
        self.params = {}

    def _get(self, api_endpoint, **kwargs):
        """
        Method for making a request to TotalCorner API
        :param api_endpoint: Totalcorner API endpoint
        """
        req_str = totalcorner_API_URL + api_endpoint
        response = requests.get(url=req_str, params=self.params)
        return response.json()

    def get_odds(self, **kwargs):
        """
        Method for retrieving odds from totalscore
        """
        if kwargs:
            self.params.update(**kwargs)
        self.params['token'] = self.token
        self.params['type'] = 'inplay'
        self.params['columns'] = "odds,cornerLine,cornerLineHalf,\
        goalLine,goalLineHalf,asianCorner,attacks,\
        dangerousAttacks,shotOn,shotOff,possession"

        data = self._get('match/today', params=self.params)

        if not data['success']:
            raise LiveOddsError(str(data['error']))
            return 1
        return data["data"]

    def get_league_odds(self, league_id, **kwargs):
        """
        Method for retrieving league odds from totalscore
        """
        self.league_id = league_id
        if kwargs:
            self.params.update(**kwargs)
        self.params['type'] = 'inplay'
        self.params['token'] = self.token
        self.params['columns'] = "odds,cornerLine,cornerLineHalf,\
        goalLine,goalLineHalf,asianCorner,attacks,\
        dangerousAttacks,shotOn,shotOff,possession"

        data = self._get(f'league/schedule/{self.league_id}',
                         params=self.params)

        if not data['success']:
            raise LiveOddsError(str(data['error']))
            return 1
        return data["data"]

    def get_match_odds(self, match_id, **kwargs):
        """
        Method for retrieving odds for a specific match
        """
        self.match_id = match_id
        if kwargs:
            self.params.update(**kwargs)
        self.params['token'] = self.token
        self.params['columns'] = ['events', 'odds']

        req_str = f'matchodds/{self.match_id}'
        data = self._get(req_str, params=self.params)

        if not data['success']:
            raise LiveOddsError(str(data['error']))
            return 1
        return data["data"]
