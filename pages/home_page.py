"""
Home Page Object - Contains all methods for interacting with the home page.
"""

from .base_page import BasePage
from config.locators import Locators
from core.reporter import Reporter

class HomePage(BasePage):
    """
    Methods for home page specific validations.
    """
    
    def __init__(self, page, reporter: Reporter):
        """
        Initialize Home Page.
        """
        super().__init__(page, reporter)
        self.locators = Locators.Home
        self.validation_results = {
            'banner_found': False,
            'banner_text_found': False
        }

    def validate_banners(self, take_screenshot: bool = True):
        """
        Validates the presence and content of banner elements on the home page.
        """
        self.logger.info("\n" + "="*30 + " Banner Validation " + "="*30)
        
        banner_container = self.find_element(self.locators.HERO_SECTION, "Banner container")
        
        if banner_container:
            self.validation_results['banner_found'] = True
            self.logger.info("✓ Banner container found.")

            # Note: Banner image and text locators may need to be updated based on actual site structure
            self.logger.info("Banner validation completed.")
        else:
            self.logger.error("✗ Banner validation failed as container was not found.")
        
        self.reporter.add_data('banner_details', self.validation_results)