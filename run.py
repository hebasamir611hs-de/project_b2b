"""
Main execution script for the Playwright validation project (OOP Version).
Run this file to execute the validation using Page Object Model.
"""

import sys
import time
from datetime import datetime
from typing import Optional

from config.settings import Settings
from core.browser_manager import BrowserManager
from core.logger import Logger
from core.reporter import Reporter
from pages.base_page import BasePage
from pages.header_page import HeaderPage
from pages.footer_page import FooterPage
from pages.home_page import HomePage


class WebsiteValidator:
    """
    Main Website Validator class orchestrating the validation process.
    """
    
    def __init__(self):
        """Initialize Website Validator."""
        self.logger = Logger.get_logger()
        self.settings = Settings
        self.browser_manager: Optional[BrowserManager] = None
        self.reporter = Reporter()
        self.exit_code = Settings.EXIT_CODE_SUCCESS
    
    def run(self) -> int:
        """
        Main execution method.
        """
        self._print_header()
        
        try:
            self.browser_manager = BrowserManager()
            with self.browser_manager as browser:
                page = browser.get_page()
                if not page:
                    self.logger.error("Failed to create page")
                    return Settings.EXIT_CODE_UNKNOWN_ERROR
                
                self._initialize_reporter()
                
                if self._navigate(page):
                    page.wait_for_timeout(2000)
                    self._run_validation_flow(page)
                
        except KeyboardInterrupt:
            self.logger.warning("\nScript interrupted by user.")
            self.exit_code = 130
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())
            self.exit_code = Settings.EXIT_CODE_UNKNOWN_ERROR
        finally:
            self._generate_reports()
            self._print_summary()

        return self.exit_code

    def _run_validation_flow(self, page):
        """
        Orchestrates the full validation sequence.
        """
        header_page = HeaderPage(page, self.reporter)
        home_page = HomePage(page, self.reporter)
        footer_page = FooterPage(page, self.reporter)

        if self.settings.VALIDATE_HEADER:
            header_page.validate_all()

        # Banner validation is temporarily disabled as the locators are incorrect.
        # self._validate_home_page(home_page)
        
        self._perform_language_switch_test(header_page)
        
        # Perform search test and take screenshot of results
        self._perform_search_test(header_page)

        if self.settings.VALIDATE_FOOTER:
            footer_page.validate_all()

        self._take_screenshot(page)

    def _print_header(self):
        self.logger.info("=" * 80)
        self.logger.info(f"{self.settings.PROJECT_NAME} v{self.settings.PROJECT_VERSION}")
        self.logger.info(self.settings.display_config())
    
    def _initialize_reporter(self):
        self.reporter.add_data('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.reporter.add_data('url', self.settings.TARGET_URL)
        self.reporter.add_data('browser', self.settings.BROWSER_TYPE)
        self.reporter.add_data('viewport', self.settings.get_viewport())
    
    def _navigate(self, page) -> bool:
        self.logger.info("\n" + "="*30 + " Navigation " + "="*30)
        base_page = BasePage(page, self.reporter)
        success, status_code = base_page.navigate(self.settings.TARGET_URL)
        
        self.reporter.add_data('navigation_success', success)
        self.reporter.add_data('status_code', status_code)
        
        if not success:
            self.logger.error(f"✗ Navigation to {self.settings.TARGET_URL} failed!")
            self.exit_code = Settings.EXIT_CODE_NAVIGATION_FAILED
        else:
            self.logger.info(f"✓ Successfully navigated to {self.settings.TARGET_URL}")
        
        return success
    
    def _validate_home_page(self, home_page: HomePage):
        home_page.validate_banners()

    def _perform_language_switch_test(self, header_page: HeaderPage):
        self.logger.info("\n" + "="*30 + " Language Switch Test " + "="*30)
        if header_page.switch_language_and_verify(target_lang='ar'):
            time.sleep(2)
            header_page.switch_language_and_verify(target_lang='en')
            
    def _perform_search_test(self, header_page: HeaderPage):
        """
        Perform search for 'iPhone 13' and take screenshot of results.
        """
        self.logger.info("\n" + "="*30 + " Search Test " + "="*30)
        search_term = "iPhone 13"
        
        # Perform the dynamic search
        search_successful = header_page.perform_dynamic_search(search_term)
        
        if search_successful:
            self.logger.info(f"✓ Search for '{search_term}' completed successfully")
            # Take screenshot of search results
            base_page = BasePage(header_page.page, self.reporter)
            screenshot_path = base_page.take_page_screenshot("search_results")
            if screenshot_path:
                self.logger.info(f"✓ Screenshot of search results saved to: {screenshot_path}")
        else:
            self.logger.error(f"✗ Search for '{search_term}' failed")
            # Even if search fails, take a screenshot for debugging
            base_page = BasePage(header_page.page, self.reporter)
            screenshot_path = base_page.take_page_screenshot("search_failed")
            if screenshot_path:
                self.logger.info(f"Screenshot of failed search saved to: {screenshot_path}")

    def _take_screenshot(self, page):
        base_page = BasePage(page, self.reporter)
        base_page.take_page_screenshot("final_page_state")

    def _generate_reports(self):
        if not self.reporter:
            return
        self.reporter.add_data('exit_code', self.exit_code)
        if self.settings.GENERATE_JSON_REPORT:
            self.reporter.generate_json_report()
        if self.settings.GENERATE_HTML_REPORT:
            self.reporter.generate_html_report()
    
    def _print_summary(self):
        self.logger.info("\n" + "="*30 + " Validation Summary " + "="*30)
        self.logger.info(f"  Exit Code: {self.exit_code}")
        if self.settings.REPORTS_DIR.exists():
            self.logger.info(f"  Reports Folder: {self.settings.REPORTS_DIR.absolute()}")
        self.logger.info("="*80)

def main() -> int:
    validator = WebsiteValidator()
    return validator.run()

if __name__ == "__main__":
    sys.exit(main())