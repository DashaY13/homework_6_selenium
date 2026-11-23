from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница логина в админку"""
    
    # Локаторы
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#passwd")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button#submit_login")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href*='password']")
    LOGO_IMAGE = (By.CSS_SELECTOR, "img[alt='PrestaShop']")
    LANGUAGE_SELECTOR = (By.CSS_SELECTOR, "select#language")
    LOGIN_FORM = (By.CSS_SELECTOR, "form#login_form")
    SHOP_LINK = (By.CSS_SELECTOR, "a[href*='shop.prestashop.com']")
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href*='registration']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    
    def open_login_page(self):
        """Открыть страницу логина"""
        self.open("/administration")
    
    def login(self, email, password):
        """Выполнить логин"""
        self.find(self.EMAIL_INPUT).send_keys(email)
        self.find(self.PASSWORD_INPUT).send_keys(password)
        self.find_clickable(self.LOGIN_BUTTON).click()