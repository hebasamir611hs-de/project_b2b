"""
Header Page Object - Handles all header-related validations and interactions.
"""

import time
from typing import Dict, List, Optional
from playwright.sync_api import Page, Locator

from .base_page import BasePage
from config.locators import Locators
from config.settings import Settings
from core.reporter import Reporter


class HeaderPage(BasePage):
    """
    Header Page Object for validating and interacting with header elements.
    """
    
    def __init__(self, page: Page, reporter: Reporter):
        """
        Initialize Header Page.
        """
        super().__init__(page, reporter)
        self.locators = Locators.Header
        self.validation_results = {
            'header_exists': False,
            'logo_exists': False,
            'logo_clickable': False,
            'login_button_exists': False,
            'login_button_clickable': False,
            'language_switcher_exists': False,
            'language_switcher_clickable': False,
            'dropdowns': [],
            'nav_items_count': 0,
            'screenshots': []
        }
    
    def find_header(self) -> Optional[Locator]:
        return self.find_element(self.locators.CONTAINER, "Header container")

    def find_logo(self) -> Optional[Locator]:
        return self.find_element(self.locators.LOGO, "Logo")

    def find_login_button(self) -> Optional[Locator]:
        return self.find_element(self.locators.LOGIN_BUTTON, "Login button")

    def find_language_switcher(self) -> Optional[Locator]:
        return self.find_element(self.locators.LANGUAGE_SWITCHER, "Language switcher")

    def find_search_box(self) -> Optional[Locator]:
        return self.find_element(self.locators.SEARCH_BOX, "Search box")

    def find_search_icon(self) -> Optional[Locator]:
        return self.find_element(self.locators.SEARCH_ICON, "Search icon")

    def is_header_visible(self) -> bool:
        is_visible = self.is_element_visible(self.locators.CONTAINER, "header")
        self.validation_results['header_exists'] = is_visible
        return is_visible

    def validate_logo(self):
        logo = self.find_element(self.locators.LOGO, "Logo")
        if logo:
            self.validation_results['logo_exists'] = True
            try:
                parent = logo.locator('xpath=..').first
                if parent.evaluate('el => el.tagName') == 'A':
                    self.validation_results['logo_clickable'] = True
            except:
                pass
            if Settings.TAKE_ELEMENT_SCREENSHOTS:
                path = self.take_element_screenshot(logo, "logo")
                if path: self.validation_results['screenshots'].append("logo")

    def validate_login_button(self):
        login_btn = self.find_element(self.locators.LOGIN_BUTTON, "Login button")
        if login_btn:
            self.validation_results['login_button_exists'] = True
            self.validation_results['login_button_clickable'] = self.is_element_clickable(login_btn)
            if Settings.TAKE_ELEMENT_SCREENSHOTS:
                path = self.take_element_screenshot(login_btn, "login_button")
                if path: self.validation_results['screenshots'].append("login_button")

    def validate_language_switcher(self):
        lang_switcher = self.find_element(self.locators.LANGUAGE_SWITCHER, "Language switcher")
        if lang_switcher:
            self.validation_results['language_switcher_exists'] = True
            self.validation_results['language_switcher_clickable'] = self.is_element_clickable(lang_switcher)
            if Settings.TAKE_ELEMENT_SCREENSHOTS:
                path = self.take_element_screenshot(lang_switcher, "language_switcher")
                if path: self.validation_results['screenshots'].append("language_switcher")

    def perform_search(self, search_term: str) -> bool:
        self.logger.info(f"--- Performing search for '{search_term}' ---")
        search_icon = self.find_element(self.locators.SEARCH_ICON, "Search icon")
        if not search_icon:
            self.logger.error("Search icon not found.")
            return False

        # Use JavaScript to click the icon and make the search box visible
        self.page.evaluate("document.querySelector('.search_icon .sicon').click();")
        time.sleep(1) # Wait for the animation
        self.page.evaluate("document.querySelector('#search').style.display = 'block';")

        search_box = self.find_element(self.locators.SEARCH_BOX, "Search box")
        if not search_box:
            self.logger.error("Search box not found after making it visible with JavaScript.")
            return False

        self.fill_text(search_box, search_term, "Search box")
        self.page.press("body", "Enter")  # Press Enter to submit

        # Wait for search results to appear
        try:
            self.page.wait_for_selector(self.locators.SEARCH_RESULTS_CONTAINER[0], timeout=10000)
            self.logger.info("✓ Search results dropdown appeared.")
            return True
        except Exception as e:
            self.logger.error(f"✗ Search results did not appear after searching for '{search_term}'. {e}")
            return False

    def perform_dynamic_search(self, search_term: str) -> bool:
        """
        Perform a dynamic search that updates results as the user types.
        
        Steps:
        1. Click on the search bar in the header
        2. Enter a valid product keyword (e.g., "iPhone 15")
        3. Results update dynamically as user types
        4. Press Enter or click the search icon
        5. Matching products are displayed in a dropdown list
        """
        self.logger.info(f"--- Performing dynamic search for '{search_term}' ---")
        
        # Step 1: Click on the search bar in the header
        search_box = self.find_search_box()
        if not search_box:
            # Try to make search box visible first
            search_icon = self.find_search_icon()
            if search_icon:
                self.click_element(search_icon, "Search icon")
                time.sleep(1)  # Wait for animation
                search_box = self.find_search_box()
        
        if not search_box:
            self.logger.error("Search box not found.")
            return False
            
        # Click on the search box to focus it
        self.click_element(search_box, "Search box")
        self.logger.info("✓ Clicked on the search bar in the header")
        
        # Step 2: Enter a valid product keyword
        self.fill_text(search_box, search_term, "Search box")
        self.logger.info(f"✓ Entered product keyword: '{search_term}'")
        
        # Step 3: Check if results update dynamically as user types
        try:
            # Wait a bit for dynamic results to appear
            self.page.wait_for_timeout(2000)
            
            # Check if search results container exists
            results_container = self.find_element(
                self.locators.SEARCH_RESULTS_CONTAINER, 
                "Search results container"
            )
            
            if results_container:
                is_visible = results_container.is_visible()
                if is_visible:
                    self.logger.info("✓ Search results dropdown appeared dynamically as user typed")
                else:
                    self.logger.warning("Search results container found but not visible")
            else:
                self.logger.warning("Search results container not found - might not support dynamic search")
        except Exception as e:
            self.logger.warning(f"Dynamic search results check failed: {e}")
        
        # Step 4: Press Enter
        search_box.press("Enter")
        self.logger.info("✓ Pressed Enter key")
        
        # Step 5: Verify matching products are displayed in a dropdown list
        try:
            # Try multiple approaches to find search results
            search_result_selectors = self.locators.SEARCH_RESULTS_CONTAINER + [
                '[class*="search" i][class*="result" i]',
                '[id*="search" i][id*="autocomplete" i]',
                '.search-results',
                '.autocomplete'
            ]
            
            found_results = False
            for selector in search_result_selectors:
                try:
                    self.page.wait_for_selector(selector, state="visible", timeout=5000)
                    self.logger.info(f"✓ Search results dropdown appeared with selector: {selector}")
                    found_results = True
                    break
                except:
                    continue
            
            if not found_results:
                # Check if we navigated to search results page instead
                current_url = self.page.url
                if "catalogsearch" in current_url or "search" in current_url:
                    self.logger.info("✓ Navigated to search results page")
                    return True
                else:
                    self.logger.error("✗ Search results dropdown did not appear and not navigated to search page")
                    return False
                    
            return True
        except Exception as e:
            self.logger.error(f"✗ Search results verification failed. {e}")
            return False

    def type_and_check_dynamic_results(self, search_term: str, char_by_char: bool = True) -> bool:
        """
        Type in the search box and check for dynamic results after each character or word.
        
        Args:
            search_term (str): The term to search for
            char_by_char (bool): If True, type one character at a time and check for results after each
                               If False, type the whole term at once
                               
        Returns:
            bool: True if dynamic results were detected, False otherwise
        """
        self.logger.info(f"--- Typing '{search_term}' and checking for dynamic results ---")
        
        # Find and click the search box
        search_box = self.find_search_box()
        if not search_box:
            search_icon = self.find_search_icon()
            if search_icon:
                self.click_element(search_icon, "Search icon")
                time.sleep(1)
                search_box = self.find_search_box()
        
        if not search_box:
            self.logger.error("Search box not found.")
            return False
            
        self.click_element(search_box, "Search box")
        
        # Clear the search box first
        search_box.fill("")
        
        # Type and check for dynamic results
        if char_by_char:
            # Type one character at a time
            for i, char in enumerate(search_term):
                search_box.type(char, delay=200)  # Add small delay to simulate real typing
                self.page.wait_for_timeout(500)   # Wait for dynamic results
                
                # Check for results after each character
                results_container = self.find_element(
                    self.locators.SEARCH_RESULTS_CONTAINER,
                    "Search results container"
                )
                
                if results_container and results_container.is_visible():
                    self.logger.info(f"✓ Dynamic results appeared after typing: '{search_term[:i+1]}'")
                    return True
        else:
            # Type the whole term at once
            search_box.fill(search_term)
            self.page.wait_for_timeout(2000)  # Wait for dynamic results
            
            results_container = self.find_element(
                self.locators.SEARCH_RESULTS_CONTAINER,
                "Search results container"
            )
            
            if results_container and results_container.is_visible():
                self.logger.info(f"✓ Dynamic results appeared after typing: '{search_term}'")
                return True
                
        self.logger.info("No dynamic results appeared during typing")
        return False

    def switch_language_and_verify(self, target_lang: str) -> bool:
        self.logger.info(f"--- Switching language to '{target_lang.upper()}' ---")
        lang_switcher = self.find_element(self.locators.LANGUAGE_SWITCHER, "Language switcher")
        if not lang_switcher:
            self.logger.error("Language switcher not found.")
            return False

        self.click_element(lang_switcher, "Language switcher")
        self.page.wait_for_load_state(Settings.WAIT_UNTIL, timeout=Settings.NAVIGATION_TIMEOUT)
        self.logger.info(f"Clicked language switcher. Verifying UI update...")

        # Verify by checking the lang attribute of the <html> tag
        try:
            self.page.wait_for_selector(f"html[lang*='{target_lang}']", timeout=5000)
            html_element = self.page.locator("html")
            actual_lang = html_element.get_attribute("lang")
            self.logger.info(f"Found <html lang='{actual_lang}'>")
            
            if target_lang in actual_lang.lower():
                self.logger.info(f"✓ UI updated to {target_lang.upper()} successfully.")
                self.take_page_screenshot(f"language_switch_{target_lang}")
                return True
            else:
                self.logger.error(f"✗ Verification failed. Expected lang='{target_lang}', but found '{actual_lang}'.")
                self.take_page_screenshot(f"language_switch_{target_lang}_failed")
                return False
        except Exception as e:
            self.logger.error(f"✗ Could not verify language change by checking <html lang>: {str(e)}")
            self.take_page_screenshot(f"language_switch_{target_lang}_failed")
            return False

    def validate_all(self) -> Dict:
        self.logger.info("\n" + "="*30 + " Header Validation " + "="*30)
        if not self.is_header_visible():
            self.logger.error("Header not found - skipping other checks")
            return self.validation_results
        
        self.validate_logo()
        self.validate_login_button()
        self.validate_language_switcher()
        
        if Settings.TAKE_ELEMENT_SCREENSHOTS:
            header = self.find_header()
            if header:
                path = self.take_element_screenshot(header, "header_full")
                if path: self.validation_results['screenshots'].append("header_full")
        
        self.reporter.add_data('header_details', self.validation_results)
        return self.validation_results