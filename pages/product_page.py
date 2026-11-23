from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Карточка товара"""
    
    # Локаторы
    PRODUCT_NAME = (By.CSS_SELECTOR, "h1.h1")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "span.current-price")
    PRODUCT_DESCRIPTION = (By.CSS_SELECTOR, "div#product-description")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-button-action='add-to-cart']")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input#quantity_wanted")
    SIZE_SELECTOR = (By.CSS_SELECTOR, "select#group_1")
    COLOR_SELECTORS = (By.CSS_SELECTOR, "ul#group_2 li")
    PRODUCT_IMAGES = (By.CSS_SELECTOR, "ul.product-images")
    SHARE_BUTTON = (By.CSS_SELECTOR, "button[data-share-url]")
    PRODUCT_REFERENCE = (By.CSS_SELECTOR, "span[itemprop='sku']")
    
    def open_product(self, product_id=1):
        """Открыть страницу товара (по id)"""
        self.open(f"/art/{product_id}-product-name.html")
    
    def add_to_cart(self):
        """Добавить товар в корзину"""
        add_btn = self.find_clickable(self.ADD_TO_CART_BUTTON)
        add_btn.click()