"""Custom logging handler"""

import datetime
import logging

from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class CustomLogger(logging.StreamHandler):
    """Custom logging handler class"""

    def __init__(self):
        """Constructor"""
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        """Emitting messages"""
        try:
            msg = self.format(record)
            stream = self.stream

            # Displaying messages without new line
            msg = msg.replace("\n", "\r")

            stream.write(msg)
            stream.write(self.terminator)
            self.flush()

        except Exception:  # noqa: BLE001
            self.handleError(record)


def format_message(message):
    """Format log message"""
    d = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")
    return f"*{d}*: {message}"


class SlackLogger(logging.Handler):
    """Class to log to slack"""

    def __init__(self):
        """Call parent constructor"""
        logging.Handler.__init__(self)

    def emit(self, record):
        """Override emit method"""
        # send emails only in production env

        message = format_message(record.getMessage())
        message = message.replace("\n", "\r")

        # Send a slack message only if it comes from an app
        try:
            # Try sending the error log directly to Slack
            slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)
            slack_client.chat_postMessage(
                channel=settings.SLACK_BOT_CHANNEL,
                text=message,
            )

        except SlackApiError:
            # Send the error log via e-mail if sending to slack fails
            # override credentials from config
            pass
