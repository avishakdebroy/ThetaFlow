"""
Module: utils
Purpose: Provides helper functions such as logging configuration.
"""

import logging
import os


def setup_logging(log_file="logs/run_logs.txt"):
    """
    Sets up the logging configuration. Logs are saved to the specified file.

    Args:
        log_file (str): Path to the log file.
    """
    # Ensure the logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logging.basicConfig(filename=log_file,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        filemode='a')


def log_message(message):
    """
    Logs a message at the INFO level.

    Args:
        message (str): The message you wish to log.
    """
    logging.info(message)
