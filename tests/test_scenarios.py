import pytest
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.currency_page import CurrencyPage
from selenium.webdriver.common.by import By


class TestUserScenarios:
    """Тесты для пользовательских сценариев"""
    
    def test_user_registration(self, driver, base_url):
        """
        Сценарий: Регистрация нового пользователя
        1. Открыть страницу регистрации
        2. Заполнить форму валидными данными
        3. Отправить форму
        4. Проверить, что регистрация прошла успешно
        """
        registration_page = RegistrationPage(driver, base_url)
        registration_page.open()
        
        # Генерируем уникальные данные
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_lowercase, k=6))
        email = f"test_{random_string}@example.com"
        
        # Заполняем форму
        registration_page.select_social_title("mr")
        registration_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email=email,
            password="SecurePass123!",
            birthday="1990-01-15"
        )
        
        # Принимаем согласия
        registration_page.accept_gdpr()
        registration_page.accept_customer_privacy()
        registration_page.subscribe_newsletter()
        
        # Отправляем форму
        success = registration_page.submit_registration()
        
        assert success, f"Регистрация не удалась. Ошибка: {registration_page.get_error_messages()}"
    
    def test_registration_without_gdpr(self, driver, base_url):
        """
        Сценарий: Регистрация без принятия GDPR (должна быть ошибка)
        1. Открыть страницу регистрации
        2. Заполнить форму
        3. Не принимать GDPR
        4. Отправить форму
        5. Проверить, что появилась ошибка
        """
        registration_page = RegistrationPage(driver, base_url)
        registration_page.open()
        
        # Заполняем форму без GDPR
        registration_page.select_social_title("mr")
        registration_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email="test_no_gdpr@example.com",
            password="SecurePass123!"
        )
        
        # Принимаем только privacy (без GDPR)
        registration_page.accept_customer_privacy()
        
        # Отправляем форму
        success = registration_page.submit_registration()
        
        # Ожидаем ошибку, так как GDPR не принят
        assert not success, "Регистрация прошла успешно, хотя GDPR не был принят"
        
        error = registration_page.get_error_messages()
        assert error is not None, "Нет сообщения об ошибке"
        assert "gdpr" in error.lower(), f"Неожиданное сообщение об ошибке: {error}"
    
    def test_currency_switch_on_main_page(self, driver, base_url):
        """
        Сценарий: Переключение валют на главной странице
        1. Открыть главную страницу
        2. Запомнить цены в текущей валюте
        3. Переключить на USD
        4. Проверить, что цены изменились
        5. Переключить на EUR
        6. Проверить, что цены вернулись
        """
        # Открываем главную страницу
        main_page = MainPage(driver, base_url)
        main_page.open_main_page()
        
        currency_page = CurrencyPage(driver, base_url)
        
        # Шаг 2: Запоминаем цены в EUR
        prices_eur = currency_page.get_all_prices()
        assert len(prices_eur) > 0, "Нет цен на главной странице"
        
        # Шаг 3: Переключаем на USD
        currency_page.switch_currency("USD")
        
        # Шаг 4: Проверяем, что цены изменились
        prices_usd = currency_page.get_all_prices()
        assert currency_page.are_prices_different(prices_eur, prices_usd), \
            "Цены не изменились при переключении на USD"
        
        # Проверяем символ валюты
        current_currency = currency_page.get_current_currency_symbol()
        assert current_currency == "USD", f"Ожидался USD, получен {current_currency}"
        
        # Шаг 5: Переключаем обратно на EUR
        currency_page.switch_currency("EUR")
        
        # Шаг 6: Проверяем, что цены вернулись
        prices_eur_after = currency_page.get_all_prices()
        assert prices_eur == prices_eur_after, \
            "Цены не вернулись к исходным после переключения обратно на EUR"
    
    def test_currency_switch_on_catalog(self, driver, base_url):
        """
        Сценарий: Переключение валют в каталоге
        1. Открыть каталог
        2. Запомнить цены
        3. Переключить валюту
        4. Проверить, что цены изменились
        """
        from pages.catalog_page import CatalogPage
        
        # Открываем каталог
        catalog_page = CatalogPage(driver, base_url)
        catalog_page.open_art_catalog()
        
        currency_page = CurrencyPage(driver, base_url)
        
        # Шаг 2: Запоминаем цены в текущей валюте
        prices_before = currency_page.get_all_prices()
        assert len(prices_before) > 0, "Нет цен в каталоге"
        
        # Шаг 3: Переключаем на USD
        currency_page.switch_currency("USD")
        
        # Шаг 4: Проверяем, что цены изменились
        prices_after = currency_page.get_all_prices()
        assert currency_page.are_prices_different(prices_before, prices_after), \
            "Цены не изменились в каталоге при переключении валюты"
    
    def test_multiple_currency_switches(self, driver, base_url):
        """
        Сценарий: Многократное переключение валют
        1. Открыть главную страницу
        2. Переключить EUR -> USD -> PLN -> EUR
        3. Проверить, что цены в начале и конце совпадают
        """
        main_page = MainPage(driver, base_url)
        main_page.open_main_page()
        
        currency_page = CurrencyPage(driver, base_url)
        
        # Запоминаем цены в EUR
        prices_start = currency_page.get_all_prices()
        
        # Переключаем валюты
        currency_page.switch_currency("USD")
        currency_page.switch_currency("PLN")
        currency_page.switch_currency("EUR")
        
        # Проверяем, что цены вернулись к исходным
        prices_end = currency_page.get_all_prices()
        assert prices_start == prices_end, \
            "Цены не вернулись к исходным после многократного переключения"