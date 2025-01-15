import pandas as pd

# Создание таблицы "Музыкальный инструмент"
def create_music_instruments():
    data = {
        'ID': [1, 2, 3, 4],
        'Name': ['Гитара', 'Барабаны', 'Фортепиано', 'Скрипка'],
        'Brand': ['Fender', 'Pearl', 'Yamaha', 'Stradivarius'],
        'Genre': ['Рок', 'Рок', 'Классика', 'Классика'],
        'class': ['Электрическая', 'Активная', 'Акустическая', 'Струнная'],
        'price': [15000, 25000, 45000, 100000]
    }
    df = pd.DataFrame(data)
    df.to_excel('database/music_instruments.xlsx', index=False)
    print("Таблица 'Музыкальный инструмент' создана.")

# Создание таблицы "Покупатель"
def create_customers():
    data = {
        'ID': [1, 2],
        'Login': ['customer1', 'customer2'],
        'password': ['pass1', 'pass2']
    }
    df = pd.DataFrame(data)
    df.to_excel('database/customers.xlsx', index=False)
    print("Таблица 'Покупатель' создана.")

# Создание таблицы "Продавец"
def create_sellers():
    data = {
        'ID': [1, 2],
        'Login': ['seller1', 'seller2'],
        'password': ['pass1', 'pass2']
    }
    df = pd.DataFrame(data)
    df.to_excel('database/sellers.xlsx', index=False)
    print("Таблица 'Продавец' создана.")

# Создание таблицы "Продажа"
def create_sales():
    data = {
        'ID': [1, 2],
        'дата продажи': ['2025-01-01', '2025-01-02'],
        'кол-во всего': [1, 2],
        'продавец': ['seller1', 'seller2'],
        'покупатель': ['customer1', 'customer2']
    }
    df = pd.DataFrame(data)
    df.to_excel('database/sales.xlsx', index=False)
    print("Таблица 'Продажа' создана.")

# Создание таблицы "Возврат"
def create_returns():
    data = {
        'ID': [1, 2],
        'дата возврата': ['2025-01-05', '2025-01-06'],
        'причина': ['Не понравился', 'Не подошел размер']
    }
    df = pd.DataFrame(data)
    df.to_excel('database/returns.xlsx', index=False)
    print("Таблица 'Возврат' создана.")

# Создание таблицы "Критерии поиска"
def create_search_criteria():
    data = {
        'ID': [1, 2],
        'Genre': ['Рок', 'Классика'],
        'class': ['Электрическая', 'Струнная'],
        'Brand': ['Fender', 'Yamaha']
    }
    df = pd.DataFrame(data)
    df.to_excel('database/search_criteria.xlsx', index=False)
    print("Таблица 'Критерии поиска' создана.")

# Основная функция для создания всех таблиц
def create_all_databases():
    create_music_instruments()
    create_customers()
    create_sellers()
    create_sales()
    create_returns()
    create_search_criteria()

# Вызов функции для создания баз данных
if __name__ == "__main__":
    create_all_databases()
