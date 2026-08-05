import main


def test_prep_format_sort_sample_transactions():
    transaction = {
        "date": "2019-12-08T22:46:21.935582",
        "description": "Открытие вклада",
        "operationAmount": {
            "amount": "40542",
            "currency": {"code": "RUB"}
        },
        "to": "Счет 90424923579946435907"
    }

    gen = iter(["Открытие вклада"])

    result = main.prep_format_sort_sample_transactions(transaction, gen)

    assert "08.12.2019" in result
    assert "40542 RUB" in result


def test_main_wrong_status(monkeypatch, capsys):
    answers = iter([
        "1",
        "test",
        "EXECUTED",
        "нет",
        "нет",
        "нет"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(
        "main.djecson_from_path",
        lambda _: []
    )

    main.main()

    captured = capsys.readouterr()

    assert "недоступен" in captured.out.lower()


def test_empty_transactions(monkeypatch, capsys):
    answers = iter([
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "нет"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(
        "main.djecson_from_path",
        lambda _: []
    )

    main.main()

    captured = capsys.readouterr()

    assert "не найдено ни одной транзакции" in captured.out.lower()


def test_main_json_selected(monkeypatch, capsys):
    answers = iter([
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "нет"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(
        "main.djecson_from_path",
        lambda _: []
    )

    main.main()

    captured = capsys.readouterr()

    assert "для обработки выбран json-файл" in captured.out.lower()
