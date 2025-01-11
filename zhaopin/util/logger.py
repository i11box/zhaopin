import logging

def MethodLogging(func):
    def wrapper(*args, **kwargs):
        logging.info(f"处理 {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"结束 {func.__name__}")
        return result
    return wrapper

def ClassMethodLogging(func):
    def wrapper(*args, **kwargs):
        # 排除 self 参数
        filtered_args = args[1:] if len(args) > 0 else args
        logging.info(f"处理 {func.__name__} with args: {filtered_args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"结束 {func.__name__}")
        return result
    return wrapper

class Logger:

    def __init__(self) -> None:
        pass
    
    @staticmethod
    def info(msg):
        logging.info(msg)
        
    @staticmethod
    def error(msg):
        logging.error(msg)