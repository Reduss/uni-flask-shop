import time


def catch_error(func_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < 3:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Error in {func_name}: {e}")
                    print(f"Retrying in 1 second...")
                    time.sleep(1)
                    attempts += 1
            raise Exception("Max attempts(3) reached. Operation failed.")
        return wrapper
    return decorator