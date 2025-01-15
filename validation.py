import pandas as pd

# Проверка логина и пароля
def validate_user_login(df, login, password):
    user = df[(df['Login'] == login) & (df['password'] == password)]
    return not user.empty
