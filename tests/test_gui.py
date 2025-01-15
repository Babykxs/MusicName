import pytest
import tkinter as tk
from gui import MainWindow
from logic import authenticate_user
import pandas as pd


@pytest.fixture
def app():
    root = tk.Tk()
    app = MainWindow(root)
    yield app
    root.destroy()


# Тестирование окна входа
def test_login_success(app, monkeypatch):
    def mock_authenticate(user_type, login, password):
        return True

    monkeypatch.setattr("logic.authenticate_user", mock_authenticate)
    monkeypatch.setattr("tkinter.simpledialog.askstring", lambda *args, **kwargs: "admin")

    app.login_window("customer")
    assert app.customer_window.winfo_exists() == 1


def test_login_failure(app, monkeypatch):
    def mock_authenticate(user_type, login, password):
        return False

    monkeypatch.setattr("logic.authenticate_user", mock_authenticate)
    monkeypatch.setattr("tkinter.simpledialog.askstring", lambda *args, **kwargs: "wrong_pass")

    app.login_window("customer")
    assert "Ошибка" in app.root.call("tk_messageBox", "info", "message")


# Тестирование поиска инструментов
def test_instrument_search(app, monkeypatch):
    # Создаем фиктивную базу данных инструментов
    mock_db = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Гитара Fender', 'Барабан Yamaha', 'Пианино Casio'],
        'Genre': ['Rock', 'Jazz', 'Classical'],
        'class': ['string', 'percussion', 'keyboard'],
        'Brand': ['Fender', 'Yamaha', 'Casio']
    })

    monkeypatch.setattr("db_operations.read_excel", lambda x: mock_db)

    app.search_instruments_window()
    app.genre_var.set('Rock')
    app.class_var.set('string')
    app.brand_var.set('Fender')

    app.perform_search()
    assert "Гитара Fender" in app.root.call("tk_messageBox", "info", "message")


def test_search_no_results(app, monkeypatch):
    # Пустая база данных
    mock_db = pd.DataFrame({
        'ID': [],
        'Name': [],
        'Genre': [],
        'class': [],
        'Brand': []
    })

    monkeypatch.setattr("db_operations.read_excel", lambda x: mock_db)

    app.search_instruments_window()
    app.genre_var.set('Rock')
    app.class_var.set('string')
    app.brand_var.set('Fender')

    app.perform_search()
    assert "Нет инструментов" in app.root.call("tk_messageBox", "info", "message")


# Тестирование возврата
def test_return_instrument(app, monkeypatch):
    return_db = pd.DataFrame({
        'ID': [1],
        'дата возврата': ['2024-01-05'],
        'причина': ['Не понравился']
    })

    def mock_to_excel(*args, **kwargs):
        pass

    monkeypatch.setattr("db_operations.read_excel", lambda x: return_db)
    monkeypatch.setattr("pandas.DataFrame.to_excel", mock_to_excel)

    app.return_instrument_window()
    app.reason_var.set('Не работает')
    app.process_return()

    assert "Товар возвращен в магазин" in app.root.call("tk_messageBox", "info", "message")
