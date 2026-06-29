import pytest

from decorators import my_log


def test_log_to_stdout_success(capsys):
    """Тест успешного выполнения с выводом в консоль"""

    @my_log()
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5
    captured = capsys.readouterr()
    assert "Начало работы add" in captured.out
    assert "add ok" in captured.out
    assert "Конец работы add" in captured.out


def test_log_to_stdout_exception(capsys):
    """Тест обработки исключения с выводом в консоль"""

    @my_log()
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "Начало работы divide" in captured.out
    assert "divide error: ZeroDivisionError. Inputs: (10, 0)" in captured.out
    assert "Конец работы divide" in captured.out


def test_log_to_stdout_exception_with_kwargs(capsys):
    """Тест обработки исключения с именованными аргументами в консоль"""

    @my_log()
    def faulty_function(value, multiplier=1):
        return value / multiplier

    with pytest.raises(ZeroDivisionError):
        faulty_function(10, multiplier=0)

    captured = capsys.readouterr()
    assert "faulty_function error: ZeroDivisionError. Inputs: (10, multiplier=0)" in captured.out


def test_log_to_file_success(tmp_path):
    """Тест успешного выполнения функции с записью в файл"""
    log_file = tmp_path / "test.log"
    filename = str(log_file)

    @my_log(filename)
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5
    assert log_file.exists()

    content = log_file.read_text(encoding='utf-8')
    assert "Начало работы add" in content
    assert "add ok" in content
    assert "Конец работы add" in content
    # Проверяем порядок
    lines = content.strip().split('\n')
    assert lines[0] == "Начало работы add"
    assert lines[1] == "add ok"
    assert lines[2] == "Конец работы add"


def test_log_to_file_exception(tmp_path):
    """Тест обработки исключения с записью в файл"""
    log_file = tmp_path / "test.log"
    filename = str(log_file)

    @my_log(filename)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    content = log_file.read_text(encoding='utf-8')
    assert "Начало работы divide" in content
    assert "divide error: ZeroDivisionError. Inputs: (10, 0)" in content
    assert "Конец работы divide" in content


# noinspection PyNoneFunctionAssignment
def test_log_function_returns_none(capsys):
    """Тест функции, возвращающей None"""

    @my_log()
    def do_nothing():
        pass

    result = do_nothing()
    assert result is None

    captured = capsys.readouterr()
    assert "do_nothing ok" in captured.out


def test_log_function_without_args(capsys):
    """Тест функции без аргументов"""

    @my_log()
    def say_hello():
        return "Hello!"

    result = say_hello()
    assert result == "Hello!"

    captured = capsys.readouterr()
    assert "Начало работы say_hello" in captured.out
    assert "say_hello ok" in captured.out
    assert "Конец работы say_hello" in captured.out
