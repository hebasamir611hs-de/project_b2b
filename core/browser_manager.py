"""
Browser Manager - Handles browser lifecycle and context management.
"""

from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright

from config.settings import Settings
from .logger import Logger


class BrowserManager:
    """
    Manages browser lifecycle, context, and page creation.
    Implements context manager protocol for clean resource management.
    """
    
    def __init__(self):
        """Initialize Browser Manager."""
        self.logger = Logger.get_logger()
        self.settings = Settings
        
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def __enter__(self):
        """Context manager entry - start browser."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        self.cleanup()
        return False
    
    def start(self) -> Page:
        """
        Start browser and create page.
        
        Returns:
            Playwright Page object
        """
        try:
            self.logger.info("Starting browser...")
            
            # Start Playwright
            self.playwright = sync_playwright().start()
            
            # Launch browser
            browser_type = getattr(self.playwright, self.settings.BROWSER_TYPE)
            self.browser = browser_type.launch(
                headless=self.settings.HEADLESS,
                args=['--start-maximized'] if not self.settings.HEADLESS else []
            )
            
            self.logger.info(f"✓ Browser launched: {self.settings.BROWSER_TYPE} "
                           f"(Headless: {self.settings.HEADLESS})")
            
            # Create context
            context_options = {
                'viewport': self.settings.get_viewport(),
                'user_agent': self.settings.USER_AGENT,
            }
            
            # Enable tracing if configured
            self.context = self.browser.new_context(**context_options)
            
            if self.settings.ENABLE_TRACING:
                self.context.tracing.start(
                    screenshots=self.settings.TRACE_SCREENSHOTS,
                    snapshots=self.settings.TRACE_SNAPSHOTS
                )
                self.logger.info("✓ Tracing enabled")
            
            # Create page
            self.page = self.context.new_page()
            
            # Set default timeouts
            self.page.set_default_timeout(self.settings.ELEMENT_TIMEOUT)
            self.page.set_default_navigation_timeout(self.settings.NAVIGATION_TIMEOUT)
            
            self.logger.info(f"✓ Page created with viewport: "
                           f"{self.settings.VIEWPORT_WIDTH}x{self.settings.VIEWPORT_HEIGHT}")
            
            return self.page
            
        except Exception as e:
            self.logger.error(f"Failed to start browser: {str(e)}")
            self.cleanup()
            raise
    
    def get_page(self) -> Optional[Page]:
        """
        Get current page instance.
        
        Returns:
            Playwright Page object or None
        """
        return self.page
    
    def get_context(self) -> Optional[BrowserContext]:
        """
        Get current browser context.
        
        Returns:
            BrowserContext object or None
        """
        return self.context
    
    def get_browser(self) -> Optional[Browser]:
        """
        Get current browser instance.
        
        Returns:
            Browser object or None
        """
        return self.browser
    
    def save_trace(self, filename: str = "trace.zip") -> Optional[str]:
        """
        Save trace file if tracing is enabled.
        
        Args:
            filename: Trace filename
        
        Returns:
            Path to trace file or None
        """
        if self.context and self.settings.ENABLE_TRACING:
            try:
                trace_path = self.settings.TRACES_DIR / filename
                self.context.tracing.stop(path=str(trace_path))
                self.logger.info(f"✓ Trace saved: {trace_path}")
                return str(trace_path)
            except Exception as e:
                self.logger.error(f"Failed to save trace: {str(e)}")
                return None
        return None
    
    def take_screenshot(self, filename: str, full_page: bool = True) -> Optional[str]:
        """
        Take screenshot of current page.
        
        Args:
            filename: Screenshot filename (without extension)
            full_page: Take full page screenshot if True
        
        Returns:
            Path to screenshot or None
        """
        if self.page:
            try:
                screenshot_path = self.settings.SCREENSHOT_DIR / f"{filename}.{self.settings.SCREENSHOT_FORMAT}"
                self.page.screenshot(path=str(screenshot_path), full_page=full_page)
                self.logger.info(f"✓ Screenshot saved: {screenshot_path.name}")
                return str(screenshot_path)
            except Exception as e:
                self.logger.error(f"Failed to take screenshot: {str(e)}")
                return None
        return None
    
    def get_browser_info(self) -> Dict[str, Any]:
        """
        Get browser information.
        
        Returns:
            Dictionary with browser info
        """
        info = {
            'browser_type': self.settings.BROWSER_TYPE,
            'headless': self.settings.HEADLESS,
            'viewport': self.settings.get_viewport(),
            'user_agent': self.settings.USER_AGENT,
        }
        
        if self.browser:
            info['browser_version'] = self.browser.version
        
        if self.page:
            info['current_url'] = self.page.url
            info['page_title'] = self.page.title()
        
        return info
    
    def cleanup(self) -> None:
        """Clean up browser resources."""
        self.logger.info("Cleaning up browser resources...")
        
        # Save trace if enabled
        if self.settings.ENABLE_TRACING and self.context:
            try:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.save_trace(f"trace_{timestamp}.zip")
            except:
                pass
        
        # Close page
        if self.page:
            try:
                self.page.close()
                self.logger.debug("✓ Page closed")
            except Exception as e:
                self.logger.debug(f"Error closing page: {str(e)}")
        
        # Close context
        if self.context:
            try:
                self.context.close()
                self.logger.debug("✓ Context closed")
            except Exception as e:
                self.logger.debug(f"Error closing context: {str(e)}")
        
        # Close browser
        if self.browser:
            try:
                self.browser.close()
                self.logger.debug("✓ Browser closed")
            except Exception as e:
                self.logger.debug(f"Error closing browser: {str(e)}")
        
        # Stop Playwright
        if self.playwright:
            try:
                self.playwright.stop()
                self.logger.debug("✓ Playwright stopped")
            except Exception as e:
                self.logger.debug(f"Error stopping Playwright: {str(e)}")
        
        self.logger.info("✓ Cleanup complete")
