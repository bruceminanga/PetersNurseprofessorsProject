from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase
from django.urls import reverse

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
        
        # Test the page title
        self.assertIn('Home', self.browser.title)
        
        # Test the presence of Navbar
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME, 'navbar'))
        
        # Test the presence of sections
        self.assertIsNotNone(self.browser.find_element(By.ID, 'about_us'))
        self.assertIsNotNone(self.browser.find_element(By.CSS_SELECTOR, '.bsb-cta-1'))
        self.assertIsNotNone(self.browser.find_element(By.ID, 'pricing'))
        self.assertIsNotNone(self.browser.find_element(By.ID, 'questions'))
        
        # Test the presence of at least one FAQ item
        faq_items = self.browser.find_elements(By.CLASS_NAME, 'accordion-item')
        self.assertGreaterEqual(len(faq_items), 1)

    def test_order_form_page(self):
        # Navigate to the order form page
        orderform_url = self.live_server_url + reverse('app1:order')  # Replace 'order' with the actual name of your view
        self.browser.get(orderform_url)

        # Test the presence of the Personal Details section
        self.assertIsNotNone(self.browser.find_element(By.CSS_SELECTOR, 'h5[style="color:blue;"]:nth-of-type(1)'))
        
        # Test the presence of CSRF token
        csrf_token = self.browser.find_element(By.NAME, 'csrfmiddlewaretoken')
        self.assertIsNotNone(csrf_token)

        # Test form fields
        form_fields = [
            'id_academic_level',
            'id_type_of_service',
            'id_type_of_paper',
            'id_subject_area',
            'id_title',
            'id_paper_instructions',
            'id_additional_material',
            'id_paper_format',
            'id_number_of_pages_increment',
            'id_number_of_pages',
            'id_currency',
            'id_sources',
            'id_powerpoint_slides',
            'id_deadline',
            'id_writer_category',
            'id_preferred_writers_id'
        ]
        for field_id in form_fields:
            self.assertIsNotNone(self.browser.find_element(By.ID, field_id))
        
        # Test the presence of the Pricing Details section
        self.assertIsNotNone(self.browser.find_element(By.CSS_SELECTOR, 'h5[style="color:blue;"]:nth-of-type(2)'))
        
        # Test the presence of the submit button
        submit_button = self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.assertIsNotNone(submit_button)
        
        # Test the presence of the fixed card on the right
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME, 'fixed-card'))
        
        # Test the presence of the PayPal button container
        self.assertIsNotNone(self.browser.find_element(By.ID, 'paypal-button-container'))

        # Test the presence of the coupon form
        coupon_apply_form = self.browser.find_element(By.CSS_SELECTOR, 'form p input[type="text"]')
        self.assertIsNotNone(coupon_apply_form)
        apply_button = self.browser.find_element(By.CSS_SELECTOR, 'button[onclick="applyCoupon()"]')
        self.assertIsNotNone(apply_button)

        # Test JavaScript functionality (apply coupon button click)
        apply_button.click()

if __name__ == "__main__":
    FrontendTests()
