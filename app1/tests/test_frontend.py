from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase

class FrontendTests(LiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        self.browser = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.browser.quit()

    def test_home_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Home', self.browser.title)
        navbar = self.browser.find_element(By.CLASS_NAME, 'navbar')
        self.assertIsNotNone(navbar)
        about_us = self.browser.find_element(By.ID, 'about_us')
        self.assertIsNotNone(about_us)
