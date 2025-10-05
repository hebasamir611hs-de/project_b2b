# ⚡ Quick Reference Guide

Fast reference for common tasks and commands.

---

## 🚀 Quick Start

```bash
# Setup (first time only)
pip install -r requirements.txt
playwright install chromium

# Run validation
python run.py

# Run tests
pytest
```

---

## 📝 Common Commands

### Running Validation

```bash
# Default run
python run.py

# Custom URL
set TARGET_URL=https://example.com && python run.py

# Headed mode (see browser)
set HEADLESS=false && python run.py

# Different browser
set BROWSER_TYPE=firefox && python run.py
```

### Running Tests

```bash
# All tests
pytest

# Specific marker
pytest -m smoke
pytest -m regression
pytest -m header

# Specific file
pytest tests/test_website_validation.py

# With HTML report
pytest --html=report.html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

---

## 🔧 Configuration Quick Edit

### Environment Variables (Quick Override)

```bash
# Windows
set TARGET_URL=https://example.com
set BROWSER_TYPE=chromium
set HEADLESS=true
set SCREENSHOT_STRATEGY=fullpage
set LOG_LEVEL=INFO

# Linux/Mac
export TARGET_URL=https://example.com
export BROWSER_TYPE=chromium
export HEADLESS=true
```

### Settings File: `config/settings.py`

```python
# Most commonly changed settings:

TARGET_URL = "https://your-site.com"
BROWSER_TYPE = "chromium"  # chromium, firefox, webkit
HEADLESS = True
SCREENSHOT_STRATEGY = "fullpage"  # fullpage, viewport, element
VALIDATE_HEADER_ELEMENTS = True
TAKE_ELEMENT_SCREENSHOTS = True
```

---

## 📊 Import Cheat Sheet

```python
# Configuration
from config.settings import Settings
from config.locators import Locators

# Core
from core.browser_manager import BrowserManager
from core.logger import Logger
from core.reporter import Reporter

# Pages
from pages.base_page import BasePage
from pages.header_page import HeaderPage
from pages.footer_page import FooterPage
```

---

## 💻 Code Snippets

### Basic Validation Script

```python
from core.browser_manager import BrowserManager
from pages.header_page import HeaderPage

with BrowserManager() as browser:
    page = browser.get_page()
    
    header_page = HeaderPage(page)
    header_page.navigate("https://example.com")
    results = header_page.validate_all()
    
    print(results)
```

### Custom Page Object

```python
from pages.base_page import BasePage
from config.locators import Locators

class MyPage(BasePage):
    def validate_element(self):
        element = self.find_element(Locators.Header.LOGO)
        return element is not None
```

### Using Reporter

```python
from core.reporter import Reporter

reporter = Reporter()
reporter.add_data('url', 'https://example.com')
reporter.add_data('status', 200)
reporter.generate_html_report()
reporter.generate_json_report()
```

### Finding Elements

```python
# Single element
logo = page_object.find_element(Locators.Header.LOGO)

# Check visibility
is_visible = page_object.is_element_visible(
    Locators.Header.LOGIN_BUTTON,
    "login button"
)

# Multiple elements
nav_items = page_object.get_all_elements(Locators.Header.NAV_ITEMS)
```

### Taking Screenshots

```python
# Page screenshot
page_object.take_page_screenshot("my_screenshot", full_page=True)

# Element screenshot
element = page_object.find_element(selectors)
page_object.take_element_screenshot(element, "element_screenshot")
```

---

## 🎯 Locators Quick Access

```python
from config.locators import Locators

# Header
Locators.Header.CONTAINER
Locators.Header.LOGO
Locators.Header.LOGIN_BUTTON
Locators.Header.LANGUAGE_SWITCHER
Locators.Header.DROPDOWNS
Locators.Header.NAV_ITEMS

# Footer
Locators.Footer.CONTAINER
Locators.Footer.SOCIAL_LINKS
Locators.Footer.FOOTER_LINKS
Locators.Footer.NEWSLETTER_INPUT

# Get all clickable
all_clickable = Locators.get_all_clickable_selectors()

# Get organized
header_elements = Locators.get_header_clickable_elements()
```

---

## 🔍 Debugging

### Enable Debug Mode

```python
# In config/settings.py
LOG_LEVEL = "DEBUG"
HEADLESS = False
ENABLE_TRACING = True
```

### View Logs

```bash
# Windows
type logs\validation_*.log

# Linux/Mac
cat logs/validation_*.log
```

### Check Reports

```bash
# Open latest HTML report
start reports\report_*.html

# View JSON report
type reports\report_*.json
```

---

## 📊 Exit Codes Reference

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Navigation failed |
| 2 | Elements missing |
| 3 | Screenshot failed |
| 99 | Unknown error |
| 130 | User interrupted |

---

## 🧪 Test Markers

```bash
pytest -m smoke        # Quick smoke tests
pytest -m regression   # Full regression
pytest -m header       # Header tests only
pytest -m footer       # Footer tests only
pytest -m navigation   # Navigation tests
```

---

## 📁 File Locations

| Type | Location |
|------|----------|
| Reports | `reports/report_*.html` |
| Screenshots | `screenshots/*.png` |
| Logs | `logs/validation_*.log` |
| Traces | `traces/trace_*.zip` |
| Config | `config/settings.py` |
| Locators | `config/locators.py` |

---

## ⚙️ Settings Quick Reference

```python
# Browser
BROWSER_TYPE = "chromium"  # chromium, firefox, webkit
HEADLESS = True
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Timeouts (ms)
NAVIGATION_TIMEOUT = 60000
ELEMENT_TIMEOUT = 10000
ACTION_TIMEOUT = 5000

# Screenshot
SCREENSHOT_STRATEGY = "fullpage"
SCREENSHOT_FORMAT = "png"
TAKE_ELEMENT_SCREENSHOTS = True
SCREENSHOT_ON_HOVER = True

# Validation
VALIDATE_HEADER = True
VALIDATE_FOOTER = True
VALIDATE_HEADER_ELEMENTS = True

# Reports
GENERATE_HTML_REPORT = True
GENERATE_JSON_REPORT = True
EMBED_SCREENSHOTS_IN_HTML = True

# Logging
LOG_LEVEL = "INFO"
LOG_TO_FILE = True
```

---

## 🔧 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Browser won't launch | `playwright install chromium` |
| Elements not found | Check `config/locators.py` |
| Timeout errors | Increase timeouts in `settings.py` |
| Import errors | `pip install -r requirements.txt` |
| Permission errors | Run as administrator |

---

## 📞 Quick Help

```bash
# Python help
python --version
pip list

# Playwright help
playwright --version
playwright install --help

# Pytest help
pytest --help
pytest --markers
```

---

## 🎨 Common Patterns

### Pattern 1: Navigate and Validate

```python
with BrowserManager() as browser:
    page = browser.get_page()
    page_object = HeaderPage(page)
    page_object.navigate(url)
    results = page_object.validate_all()
```

### Pattern 2: Find and Click

```python
element = page_object.find_element(selectors)
if element:
    page_object.click_element(element, "element name")
```

### Pattern 3: Check and Screenshot

```python
if page_object.is_element_visible(selectors, "element"):
    element = page_object.find_element(selectors)
    page_object.take_element_screenshot(element, "screenshot_name")
```

### Pattern 4: Validate and Report

```python
results = page_object.validate_all()
reporter.add_data('validation_results', results)
reporter.generate_html_report()
```

---

## 🚀 Performance Tips

1. **Use headless mode** for faster execution
2. **Reduce timeouts** for known-fast sites
3. **Disable screenshots** if not needed
4. **Use viewport strategy** instead of fullpage
5. **Disable tracing** in production

```python
# Fast configuration
HEADLESS = True
NAVIGATION_TIMEOUT = 30000
ELEMENT_TIMEOUT = 5000
TAKE_ELEMENT_SCREENSHOTS = False
SCREENSHOT_STRATEGY = "viewport"
ENABLE_TRACING = False
```

---

## 📚 Documentation Links

- **README.md** - Main documentation
- **API_DOCUMENTATION.md** - Complete API reference
- **CHANGELOG.md** - Version history
- **PROJECT_SUMMARY.md** - Project overview

---

## 🎯 One-Liners

```bash
# Quick validation
python run.py

# Quick test
pytest -m smoke

# View latest report
start reports\report_*.html

# Check logs
type logs\validation_*.log | more

# Clean artifacts
del /Q screenshots\*.png reports\*.html reports\*.json logs\*.log
```

---

**Keep this file handy for quick reference! 📌**
