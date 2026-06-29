from functools import wraps

from utils import write_or_print


def my_log(filename: str = "stdout"):
    """ Decorator for logging functions """

    def decorator_log(func):
        @wraps(func)
        def my_wrapper(*args, **kwargs):

            # Формируем строку с аргументами
            args_str = ', '.join(repr(arg) for arg in args)
            kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))

            try:
                begin_message = f"Начало работы {func.__name__}\n"
                write_or_print(begin_message, filename)

                result = func(*args, **kwargs)

                log_message = f"{func.__name__} ok\n"

                # Записываем лог
                write_or_print(log_message, filename)

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: ({all_args})\n"

                # Записываем лог
                write_or_print(log_message, filename)

                # Перебрасываем исключение дальше, чтобы поведение было ожидаемым
                raise
            finally:
                end_message = f"Конец работы {func.__name__}\n"
                write_or_print(end_message, filename)

        return my_wrapper

    return decorator_log
