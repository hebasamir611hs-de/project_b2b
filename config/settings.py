"""
Settings Configuration - All project settings centralized here.
Follows Singleton pattern for consistent configuration across the project.
"""

import os
from pathlib import Path
from typing import Literal


class Settings:
    """
    Centralized configuration class using Singleton pattern.
    All settings are class-level attributes for easy access.
    """
    
    # ===== Project Information =====
    PROJECT_NAME: str = "Playwright Website Validator"
    PROJECT_VERSION: str = "2.0.0"
    
    # ===== Target Website =====
    TARGET_URL: str = os.getenv("TARGET_URL", "https://shopdev.ooredoo.com.kw/")
    
    # ===== Browser Configuration =====
    BROWSER_TYPE: Literal["chromium", "firefox", "webkit"] = "chromium"
    HEADLESS: bool = True
    VIEWPORT_WIDTH: int = 1920
    VIEWPORT_HEIGHT: int = 1080
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # ===== Timeouts (milliseconds) =====
    NAVIGATION_TIMEOUT: int = 60000  # 60 seconds
    ELEMENT_TIMEOUT: int = 10000     # 10 seconds
    SCREENSHOT_TIMEOUT: int = 5000   # 5 seconds
    ACTION_TIMEOUT: int = 5000       # 5 seconds for clicks, hovers, etc.
    
    # ===== Retry Configuration =====
    MAX_RETRIES: int = 3
    RETRY_DELAY: int = 2  # seconds
    
    # ===== Navigation Settings =====
    WAIT_UNTIL: Literal["load", "domcontentloaded", "networkidle", "commit"] = "domcontentloaded"
    
    # ===== Directory Paths =====
    BASE_DIR: Path = Path(__file__).parent.parent
    SCREENSHOT_DIR: Path = BASE_DIR / "screenshots"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    LOGS_DIR: Path = BASE_DIR / "logs"
    TRACES_DIR: Path = BASE_DIR / "traces"
    
    # ===== Screenshot Configuration =====
    SCREENSHOT_STRATEGY: Literal["fullpage", "viewport", "element", "random"] = "fullpage"
    SCREENSHOT_FORMAT: Literal["png", "jpeg"] = "png"
    SCREENSHOT_QUALITY: int = 90  # For JPEG only (0-100)
    
    # ===== Logging Configuration =====
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: str = "[%(asctime)s] [%(levelname)s] %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_TO_FILE: bool = True
    LOG_FILE_NAME: Path = LOGS_DIR / f"validation_{os.getpid()}.log"
    
    # ===== Report Configuration =====
    GENERATE_HTML_REPORT: bool = True
    GENERATE_JSON_REPORT: bool = True
    REPORT_RETENTION_DAYS: int = 30
    EMBED_SCREENSHOTS_IN_HTML: bool = True  # Embed as base64
    
    # ===== Validation Configuration =====
    VALIDATE_HEADER: bool = True
    VALIDATE_FOOTER: bool = True
    VALIDATE_HEADER_ELEMENTS: bool = True  # Deep header validation
    TAKE_ELEMENT_SCREENSHOTS: bool = True
    SCREENSHOT_ON_HOVER: bool = True
    
    # ===== Tracing Configuration =====
    ENABLE_TRACING: bool = False
    TRACE_SCREENSHOTS: bool = True
    TRACE_SNAPSHOTS: bool = True
    
    # ===== Exit Codes =====
    EXIT_CODE_SUCCESS: int = 0
    EXIT_CODE_NAVIGATION_FAILED: int = 1
    EXIT_CODE_ELEMENTS_MISSING: int = 2
    EXIT_CODE_SCREENSHOT_FAILED: int = 3
    EXIT_CODE_VALIDATION_FAILED: int = 4
    EXIT_CODE_UNKNOWN_ERROR: int = 99
    
    @classmethod
    def create_directories(cls) -> None:
        """Create all required directories if they don't exist."""
        for directory in [cls.SCREENSHOT_DIR, cls.REPORTS_DIR, cls.LOGS_DIR, cls.TRACES_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_viewport(cls) -> dict:
        """Get viewport configuration as dictionary."""
        return {
            'width': cls.VIEWPORT_WIDTH,
            'height': cls.VIEWPORT_HEIGHT
        }
    
    @classmethod
    def update_from_env(cls) -> None:
        """Update settings from environment variables."""
        # Browser settings
        if os.getenv("BROWSER_TYPE"):
            cls.BROWSER_TYPE = os.getenv("BROWSER_TYPE")
        
        if os.getenv("HEADLESS"):
            cls.HEADLESS = os.getenv("HEADLESS").lower() == "true"
        
        # Timeouts
        if os.getenv("NAVIGATION_TIMEOUT"):
            cls.NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT"))
        
        if os.getenv("ELEMENT_TIMEOUT"):
            cls.ELEMENT_TIMEOUT = int(os.getenv("ELEMENT_TIMEOUT"))
        
        # Screenshot strategy
        if os.getenv("SCREENSHOT_STRATEGY"):
            cls.SCREENSHOT_STRATEGY = os.getenv("SCREENSHOT_STRATEGY")
        
        # Logging
        if os.getenv("LOG_LEVEL"):
            cls.LOG_LEVEL = os.getenv("LOG_LEVEL")
    
    @classmethod
    def display_config(cls) -> str:
        """Return configuration summary as string."""
        return f"""
{'='*80}
{cls.PROJECT_NAME} v{cls.PROJECT_VERSION} - Configuration
{'='*80}
Target URL: {cls.TARGET_URL}
Browser: {cls.BROWSER_TYPE} (Headless: {cls.HEADLESS})
Viewport: {cls.VIEWPORT_WIDTH}x{cls.VIEWPORT_HEIGHT}
Navigation Timeout: {cls.NAVIGATION_TIMEOUT}ms
Element Timeout: {cls.ELEMENT_TIMEOUT}ms
Screenshot Strategy: {cls.SCREENSHOT_STRATEGY}
Reports: HTML={cls.GENERATE_HTML_REPORT}, JSON={cls.GENERATE_JSON_REPORT}
Tracing: {cls.ENABLE_TRACING}
{'='*80}
"""


# Initialize directories on import
Settings.create_directories()
Settings.update_from_env()
