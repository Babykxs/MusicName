import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd
from db_operations import read_excel
from logic import authenticate_user, search_instruments

# Загрузка данных из Excel
music_instruments = read_excel('database/music_instruments.xlsx')
sales = read_excel('database/sales.xlsx')
returns = read_excel('database/returns.xlsx')
search_criteria = read_excel('database/search_criteria.xlsx')


# Главный экран
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Информационная система музыкального магазина")

        self.label = tk.Label(root, text="Выберите роль:")
        self.label.pack(pady=10)

        self.customer_button = tk.Button(root, text="Покупатель", command=self.login_customer)
        self.customer_button.pack(pady=5)

        self.seller_button = tk.Button(root, text="Продавец", command=self.login_seller)
        self.seller_button.pack(pady=5)

    def login_customer(self):
        self.login_window("customer")

    def login_seller(self):
        self.login_window("seller")

    def login_window(self, user_type):
        login = simpledialog.askstring("Логин", "Введите логин:")
        password = simpledialog.askstring("Пароль", "Введите пароль:", show='*')

        if authenticate_user(user_type, login, password):
            messagebox.showinfo("Успех", f"Добро пожаловать, {user_type}!")
            if user_type == 'customer':
                self.customer_choice_window()
            else:
                self.seller_choice_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    # Окно выбора для покупателя
    def customer_choice_window(self):
        self.customer_window = tk.Toplevel(self.root)
        self.customer_window.title("Выберите действие")

        # Выбор критерия поиска
        search_button = tk.Button(self.customer_window, text="Поиск инструментов",
                                  command=self.search_instruments_window)
        search_button.pack(pady=5)

        # История покупок (список продаж)
        sales_button = tk.Button(self.customer_window, text="Мои покупки", command=self.view_sales_window)
        sales_button.pack(pady=5)

        # Возврат товара
        return_button = tk.Button(self.customer_window, text="Возврат инструмента",
                                  command=self.return_instrument_window)
        return_button.pack(pady=5)

    # Окно выбора для продавца
    def seller_choice_window(self):
        self.seller_window = tk.Toplevel(self.root)
        self.seller_window.title("Выберите действие")

        sales_button = tk.Button(self.seller_window, text="Продажа", command=self.manage_sales_window)
        sales_button.pack(pady=5)

        instruments_button = tk.Button(self.seller_window, text="Инструменты", command=self.manage_instruments_window)
        instruments_button.pack(pady=5)

    # Окно поиска инструментов для покупателя
    def search_instruments_window(self):
        self.search_window = tk.Toplevel(self.root)
        self.search_window.title("Поиск музыкальных инструментов")

        # Критерии поиска (жанр, класс, бренд)
        genre_label = tk.Label(self.search_window, text="Выберите жанр:")
        genre_label.pack(pady=5)
        self.genre_var = tk.StringVar(self.search_window)
        self.genre_var.set(search_criteria['Genre'].iloc[0])  # Default value
        genre_menu = tk.OptionMenu(self.search_window, self.genre_var, *search_criteria['Genre'].unique())
        genre_menu.pack(pady=5)

        class_label = tk.Label(self.search_window, text="Выберите класс:")
        class_label.pack(pady=5)
        self.class_var = tk.StringVar(self.search_window)
        self.class_var.set(search_criteria['class'].iloc[0])  # Default value
        class_menu = tk.OptionMenu(self.search_window, self.class_var, *search_criteria['class'].unique())
        class_menu.pack(pady=5)

        brand_label = tk.Label(self.search_window, text="Выберите бренд:")
        brand_label.pack(pady=5)
        self.brand_var = tk.StringVar(self.search_window)
        self.brand_var.set(search_criteria['Brand'].iloc[0])  # Default value
        brand_menu = tk.OptionMenu(self.search_window, self.brand_var, *search_criteria['Brand'].unique())
        brand_menu.pack(pady=5)

        search_button = tk.Button(self.search_window, text="Поиск", command=self.perform_search)
        search_button.pack(pady=10)

    # Выполнение поиска с фильтрацией по всем критериям
    def perform_search(self):
        genre = self.genre_var.get()
        class_ = self.class_var.get()
        brand = self.brand_var.get()

        # Фильтруем музыкальные инструменты по выбранным критериям
        filtered_instruments = music_instruments[
            (music_instruments['Genre'] == genre) &
            (music_instruments['class'] == class_) &
            (music_instruments['Brand'] == brand)
            ]

        if filtered_instruments.empty:
            messagebox.showinfo("Результаты поиска", "Нет инструментов, соответствующих выбранным критериям.")
        else:
            instruments_list = "\n".join(filtered_instruments['Name'])
            messagebox.showinfo("Результаты поиска", instruments_list)

    # Просмотр продаж (для покупателя)
    def view_sales_window(self):
        self.sales_window = tk.Toplevel(self.root)
        self.sales_window.title("Мои покупки")

        sales_list = "\n".join([
                                   f"ID: {row['ID']}, Продавец: {row['продавец']}, Дата: {row['дата продажи']}, Сумма: {row['кол-во всего'] * music_instruments.loc[music_instruments['ID'] == row['ID'], 'price'].values[0]}"
                                   for index, row in sales.iterrows()])
        sales_label = tk.Label(self.sales_window, text=sales_list)
        sales_label.pack(pady=10)

    # Окно возврата инструмента
    def return_instrument_window(self):
        self.return_window = tk.Toplevel(self.root)
        self.return_window.title("Возврат музыкального инструмента")

        # Выбор причины возврата
        reason_label = tk.Label(self.return_window, text="Выберите причину возврата:")
        reason_label.pack(pady=10)

        self.reason_var = tk.StringVar(self.return_window)
        self.reason_var.set("Не понравился")  # Default value
        reasons = ["Не понравился", "Не подошел размер", "Не работает"]
        reason_menu = tk.OptionMenu(self.return_window, self.reason_var, *reasons)
        reason_menu.pack(pady=5)

        submit_button = tk.Button(self.return_window, text="Оформить возврат", command=self.process_return)
        submit_button.pack(pady=10)

    # Обработка возврата
    def process_return(self):
        reason = self.reason_var.get()
        new_return = pd.DataFrame({
            'ID': [len(returns) + 1],
            'дата возврата': ['2025-01-06'],  # Примерная дата, можно использовать динамическую
            'причина': [reason]
        })
        # Добавляем новый возврат
        returns = returns.append(new_return, ignore_index=True)
        returns.to_excel('database/returns.xlsx', index=False)
        messagebox.showinfo("Возврат", "Товар возвращен в магазин")

    # Просмотр инструментов (для продавца)
    def manage_instruments_window(self):
        self.instruments_window = tk.Toplevel(self.root)
        self.instruments_window.title("Список музыкальных инструментов")

        instruments_list = "\n".join(music_instruments['Name'])
        instruments_label = tk.Label(self.instruments_window, text=instruments_list)
        instruments_label.pack(pady=10)

    # Просмотр продаж (для продавца)
    def manage_sales_window(self):
        self.sales_window = tk.Toplevel(self.root)
        self.sales_window.title("Продажи")

        sales_list = "\n".join([
                                   f"ID: {row['ID']}, Продавец: {row['продавец']}, Покупатель: {row['покупатель']}, Дата: {row['дата продажи']}"
                                   for index, row in sales.iterrows()])
        sales_label = tk.Label(self.sales_window, text=sales_list)
        sales_label.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
