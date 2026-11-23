from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Главная страница магазина"""
    
    # Локаторы (уникальные для каждого элемента)
    LOGO = (By.CSS_SELECTOR, "img[alt='PrestaShop']")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='s']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CART_ICON = (By.CSS_SELECTOR, "div#_desktop_cart a")
    POPULAR_PRODUCTS = (By.CSS_SELECTOR, "section#popular-products")
    ALL_PRODUCTS_BUTTON = (By.CSS_SELECTOR, "a.all-product-link")
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, "div#_desktop_currency_selector")
    PRODUCT_GRID = (By.CSS_SELECTOR, "div.products.row")
    FOOTER = (By.CSS_SELECTOR, "footer#footer")
    CONTACT_LINK = (By.CSS_SELECTOR, "a[href*='contact']")
    
    def open_main_page(self):
        """Открыть главную страницу"""
        self.open("/")
    
    def get_all_products_prices(self):
        """
        Возвращает список цен всех товаров на главной странице
        """
        prices = self.driver.find_elements(By.CSS_SELECTOR, "span.price")
        return [price.text for price in prices if price.text]