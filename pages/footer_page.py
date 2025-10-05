"""
Footer Page Object - Handles all footer-related validations and interactions.
"""

from typing import Dict, List, Optional
from playwright.sync_api import Page, Locator

from .base_page import BasePage
from config.locators import Locators
from config.settings import Settings
from core.reporter import Reporter


class FooterPage(BasePage):
    """
    Footer Page Object for validating and interacting with footer elements.
    """
    
    def __init__(self, page: Page, reporter: Reporter):
        """
        Initialize Footer Page.
        """
        super().__init__(page, reporter)
        self.locators = Locators.Footer
        self.validation_results = {
            'footer_exists': False,
            'social_links_count': 0,
            'footer_links_count': 0,
            'newsletter_exists': False,
            'screenshots': []
        }

    def find_footer(self) -> Optional[Locator]:
        return self.find_element(self.locators.CONTAINER, "Footer container")

    def is_footer_visible(self) -> bool:
        is_visible = self.is_element_visible(self.locators.CONTAINER, "footer")
        self.validation_results['footer_exists'] = is_visible
        return is_visible

    def validate_social_links(self):
        social_links = self.get_all_elements(self.locators.SOCIAL_LINKS, base_element=self.find_footer())
        count = len(social_links)
        self.validation_results['social_links_count'] = count
        self.reporter.log_info(f"Found {count} social media links.")

    def validate_footer_links(self):
        footer_links = self.get_all_elements(self.locators.FOOTER_LINKS, base_element=self.find_footer())
        count = len(footer_links)
        self.validation_results['footer_links_count'] = count
        self.reporter.log_info(f"Found {count} footer links.")

    def validate_newsletter(self):
        newsletter = self.find_element(self.locators.NEWSLETTER_INPUT, "Newsletter input", base_element=self.find_footer())
        self.validation_results['newsletter_exists'] = newsletter is not None
        if newsletter:
            self.reporter.log_info("✓ Newsletter input form found.")
        else:
            self.reporter.log_warning("✗ Newsletter input form not found.")

    def validate_all(self) -> Dict:
        self.reporter.log_section("Footer Validation")
        if not self.is_footer_visible():
            self.reporter.log_error("Footer not found - skipping other checks")
            return self.validation_results
        
        self.validate_social_links()
        self.validate_footer_links()
        self.validate_newsletter()
        
        if Settings.TAKE_ELEMENT_SCREENSHOTS:
            footer = self.find_footer()
            if footer:
                path = self.take_element_screenshot(footer, "footer_full")
                if path: self.validation_results['screenshots'].append("footer_full")

        self.reporter.add_data('footer_details', self.validation_results)
        return self.validation_results