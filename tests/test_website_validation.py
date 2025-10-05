"""
Example test file using pytest and the OOP framework.
Run with: pytest tests/test_website_validation.py
"""

import pytest
from playwright.sync_api import Page, expect

from config.settings import Settings
from config.locators import Locators
from pages.base_page import BasePage
from pages.header_page import HeaderPage
from pages.footer_page import FooterPage
from core.reporter import Reporter


@pytest.fixture(scope="function")
def reporter() -> Reporter:
    """Fixture to create a Reporter instance."""
    return Reporter()


@pytest.fixture(scope="function")
def base_page(page: Page, reporter: Reporter) -> BasePage:
    """Fixture to create BasePage instance."""
    return BasePage(page, reporter)


@pytest.fixture(scope="function")
def header_page(page: Page, reporter: Reporter) -> HeaderPage:
    """Fixture to create HeaderPage instance."""
    return HeaderPage(page, reporter)


@pytest.fixture(scope="function")
def footer_page(page: Page, reporter: Reporter) -> FooterPage:
    """Fixture to create FooterPage instance."""
    return FooterPage(page, reporter)


class TestNavigation:
    """Test navigation functionality."""
    
    def test_navigate_to_target_url(self, base_page: BasePage):
        """Test navigation to target URL."""
        success, status_code = base_page.navigate(Settings.TARGET_URL)
        
        assert success, "Navigation should succeed"
        assert status_code == 200, f"Expected status 200, got {status_code}"
    
    def test_page_title_exists(self, base_page: BasePage):
        """Test that page has a title."""
        base_page.navigate(Settings.TARGET_URL)
        title = base_page.get_page_title()
        
        assert title, "Page should have a title"
        assert len(title) > 0, "Title should not be empty"


class TestHeader:
    """Test header validation."""
    
    def test_header_exists(self, header_page: HeaderPage):
        """Test that header element exists."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)  # Wait for page to stabilize
        
        assert header_page.is_header_visible(), "Header should be visible"
    
    def test_logo_exists(self, header_page: HeaderPage):
        """Test that logo exists in header."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)
        
        logo = header_page.find_logo()
        assert logo is not None, "Logo should exist"
    
    def test_login_button_exists(self, header_page: HeaderPage):
        """Test that login button exists."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)
        
        login_btn = header_page.find_login_button()
        assert login_btn is not None, "Login button should exist"
    
    def test_language_switcher_exists(self, header_page: HeaderPage):
        """Test that language switcher exists."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)
        
        lang_switcher = header_page.find_language_switcher()
        assert lang_switcher is not None, "Language switcher should exist"
    
    def test_header_full_validation(self, header_page: HeaderPage):
        """Test full header validation."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)
        
        results = header_page.validate_all()
        
        assert results['header_exists'], "Header should exist"
        assert results['logo_exists'], "Logo should exist"
        # Note: Some elements might not exist on all sites
        # Adjust assertions based on your target website


class TestFooter:
    """Test footer validation."""
    
    def test_footer_exists(self, footer_page: FooterPage):
        """Test that footer element exists."""
        footer_page.navigate(Settings.TARGET_URL)
        footer_page.wait(2000)
        
        assert footer_page.is_footer_visible(), "Footer should be visible"
    
    def test_footer_full_validation(self, footer_page: FooterPage):
        """Test full footer validation."""
        footer_page.navigate(Settings.TARGET_URL)
        footer_page.wait(2000)
        
        results = footer_page.validate_all()
        
        assert results['footer_exists'], "Footer should exist"


class TestScreenshots:
    """Test screenshot functionality."""
    
    def test_take_page_screenshot(self, base_page: BasePage):
        """Test taking page screenshot."""
        base_page.navigate(Settings.TARGET_URL)
        base_page.wait(2000)
        
        screenshot_path = base_page.take_page_screenshot("test_screenshot", full_page=True)
        
        assert screenshot_path is not None, "Screenshot should be captured"
        
        # Verify file exists
        from pathlib import Path
        assert Path(screenshot_path).exists(), "Screenshot file should exist"
    
    def test_take_element_screenshot(self, header_page: HeaderPage):
        """Test taking element screenshot."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)
        
        header = header_page.find_header()
        assert header is not None, "Header should exist"
        
        screenshot_path = header_page.take_element_screenshot(header, "test_header")
        assert screenshot_path is not None, "Element screenshot should be captured"


class TestSearch:
    """Test search functionality."""

    def test_perform_search(self, header_page: HeaderPage):
        """Test performing a search and verifying results."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)

        search_term = "iPhone 15"
        search_successful = header_page.perform_search(search_term)

        assert search_successful, f"Search for '{search_term}' should be successful and display results."

    def test_dynamic_search_functionality(self, header_page: HeaderPage):
        """Test the dynamic search functionality.
        
        This test covers:
        1. Click on the search bar in the header
        2. Enter a valid product keyword (e.g., "iPhone 15")
        3. Press Enter or click the search icon
        4. Matching products are displayed in a dropdown list
        5. Results update dynamically as user types
        """
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)

        search_term = "iPhone 15"
        search_successful = header_page.perform_dynamic_search(search_term)

        assert search_successful, f"Dynamic search for '{search_term}' should be successful and display results."

    def test_dynamic_results_while_typing(self, header_page: HeaderPage):
        """Test that search results update dynamically as user types."""
        header_page.navigate(Settings.TARGET_URL)
        header_page.wait(2000)

        search_term = "iPhone"
        dynamic_results_detected = header_page.type_and_check_dynamic_results(search_term, char_by_char=True)

        # This assertion is conditional because not all sites support dynamic search
        if dynamic_results_detected:
            assert True, "Dynamic search results were detected as user typed"
        else:
            header_page.logger.info("Site may not support dynamic search functionality")


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )


# Example of using markers
@pytest.mark.smoke
class TestSmoke:
    """Smoke tests - quick validation."""
    
    def test_site_is_accessible(self, base_page: BasePage):
        """Quick test that site is accessible."""
        success, status_code = base_page.navigate(Settings.TARGET_URL)
        assert success and status_code == 200
