# 🧪 Playwright Website Validator (OOP Version)

Professional website validation framework using Playwright and Page Object Model (POM) design pattern.

## 📋 Features

✅ **Object-Oriented Architecture** - Clean, maintainable code using OOP principles  
✅ **Page Object Model (POM)** - Industry-standard design pattern  
✅ **Comprehensive Header Validation** - Logo, Login, Language Switcher, Dropdowns  
✅ **Footer Validation** - Social links, Footer links, Newsletter  
✅ **Smart Screenshot Capture** - Multiple strategies with element-level screenshots  
✅ **Rich HTML Reports** - Beautiful reports with embedded screenshots  
✅ **JSON Reports** - Machine-readable validation results  
✅ **Configurable** - Centralized configuration via environment variables  
✅ **Retry Logic** - Automatic retries for navigation failures  
✅ **Colored Logging** - Clear, colored console output  
✅ **Tracing Support** - Optional Playwright tracing for debugging  

---

## 🏗️ Project Structure

```
MY_Project/
├── config/
│   ├── __init__.py
│   ├── settings.py          # All configuration settings
│   └── locators.py          # All element selectors (clickable elements)
├── pages/
│   ├── __init__.py
│   ├── base_page.py         # Base Page Object with common methods
│   ├── header_page.py       # Header Page Object
│   └── footer_page.py       # Footer Page Object
├── core/
│   ├── __init__.py
│   ├── browser_manager.py   # Browser lifecycle management
│   ├── logger.py            # Logging utility
│   └── reporter.py          # Report generation (HTML/JSON)
├── tests/
│   ├── __init__.py
│   └── test_website_validation.py
├── reports/                 # Generated reports
├── screenshots/             # Captured screenshots
├── logs/                    # Log files
├── traces/                  # Playwright traces (if enabled)
├── run.py                   # Main entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

---

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Installation

```bash
# Clone or download the project
cd MY_Project

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Run Validation

```bash
# Run with default settings
python run.py

# Run with custom URL (via environment variable)
set TARGET_URL=https://example.com && python run.py

# Run in headed mode (see browser)
set HEADLESS=false && python run.py
```

---

## ⚙️ Configuration

### Settings File: `config/settings.py`

All configuration is centralized in `config/settings.py`. Key settings:

```python
# Target website
TARGET_URL = "https://shopdev.ooredoo.com.kw/"

# Browser settings
BROWSER_TYPE = "chromium"  # chromium, firefox, webkit
HEADLESS = True
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080

# Timeouts (milliseconds)
NAVIGATION_TIMEOUT = 60000
ELEMENT_TIMEOUT = 10000

# Screenshot strategy
SCREENSHOT_STRATEGY = "fullpage"  # fullpage, viewport, element, random

# Reports
GENERATE_HTML_REPORT = True
GENERATE_JSON_REPORT = True
EMBED_SCREENSHOTS_IN_HTML = True

# Validation options
VALIDATE_HEADER = True
VALIDATE_FOOTER = True
VALIDATE_HEADER_ELEMENTS = True  # Deep header validation
```

### Environment Variables

Override settings using environment variables:

```bash
# Windows
set TARGET_URL=https://example.com
set BROWSER_TYPE=firefox
set HEADLESS=false
set SCREENSHOT_STRATEGY=viewport

# Linux/Mac
export TARGET_URL=https://example.com
export BROWSER_TYPE=firefox
export HEADLESS=false
```

### Locators File: `config/locators.py`

All element selectors are organized in `config/locators.py`:

- **Header Locators**: Logo, Login Button, Language Switcher, Dropdowns, Nav Items
- **Footer Locators**: Social Links, Footer Links, Newsletter
- **Interactive Elements**: Buttons, Links, Inputs, Checkboxes

**Example:**
```python
# Get all header clickable elements
clickable_elements = Locators.get_header_clickable_elements()

# Access specific selectors
logo_selectors = Locators.Header.LOGO
login_selectors = Locators.Header.LOGIN_BUTTON
```

---

## 📊 Reports

### HTML Report

Beautiful, interactive HTML report with:
- Overview dashboard
- Header validation details
- Footer validation details
- Embedded screenshots
- Element-level screenshots

**Location:** `reports/report_YYYYMMDD_HHMMSS.html`

### JSON Report

Machine-readable JSON report with all validation data.

**Location:** `reports/report_YYYYMMDD_HHMMSS.json`

**Example:**
```json
{
  "timestamp": "2025-01-29 22:30:00",
  "url": "https://shopdev.ooredoo.com.kw/",
  "status_code": 200,
  "header_found": true,
  "header_details": {
    "logo_exists": true,
    "login_button_exists": true,
    "language_switcher_exists": true,
    "dropdowns_count": 3
  },
  "exit_code": 0
}
```

---

## 🎯 Usage Examples

### Basic Validation

```python
from core.browser_manager import BrowserManager
from pages.header_page import HeaderPage

# Initialize browser
with BrowserManager() as browser:
    page = browser.get_page()
    
    # Navigate
    page.goto("https://example.com")
    
    # Validate header
    header_page = HeaderPage(page)
    results = header_page.validate_all()
    
    print(results)
```

### Custom Validation

```python
from pages.base_page import BasePage
from config.locators import Locators

# Create custom page object
class CustomPage(BasePage):
    def validate_custom_element(self):
        element = self.find_element(Locators.Header.LOGO)
        return element is not None
```

---

## 🧪 Testing

### Run Tests (if using pytest)

```bash
# Run all tests
pytest

# Run with HTML report
pytest --html=test_report.html

# Run specific test
pytest tests/test_header.py
```

---

## 📝 Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - All validations passed |
| 1 | Navigation failed |
| 2 | Required elements missing (header/footer) |
| 3 | Screenshot capture failed |
| 4 | Validation failed |
| 99 | Unknown error |
| 130 | User interrupted (Ctrl+C) |

---

## 🔧 Troubleshooting

### Issue: Browser not launching

**Solution:**
```bash
# Reinstall Playwright browsers
playwright install --force chromium
```

### Issue: Elements not found

**Solution:**
1. Check `config/locators.py` and add more selectors
2. Increase `ELEMENT_TIMEOUT` in `config/settings.py`
3. Run in headed mode to see what's happening: `set HEADLESS=false`

### Issue: Navigation timeout

**Solution:**
1. Increase `NAVIGATION_TIMEOUT` in `config/settings.py`
2. Change `WAIT_UNTIL` to `"domcontentloaded"` instead of `"load"`

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **README.md** | Main documentation (this file) |
| **API_DOCUMENTATION.md** | Complete API reference |
| **CHANGELOG.md** | Version history and changes |
| **PROJECT_SUMMARY.md** | Project overview |
| **QUICK_REFERENCE.md** | Quick reference guide |
| **MIGRATION_GUIDE.md** | Migration from v1.0 to v2.0 |

---

## 🎓 Best Practices

### 1. Page Object Model
- Keep page logic in page objects
- Use `BasePage` for common functionality
- One page object per page/section

### 2. Locators
- Centralize all selectors in `config/locators.py`
- Use multiple fallback selectors
- Prefer data-testid attributes

### 3. Configuration
- Use environment variables for CI/CD
- Keep sensitive data out of code
- Document all settings

### 4. Reporting
- Enable screenshot embedding for portability
- Generate both HTML and JSON reports
- Archive old reports regularly

---

## 📄 License

This project is for internal use and testing purposes.

---

## 👤 Author

**QA Automation Team**

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review logs in `logs/` directory
3. Enable tracing: `ENABLE_TRACING=true`
4. Run in headed mode: `HEADLESS=false`

---

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Complete OOP refactoring
- ✅ Page Object Model implementation
- ✅ Centralized configuration
- ✅ Improved reporting with embedded screenshots
- ✅ Better error handling and logging

### v1.0.0
- Initial procedural version

---

**Happy Testing! 🚀**
#   p r o j e c t _ b 2 b  
 #   p r o j e c t _ b 2 b  
 