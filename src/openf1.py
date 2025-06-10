"""
This file is used to retieve openf1 data from the API.
"""

import datetime
from typing import Optional
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from pandas import DataFrame
import pandas as pd

from urllib3 import HTTPResponse

class OpenF1:
    """
    This class is used to retrieve data from the openf1 API.
    """

    def __init__(self):
        self.base_url = "https://api.openf1.org/v1/"
        
    
    def get_data(self, endpoint: str, query_params: Optional[dict] = None):
        """
        This function is used to get data from the openf1 API.
        :param endpoint: The endpoint to get data from.
        :return: The data from the API.
        """
        url = f"{self.base_url}{endpoint}"
        if query_params:
            query_string = urlencode(query_params)
            url = f"{url}?{query_string}"
        response: HTTPResponse = urlopen(url)
        
        if response.status == 200:
            return json.loads(response.read().decode('utf-8'))
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def get_latest_meeting(self) -> dict:
        """
        This function is used to get the latest meeting from the openf1 API.
        :return: The latest meeting from the API.
        """
        meetings_df = DataFrame(self.get_data(endpoint="meetings", query_params={"year": datetime.datetime.now().year}))
        meetings_df.sort_values(by="date_start", inplace=True, ascending=False)
        return meetings_df.to_dict(orient="records")[0]
    
    def get_latest_meetings_session_keys_with_session_name(self) -> list[dict[str, int|str]]:
        """
        This function is used to get the latest meeting's session keys with sessions type.
        :return: A list of dictionaries with session_key and session_type.
        """
        latest_meeting: dict = self.get_latest_meeting()
        sessions_df = DataFrame(self.get_data(endpoint="sessions", query_params={"meeting_key": latest_meeting["meeting_key"]}))
        return sessions_df[["session_key", "session_name"]].to_dict(orient="records")
    
    def get_laps_per_session(self):
        """
        This function is used to retern all laps for all sessions in a race weekend
        : return list[dicts]
        """
        sessions: list[dict] = self.get_latest_meetings_session_keys_with_session_name()

        for session in sessions:
            drivers_df = DataFrame(self.get_drivers_per_session(session["session_key"]))
            session_intervals_df: DataFrame = DataFrame(self.get_data(endpoint="laps", query_params={"session_key":session["session_key"]}))
            session_intervals_df.sort_values("lap_duration", inplace=True)
            if drivers_df.empty or session_intervals_df.empty:
                print(f"drivers/ intervals are empty for: {session['session_name']}")
                continue
            intervals_with_drivers = pd.merge(left=session_intervals_df, right=drivers_df, on="driver_number")
            intervals_with_drivers.to_csv(f'{session["session_name"]}.csv')
    
    def get_drivers_per_session(self, session_key: str) -> dict:
        """
        This function returns all drivers for a specific section.
        : return
        """
        return self.get_data(endpoint="drivers", query_params={"session_key": session_key})

    
    