from typing import Any

class Constants:
    LOGGER_COLOR_RESET: str = "\033[0m"
    LOGGER_COLOR_WHITE: str = "\033[60m"
    LOGGER_COLOR_ORANGE: str = "\033[33m"
    LOGGER_COLOR_DARK_RED: str = "\033[31m"

    TICKETMASTER_URL_ENDPOINT:str = "https://app.ticketmaster.com/discovery/v2/events.json"

    TICKET_MASTER_MOCK_DATA:list[dict[str, Any]] = [
            {
                "event_name": "NBA Finals: San Antonio Spurs at New York Knicks Game",
                "date": "2026-06-10",
                "venue": "Madison Square Garden",
                "price": 120.00,
                "url": "https://www.ticketmaster.com/mock-event-knicks-match"
            },
            {
                "event_name": "New York Knicks Home Game Watch Party Tickets",
                "date": "2026-06-10",
                "venue": "Madison Square Garden",
                "price": 45.00,
                "url": "https://www.ticketmaster.com/mock-event-knicks-watch-party"
            },

            {
                "event_name": "New York Knicks Home Game Watch Party Tickets",
                "date": "2026-06-10",
                "venue": "Madison Square Garden",
                "price": 20.00,
                "url": "https://www.ticketmaster.com/mock-event-knicks-watch-party"
            },
            {
                "event_name": "New York Knicks Concert Afterparty",
                "date": "2026-06-12",
                "venue": "Barclays Center",
                "price": 60.00,
                "url": "https://www.ticketmaster.com/mock-event-wrong-date"
            }
        ]