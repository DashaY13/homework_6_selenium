from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CurrencyPage(BasePage):
    """
    PageObject для работы с переключением валют на главной странице
    """
    
    # Локаторы
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "div#_desktop_currency_selector")
    CURRENCY_EUR = (By.CSS_SELECTOR, "a[href*='currency=1']")
    CURRENCY_USD = (By.CSS_SELECTOR, "a[href*='currency=2']")
    CURRENCY_PLN = (By.CSS_SELECTOR, "a[href*='currency=3']")
    CURRENCY_OPTIONS = (By.CSS_SELECTOR, "div#_desktop_currency_selector ul li a")
    
    # Цены товаров
    PRODUCT_PRICES = (By.CSS_SELECTOR, "span.price")
    CURRENT_CURRENCY_SYMBOL = (By.CSS_SELECTOR, "span.price")
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
    
    def open_currency_dropdown(self):
        """Открыть выпадающий список валют"""
        dropdown = self.find_clickable(self.CURRENCY_DROPDOWN)
        dropdown.click()
        # Ждем появления опций
        self.wait.until(
            EC.visibility_of_element_located(self.CURRENCY_OPTIONS)
        )
    
    def switch_currency(self, currency_code="USD"):
        """
        Переключить валюту
        :param currency_code: Код валюты (EUR, USD, PLN)
        """
        self.open_currency_dropdown()
        
        # Выбираем нужную валюту
        currency_map = {
            "EUR": self.CURRENCY_EUR,
            "USD": self.CURRENCY_USD,
            "PLN": self.CURRENCY_PLN
        }
        
        if currency_code.upper() in currency_map:
            currency_option = self.find_clickable(currency_map[currency_code.upper()])
            currency_option.click()
            # Ждем обновления страницы
            self.wait_for_currency_update()
    
    def wait_for_currency_update(self):
        """Дождаться обновления цен после смены валюты"""
        self.wait.until(
            EC.presence_of_all_elements_located(self.PRODUCT_PRICES)
        )
    
    def get_all_prices(self):
        """
        Получить список всех цен на странице
        :return: List[str] - список цен в текстовом формате
        """
        prices = self.driver.find_elements(*self.PRODUCT_PRICES)
        return [price.text for price in prices if price.text.strip()]
    
    def get_first_price(self):
        """Получить цену первого товара"""
        prices = self.get_all_prices()
        return prices[0] if prices else None
    
    def get_current_currency_symbol(self):
        """
        Определить текущую валюту по символу в цене
        :return: str - символ валюты ($, €, zł)
        """
        first_price = self.get_first_price()
        if first_price:
            if '€' in first_price:
                return 'EUR'
            elif '$' in first_price:
                return 'USD'
            elif 'zł' in first_price:
                return 'PLN'
        return 'UNKNOWN'
    
    def are_prices_different(self, prices_before, prices_after):
        """
        Проверить, отличаются ли цены после смены валюты
        :param prices_before: Цены до смены
        :param prices_after: Цены после смены
        :return: bool
        """
        if not prices_before or not prices_after:
            return False
        if len(prices_before) != len(prices_after):
            return True
        
        # Сравниваем цены (они могут отличаться из-за округления)
        return prices_before != prices_after