import pandas as pd
from db_operations import read_excel, write_excel
from validation import validate_user_login

# Загрузка данных
music_instruments = read_excel('database/music_instruments.xlsx')
customers = read_excel('database/customers.xlsx')
sellers = read_excel('database/sellers.xlsx')
sales = read_excel('database/sales.xlsx')
returns = read_excel('database/returns.xlsx')
search_criteria = read_excel('database/search_criteria.xlsx')

# Функция для авторизации
def authenticate_user(user_type, login, password):
    if user_type == 'customer':
        return validate_user_login(customers, login, password)
    elif user_type == 'seller':
        return validate_user_login(sellers, login, password)
    return False

# Функция для поиска инструмента
def search_instruments(criteria):
    filtered_instruments = music_instruments
    if criteria.get('Genre'):
        filtered_instruments = filtered_instruments[filtered_instruments['Genre'] == criteria['Genre']]
    if criteria.get('class'):
        filtered_instruments = filtered_instruments[filtered_instruments['class'] == criteria['class']]
    if criteria.get('Brand'):
        filtered_instruments = filtered_instruments[filtered_instruments['Brand'] == criteria['Brand']]
    return filtered_instruments
