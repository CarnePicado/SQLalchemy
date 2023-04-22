import os
import logging

def logger(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(level=logging.INFO, filename='main.log', filemode='w',
        format=Log_Format)
        logger = logging.getLogger()
        logger.info(f'''
        Function name: {old_function.__name__}
        Arguments name: {args} and {kwargs}.
        Function has been returned: {result}.
        ''')
        return result
    return new_function