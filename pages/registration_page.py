from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
import random
import string


class RegistrationPage(BasePage):
    """
    PageObject для страницы регистрации пользователя
    URL: /registration
    """
    
    # Локаторы
    SOCIAL_TITLE_MR = (By.CSS_SELECTOR, "input#field-id_gender-1")
    SOCIAL_TITLE_MRS = (By.CSS_SELECTOR, "input#field-id_gender-2")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input#field-firstname")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input#field-lastname")
    EMAIL_INPUT = (By.CSS_SELECTOR, "input#field-email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input#field-password")
    BIRTHDAY_INPUT = (By.CSS_SELECTOR, "input#field-birthday")
    
    # Чекбоксы
    NEWSLETTER_CHECKBOX = (By.CSS_SELECTOR, "input[name='newsletter']")
    GDPR_CHECKBOX = (By.CSS_SELECTOR, "input[name='psgdpr']")
    CUSTOMER_PRIVACY_CHECKBOX = (By.CSS_SELECTOR, "input[name='customer_privacy']")
    PARTNER_OFFERS_CHECKBOX = (By.CSS_SELECTOR, "input[name='optin']")
    
    # Кнопки
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[data-link-action='save-customer']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login']")
    
    # Сообщения
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    FORM_TITLE = (By.CSS_SELECTOR, "h1.h1")
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = "/registration"
    
    def open(self):
        """Открыть страницу регистрации"""
        self.driver.get(f"{self.base_url}{self.url}")
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """Дождаться загрузки формы регистрации"""
        self.wait.until(
            EC.presence_of_element_located(self.FORM_TITLE)
        )
    
    def select_social_title(self, title="mr"):
        """
        Выбрать обращение
        :param title: "mr" или "mrs"
        """
        if title.lower() == "mr":
            self.find_clickable(self.SOCIAL_TITLE_MR).click()
        elif title.lower() == "mrs":
            self.find_clickable(self.SOCIAL_TITLE_MRS).click()
    
    def fill_registration_form(self, first_name, last_name, email, password, birthday=""):
        """
        Заполнить форму регистрации
        :param first_name: Имя
        :param last_name: Фамилия
        :param email: Email
        :param password: Пароль
        :param birthday: Дата рождения (опционально)
        """
        # Вводим имя
        first_name_input = self.find(self.FIRST_NAME_INPUT)
        first_name_input.clear()
        first_name_input.send_keys(first_name)
        
        # Вводим фамилию
        last_name_input = self.find(self.LAST_NAME_INPUT)
        last_name_input.clear()
        last_name_input.send_keys(last_name)
        
        # Вводим email
        email_input = self.find(self.EMAIL_INPUT)
        email_input.clear()
        email_input.send_keys(email)
        
        # Вводим пароль
        password_input = self.find(self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        
        # Если указана дата рождения
        if birthday:
            birthday_input = self.find(self.BIRTHDAY_INPUT)
            birthday_input.clear()
            birthday_input.send_keys(birthday)
    
    def accept_gdpr(self):
        """Принять GDPR согласие"""
        self.find_clickable(self.GDPR_CHECKBOX).click()
    
    def accept_customer_privacy(self):
        """Принять политику конфиденциальности"""
        self.find_clickable(self.CUSTOMER_PRIVACY_CHECKBOX).click()
    
    def subscribe_newsletter(self):
        """Подписаться на новости"""
        self.find_clickable(self.NEWSLETTER_CHECKBOX).click()
    
    def submit_registration(self):
        """
        Отправить форму регистрации
        :return: True если успешно, False если ошибка
        """
        submit_btn = self.find_clickable(self.SUBMIT_BUTTON)
        submit_btn.click()
        
        # Проверяем результат
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE)
            )
            return True
        except TimeoutException:
            return False
    
    def register_user(self, first_name="John", last_name="Doe", email=None, password="Password123!"):
        """
        Зарегистрировать нового пользователя с заполнением всех обязательных полей
        :param first_name: Имя
        :param last_name: Фамилия
        :param email: Email (если None, генерируется случайный)
        :param password: Пароль
        :return: True если успешно
        """
        # Генерируем email, если не указан
        if email is None:
            email = f"test_{self._generate_random_string(8)}@example.com"
        
        # Выбираем обращение
        self.select_social_title("mr")
        
        # Заполняем форму
        self.fill_registration_form(first_name, last_name, email, password)
        
        # Принимаем согласия
        self.accept_gdpr()
        self.accept_customer_privacy()
        
        # Отправляем форму
        return self.submit_registration()
    
    @staticmethod
    def _generate_random_string(length=8):
        """Сгенерировать случайную строку"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def get_error_messages(self):
        """Получить сообщения об ошибках"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.find(self.ERROR_MESSAGE).text
        return None
    
    def is_form_displayed(self):
        """Проверить, отображается ли форма регистрации"""
        return self.is_element_present(self.FIRST_NAME_INPUT)