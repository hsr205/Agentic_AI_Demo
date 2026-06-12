import logging
import sys
from typing import Any

import requests
from fastmcp import FastMCP
from requests import RequestException

from config.config import Settings
from logger.logger import AppLogger
from utils.constants import Constants


class TicketMCPServer:

    def __init__(self) -> None:
        self._config: Settings = Settings()
        self._api_key: str = self._config.ticketmaster_consumer_key
        self._api_secret: str = self._config.ticketmaster_consumer_secret

        self.mcp: FastMCP = FastMCP(
            name="ticket-discovery-management-server",
            version="1.2.0"
        )

        self.register_tools()

        self._logger = AppLogger.get_logger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, stream=sys.stderr, force=True)

    def run_stdio_transport(self) -> None:
        self.mcp.run(transport="stdio")

    def register_tools(self) -> None:

        @self.mcp.tool()
        async def fetch_filtered_events(
                keyword: str,
                target_date: str,
                target_venue: str,
                max_price: float
        ) -> list[dict[str, Any]] | str:
            """Retrieves a precise list of upcoming ticketed events that strictly match

            deterministic criteria values for a specific date, venue, and max price[cite: 183, 187].

            Args:
                keyword: The text keyword to search events by (e.g., 'New York Knicks').
                target_date: The exact date of the event in ISO format YYYY-MM-DD (e.g., '2026-06-09').
                target_venue: The required phrase or name of the venue (e.g., 'Madison Square Garden').
                max_price: The strict numerical upper cost limit ceiling (e.g., 50.00).
            """
            parameters_dict: dict[str, Any] = {
                "apikey": self._api_key,
                "keyword": keyword,
                "size": 10
            }

            try:
                sys.stderr.write(f"Hitting Ticketmaster for: '{keyword}'\n")
                sys.stderr.flush()

                # TODO: After testing uncomment this
                response = requests.get(url=Constants.TICKETMASTER_URL_ENDPOINT, params=parameters_dict)

                # # Resilient fallback handler to evaluate data structure mechanics seamlessly
                # if response.status_code in (401, 403) or self._api_key == "mock_key":
                #     raw_events = self._get_mock_ticketmaster_data()
                # else:
                #     response.raise_for_status()
                #     raw_events = self._parse_ticketmaster_payload(response.json())

                matching_events_list: list[dict[str, Any]] = self._get_matching_events_list(target_date=target_date,
                                                                                            target_venue=target_venue,
                                                                                            max_price=max_price)

                # MCP tools optimally return strings containing data or serialized JSON payloads

                return matching_events_list

            except RequestException as e:
                sys.stderr.write(f"[ERROR] Discovery collection break: {e}\n")
                sys.stderr.flush()
                return f"Error encountered while executing data fetch: {str(e)}"

    def _get_matching_events_list(self, target_date: str, target_venue: str, max_price: float) -> list[dict[str, Any]]:

        raw_events_list: list[dict[str, Any]] = Constants.TICKET_MASTER_MOCK_DATA

        matching_events_list: list[dict[str, Any]] = []
        for event_dict in raw_events_list:
            if event_dict.get("date") != target_date:
                continue

            if target_venue.lower() not in event_dict.get("venue", "").lower():
                continue

            if event_dict.get("price", 0.0) > max_price:
                continue

            matching_events_list.append(event_dict)

        return matching_events_list

    def _parse_ticketmaster_payload(self, payload_dict: dict[str, Any]) -> list[dict[str, Any]]:

        response_list: list[dict[str, Any]] = []
        if "_embedded" not in payload_dict:
            return response_list

        event_list: list[dict[str, Any]] = payload_dict["_embedded"].get("events", [])
        for event in event_list:
            try:
                # Safely parsing nested fields via fallback options
                name: str = event.get("name", "Unknown Event")
                date: str = event.get("dates", {}).get("start", {}).get("localDate", "Unknown Date")
                venue: str = event.get("_embedded", {}).get("venues", [{}])[0].get("name", "Unknown Venue")
                url: str = event.get("url", "")

                # Parsing standard price variations if present
                price_info = event.get("priceRanges", [{}])[0]
                current_price: float = float(price_info.get("min", 150.00))

                response_list.append({
                    "event_name": name,
                    "date": date,
                    "venue": venue,
                    "price": current_price,
                    "url": url
                })
            except (KeyError, ValueError):
                continue

        return response_list


if __name__ == "__main__":
    ticket_mcp_server: TicketMCPServer = TicketMCPServer()
    ticket_mcp_server.run_stdio_transport()
