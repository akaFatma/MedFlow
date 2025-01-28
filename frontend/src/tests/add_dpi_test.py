from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import unittest
from datetime import datetime

class TestDPICreation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = "http://localhost:4200" 
        
    def tearDown(self):
        self.driver.quit()
        
    def test_dpi_creation_complete_flow(self):
        driver = self.driver
        # navigate to the page
        driver.get(f"{self.base_url}/add-dpi")
        
        # Wait for the form to be visible
        wait = WebDriverWait(driver, 10)
        form = wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
        
        # Test Step 1: Personal Information
        # Fill in the first step form
        self.fill_step_one()
        
        # Click Next button
        next_button = driver.find_element(By.CSS_SELECTOR, "button.button.suivant")
        next_button.click()
        
        # Test Step 2: Additional Information
        # Wait for second step to be visible and fill it
        self.fill_step_two()
        
        # Click Next button again
        next_button = driver.find_element(By.CSS_SELECTOR, "button.button.suivant")
        next_button.click()
        
        # Test Step 3: Verification and Submission
        # Verify summary data
        self.verify_summary_data()
        
        # Submit the form
        validate_button = driver.find_element(By.CSS_SELECTOR, "button.button.suivant")
        validate_button.click()
        
        # Verify success notification
        try:
            success_notification = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "app-success-notif"))
            )
            self.assertTrue(success_notification.is_displayed())
        except TimeoutException:
            self.fail("Success notification did not appear")

    def fill_step_one(self):
        """Fill in the first step of the form"""
        # Fill in personal information
        self.driver.find_element(By.ID, "prenom").send_keys("Jean")
        self.driver.find_element(By.ID, "nom").send_keys("Dupont")
        self.driver.find_element(By.ID, "date_naissance").send_keys("1990-01-01")
        self.driver.find_element(By.ID, "telephone").send_keys("0612345678")

    def fill_step_two(self):
        """Fill in the second step of the form"""
        wait = WebDriverWait(self.driver, 10)
        
        # Wait for and fill in additional information
        nss_input = wait.until(EC.presence_of_element_located((By.ID, "nss")))
        nss_input.send_keys("1900123456789")
        
        self.driver.find_element(By.ID, "mutuelle").send_keys("MGEN")
        self.driver.find_element(By.ID, "adr").send_keys("123 Rue de Paris")
        self.driver.find_element(By.ID, "nom_personne").send_keys("Martin")
        self.driver.find_element(By.ID, "prenom_personne").send_keys("Marie")
        self.driver.find_element(By.ID, "telephone_personne").send_keys("0687654321")

    def verify_summary_data(self):
        """Verify the summary data in step 3"""
        wait = WebDriverWait(self.driver, 10)
        
        # Wait for summary container to be visible
        summary_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary-container"))
        )
        
        # Verify the entered data is displayed correctly
        summary_text = summary_container.text
        test_data = {
            "Nom": "Dupont",
            "Prénom": "Jean",
            "Date de naissance": "1990-01-01",
            "Numéro de téléphone": "0612345678",
            "Numéro de sécurité sociale": "1900123456789",
            "Adresse": "123 Rue de Paris"
        }
        
        for label, value in test_data.items():
            self.assertIn(value, summary_text, f"Cannot find {value} in summary")

    def test_form_validation(self):
        """Test form validation"""
        driver = self.driver
        driver.get(f"{self.base_url}/add-dpi")
        
        next_button = driver.find_element(By.CSS_SELECTOR, "button.button.suivant")
        next_button.click()
        
        # Verify we're still on step 1 (form shouldn't proceed)
        current_step = driver.find_element(By.CLASS_NAME, "circle")
        self.assertEqual(current_step.text, "1")

    def test_navigation_buttons(self):
        """Test navigation buttons (Next, Back)"""
        driver = self.driver
        driver.get(f"{self.base_url}/add-dpi")
        
        # Fill step 1 and go to step 2
        self.fill_step_one()
        next_button = driver.find_element(By.CSS_SELECTOR, "button.button.suivant")
        next_button.click()
        
        # Test back button
        back_button = driver.find_element(By.CSS_SELECTOR, "button.button.retour")
        back_button.click()
        
        # Verify we're back on step 1
        current_step = driver.find_element(By.CLASS_NAME, "circle")
        self.assertEqual(current_step.text, "1")

if __name__ == "__main__":
    unittest.main()