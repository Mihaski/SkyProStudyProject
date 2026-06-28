from datetime import datetime
from functools import wraps


def log(filename: str = "stdout"):
    """ Decorator for logging functions """

    def decorator_log(func):
        @wraps(func)
        def my_wrapper(*args, **kwargs):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Формируем строку с аргументами
            args_str = ', '.join(repr(arg) for arg in args)
            kwargs_str = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())
            all_args = ', '.join(filter(None, [args_str, kwargs_str]))

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                log_message = (f"[{timestamp}] УСПЕХ: {func.__name__}({all_args}) -> {repr(result)}\n"
                )

                # Записываем лог
                if filename != "stdout":
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                log_message = (
                    f"[{timestamp}] ОШИБКА: {func.__name__}({all_args}) -> "
                    f"{type(e).__name__}: {str(e)}\n"
                )

                # Записываем лог
                if filename != "stdout":
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

                # Перебрасываем исключение дальше, чтобы поведение было ожидаемым
                raise

        return my_wrapper

    return decorator_log
