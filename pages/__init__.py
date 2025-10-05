"""
Page Objects package following Page Object Model (POM) pattern.
"""

from .base_page import BasePage
from .header_page import HeaderPage
from .footer_page import FooterPage

__all__ = ['BasePage', 'HeaderPage', 'FooterPage']
