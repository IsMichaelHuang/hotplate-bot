"""
Configuration module for the Hotplate bot.

Loads environment variables from a .env file at startup and exposes them
as a single shared `config` instance. Any missing variable raises a
ValueError immediately, preventing silent failures during runtime.

Usage:
    from bot.config import config

    config.WEBSITE_URL
    config.CARD_NUMBER
"""

from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """
    Holds all environment-based configuration for the bot.

    Attributes:
        WEBSITE_URL (str): Target vendor URL on Hotplate.
        NUMBER (str): Phone number used for checkout verification.
        CARD_NUMBER (str): Payment card number.
        EXPIRY (str): Card expiry date in MMYY format.
        CVC (str): Card security code.
        POSTAL (str): Billing postal/ZIP code.
    """

    def __init__(self):
        self.WEBSITE_URL = self._get("WEBSITE_URL")
        self.NUMBER      = self._get("NUMBER")
        self.CARD_NUMBER = self._get("CARD_NUMBER")
        self.EXPIRY      = self._get("EXPIRY")
        self.CVC         = self._get("CVC")
        self.POSTAL      = self._get("POSTAL")

    def _get(self, key):
        """Fetch an environment variable, raising an error if it is missing."""
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Missing environment variable: {key}")
        return value

config = Config()
