from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdminLoginPage(BasePage):
    """
    PageObject для страницы логина в админку PrestaShop
    URL: /administration
    """
    
    # Локаторы
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "passwd")
    LOGIN_BUTTON = (By.NAME, "submit_login")
    LOGIN_FORM = (By.ID, "login_form")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.alert-danger")
    EMPLOYEE_AVATAR = (By.CSS_SELECTOR, "img.employee_avatar")
    REMEMBER_ME_CHECKBOX = (By.ID, "rememberMe")
    LANGUAGE_SELECTOR = (By.ID, "language")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Forgot your password?")
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.url = "/administration"
    
    def open(self):
        """Открыть страницу логина админки"""
        self.driver.get(f"{self.base_url}{self.url}")
        self.wait_for_page_load()
    
    def wait_for_page_load(self):
        """Дождаться загрузки страницы логина"""
        self.wait.until(
            EC.presence_of_element_located(self.LOGIN_FORM)
        )
    
    def login(self, email, password):
        """
        Выполнить логин в админку
        :param email: Email администратора
        :param password: Пароль
        :return: AdminDashboardPage
        """
        from pages.admin_dashboard_page import AdminDashboardPage
        
        # Очищаем поля и вводим данные
        email_input = self.find(self.EMAIL_INPUT)
        email_input.clear()
        email_input.send_keys(email)
        
        password_input = self.find(self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        
        # Нажимаем кнопку логина
        self.find_clickable(self.LOGIN_BUTTON).click()
        
        # Возвращаем страницу дашборда
        dashboard = AdminDashboardPage(self.driver, self.base_url)
        dashboard.wait_for_page_load()
        return dashboard
    
    def is_login_error_displayed(self):
        """Проверить, отображается ли ошибка логина"""
        return self.is_element_present(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """Получить текст ошибки"""
        if self.is_login_error_displayed():
            return self.find(self.ERROR_MESSAGE).text
        return None