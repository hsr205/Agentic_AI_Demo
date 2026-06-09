from typing import Any

import requests
from requests import RequestException

from config.config import Settings
from logger.logger import AppLogger
from utils.constants import Constants


class TicketTools:

    def __init__(self) -> None:
        self._config: Settings = Settings()
        self._api_key: str = self._config.ticketmaster_consumer_key
        self._api_secret: str = self._config.ticketmaster_consumer_secret
        self._logger = AppLogger.get_logger(self.__class__.__name__)

    def get_ticketmaster_response_dict(self) -> list[dict]:

        response_list: list[dict] = []

        parameters_dict: dict[str, str] = {
            "apikey": self._api_key,
            # "keyword": "New York Knicks Home Game Watch Party Tickets",
            "keyword": "New York Knicks",
            "size": 5
        }

        try:
            response = requests.get(url=Constants.TICKETMASTER_URL_ENDPOINT, params=parameters_dict)
            response.raise_for_status()
            response_dict: dict[str, Any] = response.json()

            if "_embedded" in response_dict:
                event_list: list[dict[str, Any]] = response_dict.get("_embedded").get("events")

                for event in event_list:

                    event_name: str = event.get('name')
                    event_date: str = event.get('dates').get('start').get('localDate')
                    event_venue_name: str = event.get('_embedded').get('venues')[0].get('name')
                    event_url: str = event.get('url')

                    event_dict: dict[str, str] = {
                        "event_name": event_name,
                        "event_date": event_date,
                        "event_venue_name": event_venue_name,
                        "event_url": event_url,
                    }


                    response_list.append(event_dict)

                return response_list
            else:
                self._logger.warning("No events found matching your criteria.")

        except RequestException as e:
            self._logger.error(f"An error occurred: {e}")
            raise RequestException

    def _display_ticketmaster_response(self, event_dict:dict) -> None:

        self._logger.info(f"Event: {event_dict.get('name')}")
        self._logger.info(f"Date: {event_dict.get('dates').get('start').get('localDate')}")
        self._logger.info(f"Venue: {event_dict.get('_embedded').get('venues')[0].get('name')}")
        self._logger.info(f"URL: {event_dict.get('url')}")
        self._logger.info("=" * 125)
