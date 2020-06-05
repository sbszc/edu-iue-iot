# --*-- built-in packages --*--
import logging
import logging.handlers
import sys

# --*-- Installed packages --*--

# --*-- own packages --*--

def create_log(log_name, level = logging.INFO):
    
    # # create logger
    if len(sys.argv)==2:
        if sys.argv[1].lower() == "info":
            level = logging.INFO
        elif sys.argv[1].lower() == "debug":
            level = logging.DEBUG
        elif sys.argv[1].lower() == "warning":
            level = logging.WARNING
        else:
            print("Argument not recognized...")
            print("Setting DEBUG level")
            level = logging.DEBUG

    # # logger = logging.getLogger(__name__)
    logger = logging.getLogger(log_name)
    logger.setLevel(level)
    # # create formatter
    detailed_formatter = logging.Formatter(
        "%(asctime)s %(name)s[%(process)d] %(funcName)s(): "+\
        "%(levelname)s - %(message)s")

    #  # create a console handler
    # # and set its log level to the command-line option
    # #
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(detailed_formatter)

    # # create a file handler
    # # and set its log level to DEBUG
    # #
    file_handler = logging.handlers.TimedRotatingFileHandler(
        f'logs/{log_name}.log', 'midnight', 1, 30)
    file_handler.setLevel(level)
    file_handler.setFormatter(detailed_formatter)

    # # add handlers to the "mypackage" logger
    # #
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
