import logging
import threading

_logger = None
_logger_lock = threading.Lock()
UNITY_FORMAT='{asctime} {levelname} [{name}] [{filename}:{lineno}] {message}'
BASIC_FORMAT='{levelname}:{name}:{filename}:{lineno}:{message}'

def get_logger(level=logging.INFO,
               fmt=BASIC_FORMAT,
               dtfmt = '%Y-%m-%d %H:%M:%S',
               stream = True,
               filename=None,
               ):
    """
    - Create a logger if not present with name ezai
    - Set the formatting of the logger and of root logger
    - Adds stream and file hndlers
    - Removes the propagation of messages to root logger
    :param level:
    :param fmt:
    :param dtfmt:
    :param stream:
    :param filename:
    :return:
    """
    global _logger

    if _logger:
        return _logger

    _logger_lock.acquire()

    try:
#    if _logger is None:
        logger_name='ezai'
        _logger = logging.getLogger(name=logger_name)
        _logger.propagate=False
        logging.basicConfig(level=level, format=fmt, datefmt=dtfmt,style='{')
        #logging.basicConfig(format=format)
        #logger.handlers[0].stream=sys_stdout
        formatter = logging.Formatter(fmt, dtfmt, style='{')
        if filename:
            addFileHandler(filename,formatter)
        if stream:
            addStreamHandler(formatter)
        _logger.setLevel(level)
    finally:
        _logger_lock.release()

    return _logger

def addFileHandler(filename, formatter, logger_name='ezai'):
    _logger = logging.getLogger(name=logger_name)
    handler = logging.FileHandler()
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

def addStreamHandler(formatter, logger_name='ezai'):
    _logger = logging.getLogger(name=logger_name)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

def log_and_raise(exception: Exception, logger: logging.Logger = get_logger()):
    """
    Can be used to replace "raise" when throwing an exception to ensure the logging
    of the exception. After logging it, the exception is raised.
    Parameters
    ----------
    exception
        The exception instance to be raised.
    logger
        The logger instance to log the exception type and message.
    Raises
    ------
    Exception
        The provided exception
    """

    exception_type = str(type(exception)).split("'")[1]
    message = str(exception)
    logger.error(exception_type + ": " + message)

    raise exception

def list_loggers():
    for k,v in  logging.Logger.manager.loggerDict.items()  :
        print('+ [%s] {%s} ' % (str.ljust( k, 20)  , str(v.__class__)[8:-2]) )
        if not isinstance(v, logging.PlaceHolder):
            for h in v.handlers:
                print('     +++',str(h.__class__)[8:-2] )
