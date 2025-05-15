import unittest
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from app import app

class LiveServerThread(threading.Thread):
    def run(self):
        app.run(port=5001)

class TestSeleniumIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = LiveServerThread()
        cls.server.daemon = True
        cls.server.start()
        time.sleep(2)  # wait for the server to spin up

        options = Options()
        options.add_argument('--headless')
        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = 'http://localhost:5001/'

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_homepage_loads(self):
        self.driver.get(self.base_url)
        self.assertIn("Wellness Tracker", self.driver.page_source)

    def test_upload_button_exists(self):
        self.driver.get(self.base_url + 'health_data.html')
        upload_btn = self.driver.find_element(By.XPATH, '//a[contains(@href, "upload.html")]')
        self.assertIsNotNone(upload_btn)

    def test_data_form_submission(self):
        self.driver.get(self.base_url + 'data.html')
        self.driver.find_element(By.NAME, "unique_number").send_keys("12345")
        self.driver.find_element(By.NAME, "dob").send_keys("2000-01-01")
        self.driver.find_element(By.TAG_NAME, "form").submit()
        self.assertIn("Health Data", self.driver.page_source)

    def test_visualize_button_redirects(self):
        self.driver.get(self.base_url + 'health_data.html')
        self.driver.find_element(By.XPATH, '//a[contains(@href, "visualize.html")]').click()
        self.assertIn("Visualize", self.driver.title)

    def test_share_button_redirects(self):
        self.driver.get(self.base_url + 'health_data.html')
        self.driver.find_element(By.XPATH, '//a[contains(@href, "share.html")]').click()
        self.assertIn("Share", self.driver.title)

if __name__ == '__main__':
    unittest.main()
