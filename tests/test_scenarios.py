import pytest
from pages.main_page import MainPage
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class TestAdminLogin:
    """Тесты для админки"""
    
    def test_admin_login_logout(self, driver, base_url):
        """
        Сценарий: 
        1. Открыть страницу логина админки
        2. Ввести корректные данные (по умолчанию: admin@admin.com / admin123)
        3. Нажать Login
        4. Проверить, что мы попали в дашборд (виден элемент)
        5. Выполнить logout
        6. Проверить, что вернулись на страницу логина
        """
        login_page = LoginPage(driver, base_url)
        login_page.open_login_page()
        
        # Шаг 2: Логинимся
        login_page.login("admin@admin.com", "admin123")
        
        # Шаг 3: Ждем загрузки дашборда и проверяем
        dashboard_element = (By.CSS_SELECTOR, "h1.dashboard-title")
        assert login_page.is_element_present(dashboard_element), \
            "Не удалось залогиниться: дашборд не загрузился"
        
        # Шаг 4: Находим кнопку выхода (обычно это иконка пользователя)
        # В PrestaShop она может быть в верхнем правом углу
        logout_button = (By.CSS_SELECTOR, "a.logout")
        logout_element = login_page.find_clickable(logout_button)
        logout_element.click()
        
        # Шаг 5: Проверяем, что снова на странице логина
        assert login_page.is_element_present(login_page.LOGIN_FORM), \
            "Не удалось разлогиниться: форма логина не появилась"
    
    def test_add_random_product_to_cart(self, driver, base_url):
        """
        Сценарий:
        1. Открыть главную страницу
        2. Выбрать случайный товар из списка популярных
        3. Кликнуть на него, чтобы открыть карточку
        4. Добавить в корзину
        5. Перейти в корзину
        6. Проверить, что товар там есть (по названию)
        """
        from pages.product_page import ProductPage
        
        # Шаг 1: Открываем главную
        main_page = MainPage(driver, base_url)
        main_page.open_main_page()
        
        # Шаг 2: Получаем список товаров на главной
        products = driver.find_elements(By.CSS_SELECTOR, "div.product-miniature")
        assert len(products) > 0, "Нет товаров на главной странице"
        
        # Выбираем случайный товар
        import random
        random_product = random.choice(products)
        product_name = random_product.find_element(By.CSS_SELECTOR, "h3.h3.product-title a").text
        
        # Кликаем на товар
        random_product.click()
        
        # Шаг 3: Теперь мы на странице товара
        product_page = ProductPage(driver, base_url)
        
        # Шаг 4: Добавляем в корзину
        product_page.add_to_cart()
        
        # Шаг 5: Ждем появления модального окна с подтверждением и переходим в корзину
        cart_modal = (By.CSS_SELECTOR, "div#blockcart-modal")
        product_page.wait.until(EC.visibility_of_element_located(cart_modal))
        
        # Нажимаем на кнопку "Перейти в корзину"
        go_to_cart_button = product_page.find_clickable(
            (By.CSS_SELECTOR, "a.btn-primary[href*='cart']")
        )
        go_to_cart_button.click()
        
        # Шаг 6: Проверяем, что товар в корзине
        cart_product_name = (By.CSS_SELECTOR, "div.cart-items .product-line-info a.label")
        product_in_cart = driver.find_element(*cart_product_name).text
        assert product_name in product_in_cart, \
            f"Товар '{product_name}' не найден в корзине. Найден: '{product_in_cart}'"
    
    def test_currency_change_main_page(self, driver, base_url):
        """
        Сценарий:
        1. Открыть главную страницу
        2. Запомнить цены в текущей валюте (EUR)
        3. Переключить валюту на USD
        4. Проверить, что цены изменились
        5. Переключить на PLN
        6. Проверить, что цены снова изменились
        """
        main_page = MainPage(driver, base_url)
        main_page.open_main_page()
        
        # Шаг 2: Получаем цены в EUR
        prices_eur = main_page.get_all_products_prices()
        assert len(prices_eur) > 0, "Не удалось получить цены на главной"
        
        # Шаг 3: Переключаем валюту на USD
        # В PrestaShop обычно есть выпадающий список валют
        currency_selector = main_page.find_clickable(main_page.CURRENCY_DROPDOWN)
        currency_selector.click()
        
        # Выбираем USD (предположим, что это 2-й элемент в списке)
        usd_option = main_page.find_clickable((By.CSS_SELECTOR, "a[href*='currency=2']"))
        usd_option.click()
        
        # Ждем обновления страницы и снова получаем цены
        driver.implicitly_wait(2)  # Небольшая пауза для обновления
        prices_usd = main_page.get_all_products_prices()
        
        # Шаг 4: Проверяем, что цены изменились
        assert prices_eur != prices_usd, "Цены не изменились при переключении на USD"
        
        # Шаг 5: Переключаем на PLN (3-я валюта)
        currency_selector = main_page.find_clickable(main_page.CURRENCY_DROPDOWN)
        currency_selector.click()
        pln_option = main_page.find_clickable((By.CSS_SELECTOR, "a[href*='currency=3']"))
        pln_option.click()
        
        # Снова паузим и проверяем
        driver.implicitly_wait(2)
        prices_pln = main_page.get_all_products_prices()
        
        # Шаг 6: Проверяем, что цены отличаются от EUR
        assert prices_eur != prices_pln, "Цены не изменились при переключении на PLN"
    
    def test_currency_change_catalog(self, driver, base_url):
        """
        Сценарий:
        1. Открыть каталог Art
        2. Запомнить цены в EUR
        3. Переключить валюту на USD
        4. Проверить, что цены изменились
        """
        from pages.catalog_page import CatalogPage
        
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.open_art_catalog()
        
        # Шаг 2: Получаем цены в EUR
        prices_eur = catalog_page.get_all_product_prices()
        assert len(prices_eur) > 0, "Не удалось получить цены в каталоге"
        
        # Шаг 3: Переключаем валюту
        main_page = MainPage(driver, base_url)
        currency_selector = main_page.find_clickable(main_page.CURRENCY_DROPDOWN)
        currency_selector.click()
        
        usd_option = main_page.find_clickable((By.CSS_SELECTOR, "a[href*='currency=2']"))
        usd_option.click()
        
        # Шаг 4: Проверяем изменение цен
        driver.implicitly_wait(2)
        prices_usd = catalog_page.get_all_product_prices()
        
        assert prices_eur != prices_usd, f"Цены не изменились в каталоге! Было: {prices_eur[:3]}, стало: {prices_usd[:3]}"