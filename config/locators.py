"""
Locators Configuration - All element selectors centralized here.
Organized by page sections for easy maintenance.
"""

from typing import List, Dict


class Locators:
    """
    Centralized locators class containing all element selectors.
    Organized by page sections (Header, Footer, etc.)
    """
    
    # ===== Header Locators =====
    class Header:
        """Header section locators."""
        
        # Main header container
        CONTAINER: List[str] = [
            'header',
            '[role="banner"]',
            '.header',
            '#header',
            'nav',
            '.navbar',
            '.site-header',
            '.page-header',
            '.top-bar',
        ]
        
        # Logo selectors
        LOGO: List[str] = [
            'img[alt*="logo" i]',
            'img[class*="logo" i]',
            'img[id*="logo" i]',
            'a[class*="logo" i] img',
            '.logo img',
            '#logo img',
            '[data-testid*="logo" i]',
            'svg[class*="logo" i]',
            '.brand img',
            '.navbar-brand img',
        ]
        
        # Login button selectors
        LOGIN_BUTTON: List[str] = [
            # Text-based (English)
            'button:has-text("login")',
            'button:has-text("sign in")',
            'a:has-text("login")',
            'a:has-text("sign in")',
            
            # Text-based (Arabic)
            'button:has-text("تسجيل الدخول")',
            'button:has-text("دخول")',
            'a:has-text("تسجيل الدخول")',
            'a:has-text("دخول")',
            
            # Class/ID based
            'button[class*="login" i]',
            'button[id*="login" i]',
            'a[class*="login" i]',
            'a[id*="signin" i]',
            '.login-button',
            '.signin-button',
            '#login-btn',
            
            # Data attributes
            'button[data-testid*="login" i]',
            'a[href*="login"]',
            'a[href*="signin"]',
        ]
        
        # Language switcher selectors
        LANGUAGE_SWITCHER: List[str] = [
            # Ooredoo specific - Arabic/English toggle
            '#aren',
            'a[href*="___store=ar"]',
            'a[href*="___store=en"]',
            'a[title*="عربي"]',
            'a[title*="Arabic"]',
            'a[title*="English"]',
            '.switcher-language a',
            '.language-switcher a',
            
            # Text-based (exact match)
            'a:has-text("عربي")',
            'a:has-text("English")',
            'button:has-text("عربي")',
            'button:has-text("English")',
            
            # Generic text-based
            'button:has-text("EN")',
            'button:has-text("AR")',
            'a:has-text("EN")',
            'a:has-text("AR")',
            
            # Class/ID based
            'button[class*="language" i]',
            'button[class*="lang" i]',
            'button[id*="language" i]',
            'select[class*="language" i]',
            '.language-switcher',
            '.lang-switcher',
            '#language-selector',
            
            # Data attributes
            'button[data-testid*="language" i]',
            '[aria-label*="language" i]',
            
            # Icon-based
            'button:has(svg[class*="globe" i])',
            'button:has(.fa-globe)',
            'button:has([class*="translate" i])',
        ]
        
        # Dropdown menu selectors
        DROPDOWNS: List[str] = [
            # Magento/Ooredoo specific
            'nav li.level0.parent',
            'nav li.level0 > a',
            '.navigation li.parent > a',
            'nav .level-top',
            'li.level0.parent',
            
            # Generic dropdown patterns
            'button[aria-expanded]',
            'button[aria-haspopup="true"]',
            'a[aria-haspopup="true"]',
            '[role="button"][aria-expanded]',
            '.dropdown-toggle',
            'button.dropdown',
            'nav button',
            'nav [role="button"]',
            '.nav-item.dropdown',
            'nav li.dropdown > a',
            'nav li.parent > a',
            
            # Icon-based
            'button:has(svg[class*="chevron" i])',
            'button:has(svg[class*="arrow" i])',
            'a:has(svg[class*="chevron" i])',
            'a:has(svg[class*="arrow" i])',
            'button:has(.fa-chevron-down)',
            'button:has(.fa-caret-down)',
        ]
        
        # Navigation menu items
        NAV_ITEMS: List[str] = [
            'nav a',
            '.nav-link',
            '.menu-item',
            '[role="menuitem"]',
            'header a[href]',
        ]
        
        # Search box
        SEARCH_BOX: List[str] = [
            '#search',
            '[name="q"]',
            '[aria-label*="search" i]',
            'input[type="search"]',
            '.search-input',
            '.search-field',
            '.search-box input',
        ]

        # Search icon
        SEARCH_ICON: List[str] = [
            '.search_icon .sicon',
            '.search-icon',
            '[aria-label*="search" i]',
            'button[type="submit"]',
            '.search-button',
            '.search-submit',
        ]

        # Search results
        SEARCH_RESULTS_CONTAINER: List[str] = [
            '#search_autocomplete',
            '.search-autocomplete',
            '.autocomplete-results',
            '.search-results',
            '[role="listbox"]',
            '.dropdown-menu.search',
        ]
        
        # Cart/Shopping bag
        CART_BUTTON: List[str] = [
            'a.action.showcart',
            'button[aria-label*="cart" i]',
            'a[href*="cart"]',
            '.cart-button',
            '.shopping-cart',
            'button:has(svg[class*="cart" i])',
            '[data-testid*="cart" i]',
        ]
    
    # ===== Footer Locators =====
    class Footer:
        """Footer section locators."""
        
        # Main footer container
        CONTAINER: List[str] = [
            'footer',
            '[role="contentinfo"]',
            '.footer',
            '#footer',
            '.site-footer',
            '.page-footer',
            '.bottom-bar',
        ]
        
        # Social media links
        SOCIAL_LINKS: List[str] = [
            'a[href*="facebook"]',
            'a[href*="twitter"]',
            'a[href*="instagram"]',
            'a[href*="youtube"]',
            'a[href*="linkedin"]',
            '.social-link',
            '.social-icon',
            '[class*="social" i] a',
        ]
        
        # Footer links
        FOOTER_LINKS: List[str] = [
            'footer a',
            '.footer a',
            '.footer-links a',
            '.footer-nav a',
        ]
        
        # Copyright text
        COPYRIGHT: List[str] = [
            '.copyright',
            '.footer-copyright',
            'footer :has-text("©")',
            'footer :has-text("Copyright")',
        ]
    
    # ===== Home Page Locators =====
    class Home:
        """Home page locators."""
        
        # Main content area
        MAIN_CONTENT: List[str] = [
            'main',
            '[role="main"]',
            '.main',
            '#maincontent',
            '.content',
        ]
        
        # Hero/banner section
        HERO_SECTION: List[str] = [
            '.hero',
            '.banner',
            '.jumbotron',
            '.hero-banner',
            '.hero-section',
            '.slider',
        ]
        
        # Featured products
        FEATURED_PRODUCTS: List[str] = [
            '.products-grid',
            '.product-grid',
            '.featured-products',
            '.product-items',
        ]
        
        # Product item
        PRODUCT_ITEM: List[str] = [
            '.product-item',
            '.item.product',
            '[data-role="product-item"]',
        ]
        
        # Product name
        PRODUCT_NAME: List[str] = [
            '.product-name',
            '.product-item-link',
            '.product-title',
        ]
        
        # Product price
        PRODUCT_PRICE: List[str] = [
            '.price',
            '.product-price',
            '.regular-price',
        ]
        
        # Add to cart button
        ADD_TO_CART_BUTTON: List[str] = [
            'button[title*="Add to Cart" i]',
            '.action.tocart',
            '.add-to-cart',
            '.btn-cart',
        ]
