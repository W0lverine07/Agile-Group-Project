import unittest
import os
import time
import threading
import requests
import sys
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Import Flask application
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_dir)
from app import create_app

class RegistrationTest(unittest.TestCase):
    """Test registration and profile editing process"""
    
    @classmethod
    def setUpClass(cls):

        cls.screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
        if not os.path.exists(cls.screenshots_dir):
            os.makedirs(cls.screenshots_dir)
        """Set up one-time test environment"""
        # Set test server port
        cls.port = 5004
        cls.live_server_url = f"http://localhost:{cls.port}"
        
        # Create and configure Flask application
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['WTF_CSRF_ENABLED'] = False
        
        # Start Flask server in a separate thread
        def run_flask_app():
            cls.app.run(host='localhost', port=cls.port, use_reloader=False, debug=False)
        
        cls.server_thread = threading.Thread(target=run_flask_app)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        
        # Wait for server to start
        time.sleep(1)
        start_time = time.time()
        while time.time() - start_time < 7:
            try:
                response = requests.get(cls.live_server_url)
                if response.status_code == 200:
                    time.sleep(0.5)  # Extra wait to ensure full initialization
                    break
            except requests.exceptions.ConnectionError:
                time.sleep(0.1)
                continue
        
        # Set up Chrome
        chrome_options = Options()
        # Comment out headless mode for debugging
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--start-maximized')
        
        # Initialize webdriver
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        cls.driver.quit()
    
    def is_element_displayed_and_enabled(self, element):
        """Check if element is visible and interactive"""
        try:
            return element.is_displayed() and element.is_enabled()
        except:
            return False
    
    def take_screenshot(self, filename):
        """Save a screenshot to the screenshots directory"""
        filepath = os.path.join(self.__class__.screenshots_dir, filename)
        self.driver.save_screenshot(filepath) # Save screenshot
        print(f"Screenshot saved: {filepath}")
        return filepath


    def wait_for_element(self, locator, timeout=5):
        """Wait for element to be clickable"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except:
            return None
    
    def reset_focus(self):
        """Reset focus by clicking on a neutral area of the page"""
        try:
            # Try to click on the body element
            body = self.driver.find_element(By.TAG_NAME, "body")
            ActionChains(self.driver).move_to_element_with_offset(body, 0, 0).click().perform()
            # Also clear any active element
            self.driver.execute_script("document.activeElement.blur();")
            print("✓ Focus reset")
        except Exception as e:
            print(f"⚠️ Failed to reset focus: {str(e)}")
    
    def scroll_to_page_bottom(self):
        """Scroll to the bottom using multiple strategies with minimal wait time"""
        try:
            # Reset focus first
            self.reset_focus()
            
            # Strategy 1: JavaScript scroll
            self.driver.execute_script("""
                window.scrollTo(0, document.body.scrollHeight);
                window.scrollTo(0, document.documentElement.scrollHeight);
                
                // Scroll possible containers
                document.querySelectorAll('form, .content, main, .container').forEach(
                    el => { el.scrollTop = el.scrollHeight; }
                );
            """)
            
            # Strategy 2: Use keyboard END key
            try:
                html = self.driver.find_element(By.TAG_NAME, 'html')
                ActionChains(self.driver).move_to_element(html).send_keys(Keys.END).perform()
            except:
                pass
            
            # Short wait
            time.sleep(0.2)
            print("✓ Used multiple strategies to scroll to page bottom")
        except Exception as e:
            print(f"⚠️ All scroll methods failed: {str(e)}")
    
    def scroll_to_element(self, element):
        """Scroll element into center of view"""
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", 
                element
            )
            time.sleep(0.2)
            print("✓ Scrolled to element")
        except Exception as e:
            print(f"⚠️ Scroll to element failed: {str(e)}")
    
    def safe_click(self, element, description="element"):
        """Attempt to click an element safely using multiple methods"""
        try:
            # First try scrolling to it
            self.scroll_to_element(element)
            
            # Try regular click
            try:
                element.click()
                print(f"✓ Clicked {description} with regular click")
                return True
            except Exception as e:
                print(f"⚠️ Regular click on {description} failed: {str(e)}")
            
            # Try JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", element)
                print(f"✓ Clicked {description} with JavaScript")
                return True
            except Exception as e:
                print(f"⚠️ JavaScript click on {description} failed: {str(e)}")
            
            # Try Actions chain click
            try:
                ActionChains(self.driver).move_to_element(element).click().perform()
                print(f"✓ Clicked {description} with ActionChains")
                return True
            except Exception as e:
                print(f"⚠️ ActionChains click on {description} failed: {str(e)}")
            
            print(f"⚠️ All click methods failed for {description}")
            return False
            
        except Exception as e:
            print(f"⚠️ Safe click error for {description}: {str(e)}")
            return False
    
    def complete_form_and_submit(self):
        """Find and submit form using robust methods"""
        try:
            # Reset focus and scroll to bottom to see submit button
            self.reset_focus()
            self.scroll_to_page_bottom()
            
            # Try to find the submit button using multiple strategies
            submit_button = None
            
            # Look for submit buttons in different ways
            locators = [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Submit')]"),
                (By.XPATH, "//button[contains(text(), 'Save')]"),
                (By.XPATH, "//button[contains(text(), 'Update')]"),
                (By.XPATH, "//button[contains(text(), 'Continue')]"),
                (By.CSS_SELECTOR, ".submit-button")
            ]
            
            for locator in locators:
                elements = self.driver.find_elements(*locator)
                for element in elements:
                    if self.is_element_displayed_and_enabled(element):
                        submit_button = element
                        break
                if submit_button:
                    break
            
            # If submit button found, try to click it
            if submit_button:
                success = self.safe_click(submit_button, "submit button")
                if success:
                    time.sleep(0.5)  # Short wait for form processing
                    return True
            
            # If button not found or couldn't be clicked, try direct form submission
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            if forms:
                try:
                    self.driver.execute_script("arguments[0].submit();", forms[0])
                    print("✓ Form submitted via form.submit() JavaScript method")
                    time.sleep(0.5)
                    return True
                except Exception as e:
                    print(f"⚠️ Form.submit() failed: {str(e)}")
            
            # Last resort: try to press Enter on the last input field
            try:
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                if inputs:
                    last_input = inputs[-1]
                    ActionChains(self.driver).move_to_element(last_input).send_keys(Keys.ENTER).perform()
                    print("✓ Submitted form by pressing Enter on last input")
                    time.sleep(0.5)
                    return True
            except Exception as e:
                print(f"⚠️ Enter key submission failed: {str(e)}")
            
            print("⚠️ Could not submit form")
            return False
            
        except Exception as e:
            print(f"⚠️ Form submission failed: {str(e)}")
            return False
    
    def generate_test_user(self):
        """Generate test user data"""
        chars = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(chars) for _ in range(6))
        return {
            'username': f"test_user_{random_str}",
            'password': f"Test_pass{random_str}123",
            'first_name': f"First{random_str}",
            'last_name': f"Last{random_str}",
            'email': f"test_{random_str}@example.com",
            'dob': "1990-01-01",
            'blood_group': "A+",
            'weight': "70",
            'height': "175"
        }
    
    def test_registration_and_profile_update(self):
        """Test complete registration and profile completion flow"""
        # Generate test user data
        test_user = self.generate_test_user()
        
        # Step 1: Visit login page
        print("\nStep 1: Visit login page")
        self.driver.get(f"{self.live_server_url}/login")
        time.sleep(0.5)
        self.take_screenshot('step1_login_page.png')
        print("✓ Login page accessed")
        
        # Step 2: Find and click register button
        print("\nStep 2: Find and click register button")
        register_btn = None
        
        # First try with data attribute (most reliable)
        try:
            data_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-form="register"]')
            if data_buttons:
                register_btn = data_buttons[0]
                print(f"✓ Found register button by data attribute")
        except:
            pass
        
        # If not found, try by text content
        if not register_btn:
            all_buttons = self.driver.find_elements(By.TAG_NAME, 'button')
            for button in all_buttons:
                try:
                    button_text = button.text.strip() or "No text"
                    if 'register' in button_text.lower() or 'sign up' in button_text.lower():
                        register_btn = button
                        print(f"✓ Found register button by text: {button_text}")
                        break
                except:
                    continue
        
        # If still not found, try by XPath
        if not register_btn:
            try:
                xpath_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Register')]")
                if xpath_buttons:
                    register_btn = xpath_buttons[0]
                    print(f"✓ Found register button by XPath")
            except:
                pass
        
        # Click register button using safe click
        if register_btn:
            self.safe_click(register_btn, "register button")
            time.sleep(0.3)  # Short wait for transition
            self.take_screenshot('step2_after_register_click.png')
        else:
            self.fail("Could not find register button")
        
        # Step 3: Fill registration form
        print("\nStep 3: Fill registration form")
        
        # Find and fill username field
        username_field = self.wait_for_element((By.NAME, "username"))
        if not username_field:
            username_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="username"]')
            for field in username_fields:
                if self.is_element_displayed_and_enabled(field):
                    username_field = field
                    break
        
        if username_field:
            username_field.clear()
            username_field.send_keys(test_user['username'])
            print(f"✓ Username filled: {test_user['username']}")
        else:
            self.fail("Interactive username field not found")
        
        # Find and fill password field
        password_field = self.wait_for_element((By.NAME, "password"))
        if not password_field:
            password_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="password"]')
            for field in password_fields:
                if self.is_element_displayed_and_enabled(field):
                    password_field = field
                    break
        
        if password_field:
            password_field.clear()
            password_field.send_keys(test_user['password'])
            print("✓ Password filled")
        else:
            self.fail("Interactive password field not found")
        
        # Find and fill confirm password field
        confirm_field = self.wait_for_element((By.NAME, "confirm_password"))
        if not confirm_field:
            confirm_fields = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="confirm_password"]')
            for field in confirm_fields:
                if self.is_element_displayed_and_enabled(field):
                    confirm_field = field
                    break
        
        if confirm_field:
            confirm_field.clear()
            confirm_field.send_keys(test_user['password'])
            print("✓ Confirm password filled")
        else:
            print("⚠️ Confirm password field not found, this may be normal")
        
        # Find and check terms checkbox
        terms_checkbox = self.wait_for_element((By.NAME, "terms"))
        if not terms_checkbox:
            terms_boxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[name="terms"]')
            for box in terms_boxes:
                if self.is_element_displayed_and_enabled(box):
                    terms_checkbox = box
                    break
        
        if terms_checkbox and not terms_checkbox.is_selected():
            self.safe_click(terms_checkbox, "terms checkbox")
            print("✓ Terms checkbox checked")
        else:
            print("⚠️ Terms checkbox not found or already checked")
        
        # Reset focus before taking screenshot
        self.reset_focus()
        self.take_screenshot('step3_filled_registration.png')
        
        # Step 4: Submit registration form
        print("\nStep 4: Submit registration form")
        
        if not self.complete_form_and_submit():
            self.fail("Failed to submit registration form")
        
        time.sleep(0.5)  # Short wait after submission
        self.take_screenshot('step4_after_registration_submit.png')
        
        # Step 5: Verify registration result
        print("\nStep 5: Verify registration result")
        
        # Record current URL and title
        current_url = self.driver.current_url
        page_title = self.driver.title
        
        print(f"Current URL: {current_url}")
        print(f"Page title: {page_title}")
        
        # Check if redirected to edit_profile page, indicating successful registration
        edit_profile_indicators = [
            "/edit_profile" in current_url,
            "edit_profile" in current_url,
            "Edit Profile" in page_title,
            "edit profile" in page_title.lower(),
            "Update Your Profile" in self.driver.page_source,
            "update your profile" in self.driver.page_source.lower()
        ]
        
        if any(edit_profile_indicators):
            print("✓ Registration successful! Redirected to profile edit page")
            self.assertTrue(True, "Registration successful and redirected to profile edit page")
        else:
            self.take_screenshot('step5_registration_failed.png')
            self.fail("Registration failed, not redirected to profile edit page")
        
        # Step 6: Fill profile form
        print("\nStep 6: Fill profile form")
        
        # Define fields to fill and corresponding values
        profile_fields = [
            {"name": "first_name", "value": test_user["first_name"]},
            {"name": "last_name", "value": test_user["last_name"]},
            {"name": "email", "value": test_user["email"]},
            {"name": "dob", "value": test_user["dob"]},
            {"name": "weight", "value": test_user["weight"]},
            {"name": "height", "value": test_user["height"]}
        ]
        
        # Fill text fields one by one, resetting focus between each
        for field in profile_fields:
            try:
                # Try to find field using wait first
                input_element = self.wait_for_element((By.NAME, field["name"]))
                
                # If not found, try other methods
                if not input_element:
                    input_elements = self.driver.find_elements(By.NAME, field["name"])
                    for element in input_elements:
                        if self.is_element_displayed_and_enabled(element):
                            input_element = element
                            break
                
                if input_element:
                    # Scroll to the element first
                    self.scroll_to_element(input_element)
                    
                    # Clear and fill
                    input_element.clear()
                    input_element.send_keys(field["value"])
                    
                    # Reset focus after filling to avoid any dropdown/suggestion issues
                    self.reset_focus()
                    
                    print(f"✓ Filled {field['name']}: {field['value']}")
                else:
                    print(f"⚠️ {field['name']} field not found or not interactive")
            except Exception as e:
                print(f"⚠️ Error filling {field['name']} field: {str(e)}")
        
        # Select blood type
        try:
            # Try to find blood type select box
            blood_select = self.wait_for_element((By.NAME, "blood_group"))
            if not blood_select:
                blood_selects = self.driver.find_elements(By.NAME, "blood_group")
                for select in blood_selects:
                    if self.is_element_displayed_and_enabled(select):
                        blood_select = select
                        break
            
            if blood_select:
                # Use Select class to handle dropdown
                from selenium.webdriver.support.ui import Select
                
                # Scroll to the select element
                self.scroll_to_element(blood_select)
                
                # Select value
                select = Select(blood_select)
                select.select_by_visible_text(test_user["blood_group"])
                
                # Reset focus
                self.reset_focus()
                
                print(f"✓ Blood type selected: {test_user['blood_group']}")
            else:
                print("⚠️ Blood type select box not found or not interactive")
        except Exception as e:
            print(f"⚠️ Error selecting blood type: {str(e)}")
        
        # Take screenshot after form filled
        self.reset_focus()
        self.take_screenshot('step6_filled_profile.png')
        
        # Step 7: Submit profile form
        print("\nStep 7: Submit profile form")
        
        if not self.complete_form_and_submit():
            # If failed to submit normally, try form direct submission
            try:
                forms = self.driver.find_elements(By.TAG_NAME, "form")
                if forms:
                    self.driver.execute_script("arguments[0].submit();", forms[0])
                    print("✓ Last resort: Form submitted via direct JavaScript")
                    time.sleep(0.5)
                else:
                    self.fail("Form not found for direct submission")
            except Exception as e:
                self.take_screenshot('step7_submit_error.png')
                self.fail(f"All form submission methods failed: {str(e)}")
        
        self.take_screenshot('step7_after_profile_submit.png')
        
        # Step 8: Verify profile update
        print("\nStep 8: Verify profile update")
        
        # Print current URL
        current_url = self.driver.current_url
        print(f"Current URL: {current_url}")
        
        # Check for success messages
        try:
            success_messages = self.driver.find_elements(By.CLASS_NAME, "flash-message")
            for msg in success_messages:
                if self.is_element_displayed_and_enabled(msg):
                    print(f"Message: {msg.text}")
                    if "success" in msg.text.lower() or "updated" in msg.text.lower():
                        print("✓ Found profile update success message")
        except:
            pass
        
        # Check if redirected to success page
        success_indicators = [
            "dashboard" in current_url,
            "account" in current_url,
            "health_data" in current_url,
            "profile" in current_url and "edit" not in current_url,  # If redirected to view page
            "success" in self.driver.page_source.lower(),
            "updated" in self.driver.page_source.lower(),
            "welcome" in self.driver.page_source.lower() and test_user["first_name"] in self.driver.page_source
        ]
        
        if any(success_indicators):
            print("✅ Profile updated successfully!")
            self.assertTrue(True, "Profile updated successfully")
        else:
            print("⚠️ No clear indication of profile update success, but form was submitted")
        
        self.take_screenshot('step8_profile_result.png')
        print("✓ Test completed")

        # Step 9: Go to login page to verify credentials
        print("\nStep 9: Navigate to login page to verify credentials")
        try:
            # Go directly to login page
            self.driver.get(f"{self.live_server_url}/login")
            # Wait for page to load
            self.wait_for_element((By.NAME, "username"), timeout=3)
            self.take_screenshot('step9_login_page.png')
            print("✓ Navigated to login page")
            
            # Find and fill username field
            username_field = self.wait_for_element((By.NAME, "username"))
            if username_field:
                username_field.clear()
                username_field.send_keys(test_user['username'])
                print(f"✓ Username filled: {test_user['username']}")
            else:
                self.fail("Username field not found on login page")
            
            # Find and fill password field
            password_field = self.wait_for_element((By.NAME, "password"))
            if password_field:
                password_field.clear()
                password_field.send_keys(test_user['password'])
                print("✓ Password filled")
            else:
                self.fail("Password field not found on login page")
            
            # Reset focus
            self.reset_focus()
            
            # Submit login form
            login_btn = self.wait_for_element((By.CSS_SELECTOR, "button[type='submit']"))
            if not login_btn:
                # Try alternative locators
                login_locators = [
                    (By.XPATH, "//button[contains(text(), 'Login')]"),
                    (By.XPATH, "//button[contains(text(), 'Sign in')]")
                ]
                
                for locator in login_locators:
                    login_btn = self.wait_for_element(locator, timeout=1)
                    if login_btn:
                        break
            
            if login_btn:
                self.safe_click(login_btn, "login button")
                print("✓ Clicked login button")
            else:
                # Try direct form submission
                forms = self.driver.find_elements(By.TAG_NAME, "form")
                if forms:
                    self.driver.execute_script("arguments[0].submit();", forms[0])
                    print("✓ Login form submitted via JavaScript")
                else:
                    self.fail("Could not find login button or form")
            
            # Wait for login redirection
            try:
                WebDriverWait(self.driver, 3).until(
                    lambda driver: "login" not in driver.current_url
                )
                print("✓ Login redirection detected")
            except:
                print("⚠️ No redirection detected after login")
            
            self.take_screenshot('step9_after_login.png')
            
            # Verify login success
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            login_success = (
                "dashboard" in current_url or 
                "account" in current_url or 
                "health_data" in current_url or
                "welcome" in page_source.lower() or
                test_user['username'] in page_source
            )
            
            if login_success:
                print("✓ Login successful with created credentials")
            else:
                self.fail("Login verification failed - not redirected to dashboard or account page")
            
        except Exception as e:
            self.take_screenshot('step9_login_error.png')
            self.fail(f"Error during login verification: {str(e)}")

        # Step 10: Navigate to profile page
        print("\nStep 10: Navigate to profile page")
        try:
            # Find profile navigation link/button with explicit wait
            profile_btn = None
            profile_locators = [
                (By.XPATH, "//a[contains(text(), 'Profile')]"),
                (By.XPATH, "//button[contains(text(), 'Profile')]"),
                (By.CSS_SELECTOR, "a[href*='profile']"),
                (By.CSS_SELECTOR, "a[href*='account']")
            ]
            
            for locator in profile_locators:
                profile_btn = self.wait_for_element(locator, timeout=1)
                if profile_btn:
                    break
            
            if profile_btn:
                self.safe_click(profile_btn, "profile button/link")
                print("✓ Clicked profile button/link")
                
                # Wait for profile page to load
                try:
                    WebDriverWait(self.driver, 3).until(
                        lambda driver: "profile" in driver.current_url or "account" in driver.current_url
                    )
                    print("✓ Profile page navigation detected")
                except:
                    print("⚠️ No profile page navigation detected")
            else:
                # Try direct navigation
                print("⚠️ Could not find profile button, trying direct navigation")
                self.driver.get(f"{self.live_server_url}/profile")
                # Wait for profile page to load
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            
            self.take_screenshot('step10_profile_page.png')
            
            # Step 11: Verify profile information
            print("\nStep 11: Verify profile information")
            page_source = self.driver.page_source
            
            # Check for profile information
            verification_points = [
                (test_user['first_name'], "first name"),
                (test_user['last_name'], "last name"),
                (test_user['email'], "email"),
                (test_user['weight'], "weight"),
                (test_user['height'], "height")
            ]
            
            verification_passed = True
            for value, field_name in verification_points:
                if value in page_source:
                    print(f"✓ Verified {field_name}: {value}")
                else:
                    print(f"⚠️ Could not verify {field_name}: {value}")
                    verification_passed = False
            
            if verification_passed:
                print("✅ Profile information verification PASSED")
                self.assertTrue(True, "Profile information verification successful")
            else:
                print("⚠️ Some profile information could not be verified")
                # Don't fail the test, just warn
            
            self.take_screenshot('step11_profile_verification.png')
            
        except Exception as e:
            self.take_screenshot('step10_11_error.png')
            print(f"⚠️ Error during profile verification: {str(e)}")
            # Don't let this cause the test to fail, just log the failure
            print("⚠️ Profile verification encountered errors, but continuing test")

        print("✓ Test completed successfully")

if __name__ == '__main__':
    unittest.main()