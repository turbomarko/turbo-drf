"""Custom logging handler"""
import logging


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

        except Exception:
            self.handleError(record)
