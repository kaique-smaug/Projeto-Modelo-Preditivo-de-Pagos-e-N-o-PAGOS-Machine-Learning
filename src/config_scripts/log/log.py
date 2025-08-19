__version__ = '1.1.6'
from logging import getLogger, Formatter, FileHandler, DEBUG
from os.path import join

class LoggerSetup:
    """
    Logger setup class for handling log messages.

    Attributes:
        _pathLog (str): The directory where the log file will be stored.
        _nameLog (str): The name of the log file.
        _nameLogger (str): The name of the logger.
    """
    def __init__(self, pathLog, nameLog, nameLogger):
        """
        Initializes the LoggerSetup with the given log path, file name, and logger name.

        Args:
            pathLog (str): Path to the directory where the log file will be saved.
            nameLog (str): Name of the log file.
            nameLogger (str): Name of the logger instance.
        """
        self._pathLog = pathLog
        self._nameLog = nameLog
        self._nameLogger = nameLogger
        self._logger = self._setup_logger()

    def _setup_logger(self):
        """
            Configures the logger, including log format, file path, and log level.

            Returns:
                logging.Logger: Configured logger instance.
        """
        log_path = join(self._pathLog, self._nameLog)

        #Create logger
        logger = getLogger(self._nameLogger)

        #Prevent duplicate handlers
        if not logger.handlers:
            logger.setLevel(DEBUG)  # Default level

            #Create file handler
            file_handler = FileHandler(log_path)
            file_handler.setLevel(DEBUG)

            #Define log format
            formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            #Add handler to logger
            logger.addHandler(file_handler)

        return logger

    def debug_message(self, message):
        """Logs a debug message."""
        self._logger.debug(message)

    def info_message(self, message):
        """Logs an info message."""
        self._logger.info(message)

    def error_message(self, message):
        """Logs an error message."""
        self._logger.error(message)

    def warning_message(self, message):
        """Logs a warning message."""
        self._logger.warning(message)