from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Страница регистрации"""
    
    # Локаторы
    SOCIAL_TITLE_MR = (By.CSS_SELECTOR, "input#field-id_gender-1")
    SOCIAL_TITLE_MRS = (By.CSS_SELECTOR, "input#field-id_gender-2")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input#field-firstname")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input#field-lastname")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#field-email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#field-password")
    BIRTHDAY_INPUT = (By.CSS_SELECTOR, "input#field-birthday")
    NEWSLETTER_CHECKBOX = (By.CSS_SELECTOR, "input[name='newsletter']")
    GDPR_CHECKBOX = (By.CSS_SELECTOR, "input[name='psgdpr']")
    CUSTOMER_PRIVACY_CHECKBOX = (By.CSS_SELECTOR, "input[name='customer_privacy']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login']")
    FORM_TITLE = (By.CSS_SELECTOR, "h1.h1")
    
    def open_registration_page(self):
        """Открыть страницу регистрации"""
        self.open("/registration")