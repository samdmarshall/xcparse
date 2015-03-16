import logging
    
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class logging_helper(object):
    __metaclass__ = Singleton;
    _internal_logger = None;
    
    def __init__(self, *args, **kwargs):
        pass
    
    @staticmethod
    def getLogger():
        if logging_helper._internal_logger == None:
            logging_helper._internal_logger = logging.getLogger('com.samdmarshall.py.logging_helper');
            logging_helper._internal_logger.setLevel(logging.INFO);
            
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            
            # create formatter
            formatter = logging.Formatter('[%(levelname)s]%(message)s')
            
            # add formatter to ch
            ch.setFormatter(formatter)
            
            # add ch to logger
            logging_helper._internal_logger.addHandler(ch)
        return logging_helper._internal_logger;