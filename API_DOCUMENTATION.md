# 📚 API Documentation

Complete API reference for Playwright Website Validator OOP framework.

---

## Table of Contents

1. [Configuration](#configuration)
2. [Page Objects](#page-objects)
3. [Core Utilities](#core-utilities)
4. [Usage Examples](#usage-examples)

---

## Configuration

### Settings Class

**Location:** `config/settings.py`

Centralized configuration using class-level attributes.

#### Key Attributes

```python
# Project Info
Settings.PROJECT_NAME: str
Settings.PROJECT_VERSION: str

# Target
Settings.TARGET_URL: str

# Browser
Settings.BROWSER_TYPE: Literal["chromium", "firefox", "webkit"]
Settings.HEADLESS: bool
Settings.VIEWPORT_WIDTH: int
Settings.VIEWPORT_HEIGHT: int

# Timeouts (milliseconds)
Settings.NAVIGATION_TIMEOUT: int
Settings.ELEMENT_TIMEOUT: int
Settings.ACTION_TIMEOUT: int

# Directories
Settings.SCREENSHOT_DIR: Path
Settings.REPORTS_DIR: Path
Settings.LOGS_DIR: Path
Settings.TRACES_DIR: Path

# Screenshot
Settings.SCREENSHOT_STRATEGY: Literal["fullpage", "viewport", "element", "random"]
Settings.SCREENSHOT_FORMAT: Literal["png", "jpeg"]

# Validation
Settings.VALIDATE_HEADER: bool
Settings.VALIDATE_FOOTER: bool
Settings.VALIDATE_HEADER_ELEMENTS: bool
```

#### Methods

```python
@classmethod
def create_directories() -> None:
    """Create all required directories."""

@classmethod
def get_viewport() -> dict:
    """Get viewport configuration as dictionary."""

@classmethod
def update_from_env() -> None:
    """Update settings from environment variables."""

@classmethod
def display_config() -> str:
    """Return configuration summary as string."""
```

#### Usage

```python
from config.settings import Settings

# Access settings
url = Settings.TARGET_URL
timeout = Settings.NAVIGATION_TIMEOUT

# Get viewport
viewport = Settings.get_viewport()  # {'width': 1920, 'height': 1080}

# Display config
print(Settings.display_config())
```

---

### Locators Class

**Location:** `config/locators.py`

Centralized element selectors organized by page sections.

#### Nested Classes

- `Locators.Header` - Header section locators
- `Locators.Footer` - Footer section locators
- `Locators.Interactive` - Common interactive elements
- `Locators.Sections` - Main page sections

#### Header Locators

```python
Locators.Header.CONTAINER: List[str]          # Header container
Locators.Header.LOGO: List[str]               # Logo selectors
Locators.Header.LOGIN_BUTTON: List[str]       # Login button
Locators.Header.LANGUAGE_SWITCHER: List[str]  # Language switcher
Locators.Header.DROPDOWNS: List[str]          # Dropdown menus
Locators.Header.NAV_ITEMS: List[str]          # Navigation items
Locators.Header.SEARCH_BOX: List[str]         # Search box
Locators.Header.CART_BUTTON: List[str]        # Shopping cart
```

#### Footer Locators

```python
Locators.Footer.CONTAINER: List[str]          # Footer container
Locators.Footer.SOCIAL_LINKS: List[str]       # Social media links
Locators.Footer.NEWSLETTER_INPUT: List[str]   # Newsletter input
Locators.Footer.FOOTER_LINKS: List[str]       # Footer links
```

#### Static Methods

```python
@staticmethod
def get_all_clickable_selectors() -> List[str]:
    """Get all clickable element selectors combined."""

@staticmethod
def get_header_clickable_elements() -> Dict[str, List[str]]:
    """Get all header clickable elements organized by type."""

@staticmethod
def get_footer_clickable_elements() -> Dict[str, List[str]]:
    """Get all footer clickable elements organized by type."""
```

#### Usage

```python
from config.locators import Locators

# Access specific locators
logo_selectors = Locators.Header.LOGO
login_selectors = Locators.Header.LOGIN_BUTTON

# Get all clickable elements
all_clickable = Locators.get_all_clickable_selectors()

# Get organized header elements
header_elements = Locators.get_header_clickable_elements()
# Returns: {'login_button': [...], 'language_switcher': [...], ...}
```

---

## Page Objects

### BasePage Class

**Location:** `pages/base_page.py`

Base class for all page objects with common functionality.

#### Constructor

```python
def __init__(self, page: Page):
    """
    Initialize base page.
    
    Args:
        page: Playwright Page object
    """
```

#### Navigation Methods

```python
def navigate(self, url: str, retries: int = None) -> Tuple[bool, Optional[int]]:
    """
    Navigate to URL with retry logic.
    
    Args:
        url: Target URL
        retries: Number of retry attempts (default from settings)
    
    Returns:
        Tuple of (success: bool, status_code: Optional[int])
    """
```

#### Element Finding Methods

```python
def find_element(self, selectors: List[str], timeout: int = None) -> Optional[Locator]:
    """
    Find element using multiple selectors.
    
    Args:
        selectors: List of CSS selectors to try
        timeout: Timeout in milliseconds (default from settings)
    
    Returns:
        Locator if found, None otherwise
    """

def is_element_visible(self, selectors: List[str], element_name: str = "element", 
                      timeout: int = None) -> bool:
    """
    Check if element is visible using multiple selectors.
    
    Args:
        selectors: List of CSS selectors
        element_name: Name for logging
        timeout: Timeout in milliseconds
    
    Returns:
        True if visible, False otherwise
    """

def get_all_elements(self, selectors: List[str], timeout: int = None) -> List[Locator]:
    """
    Get all matching elements for given selectors.
    
    Args:
        selectors: List of CSS selectors
        timeout: Timeout in milliseconds
    
    Returns:
        List of Locator objects
    """
```

#### Interaction Methods

```python
def click_element(self, locator: Locator, element_name: str = "element") -> bool:
    """Click on element with error handling."""

def hover_element(self, locator: Locator, element_name: str = "element") -> bool:
    """Hover over element with error handling."""

def is_element_clickable(self, locator: Locator) -> bool:
    """Check if element is clickable (enabled)."""
```

#### Screenshot Methods

```python
def take_element_screenshot(self, locator: Locator, filename: str, 
                           screenshot_dir: Path = None) -> Optional[str]:
    """Take screenshot of specific element."""

def take_page_screenshot(self, filename: str, full_page: bool = True,
                        screenshot_dir: Path = None) -> Optional[str]:
    """Take screenshot of entire page or viewport."""
```

#### Utility Methods

```python
def wait(self, milliseconds: int) -> None:
    """Wait for specified time."""

def scroll_to_top(self) -> None:
    """Scroll to top of page."""

def scroll_to_bottom(self) -> None:
    """Scroll to bottom of page."""

def get_page_title(self) -> str:
    """Get page title."""

def get_current_url(self) -> str:
    """Get current page URL."""

def get_element_text(self, locator: Locator) -> Optional[str]:
    """Get text content of element."""

def get_element_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
    """Get attribute value of element."""
```

#### Usage Example

```python
from pages.base_page import BasePage

# Initialize
base_page = BasePage(page)

# Navigate
success, status = base_page.navigate("https://example.com")

# Find element
logo = base_page.find_element(Locators.Header.LOGO)

# Check visibility
is_visible = base_page.is_element_visible(Locators.Header.LOGIN_BUTTON, "login button")

# Take screenshot
base_page.take_page_screenshot("my_screenshot", full_page=True)
```

---

### HeaderPage Class

**Location:** `pages/header_page.py`

Page Object for header validation and interactions.

#### Constructor

```python
def __init__(self, page: Page):
    """Initialize Header Page."""
```

#### Attributes

```python
self.validation_results: Dict = {
    'header_exists': bool,
    'logo_exists': bool,
    'logo_clickable': bool,
    'login_button_exists': bool,
    'login_button_clickable': bool,
    'language_switcher_exists': bool,
    'language_switcher_clickable': bool,
    'dropdowns': List[Dict],
    'nav_items_count': int,
    'screenshots': List[str]
}
```

#### Methods

```python
def find_header() -> Optional[Locator]:
    """Find header element."""

def is_header_visible() -> bool:
    """Check if header is visible."""

def find_logo() -> Optional[Locator]:
    """Find logo element."""

def validate_logo() -> Dict:
    """Validate logo presence and properties."""

def find_login_button() -> Optional[Locator]:
    """Find login button."""

def validate_login_button() -> Dict:
    """Validate login button presence and clickability."""

def find_language_switcher() -> Optional[Locator]:
    """Find language switcher."""

def validate_language_switcher() -> Dict:
    """Validate language switcher presence and functionality."""

def find_dropdowns() -> List[Locator]:
    """Find all dropdown menus in header."""

def validate_dropdowns() -> Dict:
    """Validate dropdown menus presence and functionality."""

def count_nav_items() -> int:
    """Count navigation items in header."""

def validate_all() -> Dict:
    """Run all header validations."""

def print_summary() -> None:
    """Print validation summary."""

def get_results() -> Dict:
    """Get validation results."""
```

#### Usage Example

```python
from pages.header_page import HeaderPage

# Initialize
header_page = HeaderPage(page)

# Navigate
header_page.navigate("https://example.com")

# Check header
if header_page.is_header_visible():
    # Validate all elements
    results = header_page.validate_all()
    
    # Access results
    print(f"Logo exists: {results['logo_exists']}")
    print(f"Login button exists: {results['login_button_exists']}")
    print(f"Dropdowns found: {results['dropdowns_count']}")
```

---

### FooterPage Class

**Location:** `pages/footer_page.py`

Page Object for footer validation and interactions.

#### Constructor

```python
def __init__(self, page: Page):
    """Initialize Footer Page."""
```

#### Attributes

```python
self.validation_results: Dict = {
    'footer_exists': bool,
    'social_links_count': int,
    'footer_links_count': int,
    'newsletter_exists': bool,
    'screenshots': List[str]
}
```

#### Methods

```python
def find_footer() -> Optional[Locator]:
    """Find footer element."""

def is_footer_visible() -> bool:
    """Check if footer is visible."""

def find_social_links() -> List[Locator]:
    """Find all social media links in footer."""

def validate_social_links() -> Dict:
    """Validate social media links presence."""

def find_footer_links() -> List[Locator]:
    """Find all links in footer."""

def validate_footer_links() -> Dict:
    """Validate footer links presence."""

def find_newsletter_input() -> Optional[Locator]:
    """Find newsletter input field."""

def validate_newsletter() -> Dict:
    """Validate newsletter signup presence."""

def validate_all() -> Dict:
    """Run all footer validations."""

def print_summary() -> None:
    """Print validation summary."""

def get_results() -> Dict:
    """Get validation results."""
```

#### Usage Example

```python
from pages.footer_page import FooterPage

# Initialize
footer_page = FooterPage(page)

# Navigate
footer_page.navigate("https://example.com")

# Validate footer
if footer_page.is_footer_visible():
    results = footer_page.validate_all()
    
    print(f"Social links: {results['social_links_count']}")
    print(f"Footer links: {results['footer_links_count']}")
    print(f"Newsletter: {results['newsletter_exists']}")
```

---

## Core Utilities

### BrowserManager Class

**Location:** `core/browser_manager.py`

Manages browser lifecycle and context.

#### Constructor

```python
def __init__(self):
    """Initialize Browser Manager."""
```

#### Context Manager

```python
def __enter__(self):
    """Context manager entry - start browser."""

def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit - cleanup resources."""
```

#### Methods

```python
def start() -> Page:
    """Start browser and create page."""

def get_page() -> Optional[Page]:
    """Get current page instance."""

def get_context() -> Optional[BrowserContext]:
    """Get current browser context."""

def get_browser() -> Optional[Browser]:
    """Get current browser instance."""

def save_trace(filename: str = "trace.zip") -> Optional[str]:
    """Save trace file if tracing is enabled."""

def take_screenshot(filename: str, full_page: bool = True) -> Optional[str]:
    """Take screenshot of current page."""

def get_browser_info() -> Dict[str, Any]:
    """Get browser information."""

def cleanup() -> None:
    """Clean up browser resources."""
```

#### Usage Example

```python
from core.browser_manager import BrowserManager

# Using context manager (recommended)
with BrowserManager() as browser:
    page = browser.get_page()
    page.goto("https://example.com")
    # ... do work ...
# Automatic cleanup

# Manual usage
browser_manager = BrowserManager()
page = browser_manager.start()
# ... do work ...
browser_manager.cleanup()
```

---

### Logger Class

**Location:** `core/logger.py`

Centralized logging with colored output.

#### Static Methods

```python
@classmethod
def get_logger(cls, name: str = None) -> logging.Logger:
    """Get or create logger instance."""

@classmethod
def reset(cls) -> None:
    """Reset logger instance (useful for testing)."""
```

#### Usage Example

```python
from core.logger import Logger

# Get logger
logger = Logger.get_logger()

# Log messages
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.debug("Debug message")
```

---

### Reporter Class

**Location:** `core/reporter.py`

Generates HTML and JSON reports.

#### Constructor

```python
def __init__(self):
    """Initialize Reporter."""
```

#### Methods

```python
def add_data(self, key: str, value: Any) -> None:
    """Add data to report."""

def add_multiple(self, data: Dict[str, Any]) -> None:
    """Add multiple data items to report."""

def get_data(self, key: str, default: Any = None) -> Any:
    """Get data from report."""

def generate_json_report(self, filename: str = None) -> Optional[str]:
    """Generate JSON report."""

def generate_html_report(self, filename: str = None) -> Optional[str]:
    """Generate HTML report with embedded screenshots."""
```

#### Usage Example

```python
from core.reporter import Reporter

# Initialize
reporter = Reporter()

# Add data
reporter.add_data('url', 'https://example.com')
reporter.add_data('status_code', 200)
reporter.add_data('header_found', True)

# Add multiple
reporter.add_multiple({
    'footer_found': True,
    'exit_code': 0
})

# Generate reports
reporter.generate_json_report()
reporter.generate_html_report()
```

---

## Usage Examples

### Example 1: Basic Validation

```python
from core.browser_manager import BrowserManager
from pages.header_page import HeaderPage
from pages.footer_page import FooterPage

with BrowserManager() as browser:
    page = browser.get_page()
    
    # Header validation
    header_page = HeaderPage(page)
    header_page.navigate("https://example.com")
    header_results = header_page.validate_all()
    
    # Footer validation
    footer_page = FooterPage(page)
    footer_results = footer_page.validate_all()
    
    print(header_results)
    print(footer_results)
```

### Example 2: Custom Validation

```python
from pages.base_page import BasePage
from config.locators import Locators

class CustomPage(BasePage):
    def validate_search_box(self):
        search = self.find_element(Locators.Header.SEARCH_BOX)
        if search:
            return self.is_element_clickable(search)
        return False

# Usage
with BrowserManager() as browser:
    page = browser.get_page()
    custom_page = CustomPage(page)
    custom_page.navigate("https://example.com")
    
    has_search = custom_page.validate_search_box()
    print(f"Search box available: {has_search}")
```

### Example 3: With Reporting

```python
from core.browser_manager import BrowserManager
from core.reporter import Reporter
from pages.header_page import HeaderPage

reporter = Reporter()

with BrowserManager() as browser:
    page = browser.get_page()
    
    header_page = HeaderPage(page)
    success, status = header_page.navigate("https://example.com")
    
    reporter.add_data('url', 'https://example.com')
    reporter.add_data('status_code', status)
    
    results = header_page.validate_all()
    reporter.add_data('header_details', results)
    
    # Generate reports
    reporter.generate_html_report()
    reporter.generate_json_report()
```

---

## Best Practices

1. **Always use context manager for BrowserManager**
   ```python
   with BrowserManager() as browser:
       # Your code here
   ```

2. **Inherit from BasePage for custom pages**
   ```python
   class MyPage(BasePage):
       def __init__(self, page):
           super().__init__(page)
   ```

3. **Use locators from config**
   ```python
   from config.locators import Locators
   logo = self.find_element(Locators.Header.LOGO)
   ```

4. **Handle errors gracefully**
   ```python
   element = self.find_element(selectors)
   if element:
       self.click_element(element)
   else:
       self.logger.warning("Element not found")
   ```

5. **Use type hints**
   ```python
   def my_method(self, param: str) -> bool:
       return True
   ```

---

## Error Handling

All methods handle errors internally and log them. Methods return:
- `None` for failed element finding
- `False` for failed actions
- Empty lists for failed element collections
- Tuple `(False, None)` for failed navigation

Always check return values:

```python
element = page_object.find_element(selectors)
if element:
    # Element found, proceed
    page_object.click_element(element)
else:
    # Element not found, handle error
    logger.error("Element not found")
```

---

**For more examples, see the `tests/` directory.**
