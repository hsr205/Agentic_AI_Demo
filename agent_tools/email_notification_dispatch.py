import smtplib
from email.message import EmailMessage
from typing import Any

from logger.logger import AppLogger
from config.config import Settings

class EmailNotificationDispatcher:

    def __init__(self) -> None:
        self._config: Settings = Settings()
        self._gmail_user: str = "drexelword@gmail.com"
        self._gmail_app_password: str = self._config.google_app_password
        self._email_recipient_list: list[str] = ["rothenberg.h@northeastern.edu", "drexelword@gmail.com"]
        self._logger = AppLogger.get_logger(self.__class__.__name__)

    def execute_email_ticket_notification(self, matched_events: list[dict[str, Any]]) -> None:

        if not matched_events:
            self._logger.info("[DISPATCHER] Quiet termination triggered. Zero validated events passed.")
            return

        self._logger.info(f"Validated matches found: {len(matched_events)}")
        self._logger.info(f"Initiating secure Gmail SMTP transmission pipeline...")


        compiled_body_lines: list[str] = ["Greetings,\n\nOur agentic system located matching ticket deals:\n"]
        for index_num, event in enumerate(matched_events, 1):
            compiled_body_lines.append(f"{index_num}. {event.get('event_name', "No Event Name Provided")}")
            compiled_body_lines.append(f"   Price: ${float(event.get('price', 0.0)):.2f}")
            compiled_body_lines.append(f"   Link:  {event.get('url', "No URL Provided")}\n")
        compiled_body_lines.append("Best regards,\nAutomated Agent Core Engine")
        email_body_str: str = "\n".join(compiled_body_lines)

        self._email_recipients(email_body_str=email_body_str)

    def _email_recipients(self, email_body_str: str) -> None:

        for email_recipient in self._email_recipient_list:

            msg: EmailMessage = EmailMessage()
            msg['Subject'] = 'ALERT: Verified Ticket Deals Located'
            msg['From'] = self._gmail_user
            msg['To'] = email_recipient
            msg.set_content(email_body_str)

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(self._gmail_user, self._gmail_app_password)
                    smtp.send_message(msg)
                self._logger.info(f"Successfully email alert to: {email_recipient}")
            except Exception as e:
                self._logger.exception(f"[CRITICAL FAILURE] Transmission aborted to {email_recipient}: {str(e)}")
