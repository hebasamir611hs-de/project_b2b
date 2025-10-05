"""
Base Page Object - Parent class for all page objects.
Contains common methods used across all pages.
"""

import time
from typing import Optional, List, Tuple
from pathlib import Path
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeout

from config.settings import Settings
from core.logger import Logger
from core.reporter import Reporter


class BasePage:
    """
    Base Page Object class with common functionality.
    All page objects should inherit from this class.
    """
    
    def __init__(self, page: Page, reporter: Reporter):
        """
        Initialize base page.
        
        Args:
            page: Playwright Page object
            reporter: Reporter instance for logging results.
        """
        self.page = page
        self.logger = Logger.get_logger()
        self.settings = Settings
        self.reporter = reporter
    
    # ===== Navigation Methods =====
    
    def navigate(self, url: str, retries: int = None) -> Tuple[bool, Optional[int]]:
        """
        Navigate to URL with retry logic.
        """
        if retries is None:
            retries = self.settings.MAX_RETRIES
        
        for attempt in range(1, retries + 1):
            try:
                self.logger.info(f"Navigation attempt {attempt}/{retries} to {url}")
                response = self.page.goto(
                    url,
                    wait_until=self.settings.WAIT_UNTIL,
                    timeout=self.settings.NAVIGATION_TIMEOUT
                )
                if response:
                    status_code = response.status
                    self.logger.info(f"✓ Page loaded with HTTP status: {status_code}")
                    return 200 <= status_code < 300, status_code
                else:
                    self.logger.warning("No response received from navigation")
            except PlaywrightTimeout:
                self.logger.error(f"Navigation timeout on attempt {attempt}")
                if attempt == retries:
                    return False, None
            except Exception as e:
                self.logger.error(f"Navigation error: {type(e).__name__}: {str(e)}")
                if attempt == retries:
                    return False, None
            
            if attempt < retries:
                time.sleep(self.settings.RETRY_DELAY)
        
        return False, None

    # ===== Element Finding Methods =====
    
    def find_element(self, selectors: List[str], element_name: str, base_element: Optional[Locator] = None, timeout: int = None) -> Optional[Locator]:
        """
        Find element using multiple selectors.
        """
        if timeout is None:
            timeout = self.settings.ELEMENT_TIMEOUT
        
        search_context = base_element if base_element else self.page

        for selector in selectors:
            try:
                locator = search_context.locator(selector).first
                locator.wait_for(state="visible", timeout=1000) # Use a short timeout to quickly check
                self.logger.info(f"Found '{element_name}' with selector: '{selector}'")
                return locator
            except:
                continue
        
        self.logger.error(f"Could not find '{element_name}' after trying all selectors.")
        return None

    def is_element_visible(self, selectors: List[str], element_name: str = "element", timeout: int = None) -> bool:
        """
        Check if element is visible using multiple selectors.
        """
        self.logger.info(f"Checking for {element_name}...")
        element = self.find_element(selectors, element_name, timeout=timeout)
        return element is not None
    
    def get_all_elements(self, selectors: List[str], base_element: Optional[Locator] = None) -> List[Locator]:
        """
        Get all matching elements for given selectors.
        """
        all_elements = []
        search_context = base_element if base_element else self.page
        for selector in selectors:
            try:
                elements = search_context.locator(selector).all()
                all_elements.extend(elements)
            except:
                continue
        return all_elements

    # ===== Interaction Methods =====
    
    def click_element(self, locator: Locator, element_name: str = "element") -> bool:
        """
        Click on element with error handling.
        """
        try:
            locator.click(timeout=self.settings.ACTION_TIMEOUT)
            self.logger.info(f"✓ Clicked on {element_name}")
            return True
        except Exception as e:
            self.logger.error(f"✗ Failed to click {element_name}: {str(e)}")
            return False
    
    def hover_element(self, locator: Locator, element_name: str = "element") -> bool:
        """
        Hover over element with error handling.
        """
        try:
            locator.hover(timeout=self.settings.ACTION_TIMEOUT)
            self.logger.info(f"✓ Hovered over {element_name}")
            return True
        except Exception as e:
            self.logger.error(f"✗ Failed to hover {element_name}: {str(e)}")
            return False

    def is_element_clickable(self, locator: Locator) -> bool:
        """
        Check if element is clickable (enabled).
        """
        try:
            return locator.is_enabled(timeout=self.settings.ELEMENT_TIMEOUT)
        except:
            return False

    def fill_text(self, locator: Locator, text: str, element_name: str = "element") -> bool:
        """
        Fill text into an element with error handling.
        """
        try:
            locator.fill(text, timeout=self.settings.ACTION_TIMEOUT)
            self.logger.info(f"✓ Filled '{text}' into {element_name}")
            return True
        except Exception as e:
            self.logger.error(f"✗ Failed to fill {element_name}: {str(e)}")
            return False

    # ===== Screenshot Methods =====
    
    def take_element_screenshot(self, locator: Locator, filename: str) -> Optional[str]:
        """
        Take screenshot of specific element.
        """
        try:
            locator.scroll_into_view_if_needed()
            time.sleep(0.2)
            screenshot_path = self.settings.SCREENSHOT_DIR / f"{filename}.{self.settings.SCREENSHOT_FORMAT}"
            locator.screenshot(path=str(screenshot_path))
            self.logger.info(f"✓ Screenshot saved: {filename}.{self.settings.SCREENSHOT_FORMAT}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.warning(f"Failed to capture element screenshot '{filename}': {str(e)}")
            return None
    
    def take_page_screenshot(self, filename: str, full_page: bool = True) -> Optional[str]:
        """
        Take screenshot of entire page or viewport.
        """
        try:
            screenshot_path = self.settings.SCREENSHOT_DIR / f"{filename}.{self.settings.SCREENSHOT_FORMAT}"
            self.page.screenshot(path=str(screenshot_path), full_page=full_page)
            self.logger.info(f"✓ Page screenshot saved: {filename}.{self.settings.SCREENSHOT_FORMAT}")
            return str(screenshot_path)
        except Exception as e:
            self.logger.error(f"Failed to capture page screenshot '{filename}': {str(e)}")
            return None

    # ===== Utility Methods =====
    
    def get_element_text(self, locator: Locator) -> Optional[str]:
        """
        Get text content of element.
        """
        try:
            return locator.text_content()
        except:
            return None
    
    def get_element_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """
        Get attribute value of element.
        """
        try:
            return locator.get_attribute(attribute)
        except:
            return None

    def get_page_title(self) -> Optional[str]:
        """
        Get the title of the current page.
        """
        try:
            return self.page.title()
        except Exception as e:
            self.logger.error(f"Failed to get page title: {str(e)}")
            return None

    def wait(self, milliseconds: int) -> None:
        """
        Wait for a specified number of milliseconds.
        """
        time.sleep(milliseconds / 1000)
