"""
Reporter - Generates HTML and JSON reports with embedded screenshots.
"""

import json
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import Settings
from .logger import Logger


class Reporter:
    """
    Handles report generation in various formats.
    Supports HTML with embedded screenshots and JSON.
    """
    
    def __init__(self):
        """Initialize Reporter."""
        self.logger = Logger.get_logger()
        self.settings = Settings
        self.report_data: Dict[str, Any] = {}
    
    def add_data(self, key: str, value: Any) -> None:
        """
        Add data to report.
        
        Args:
            key: Data key
            value: Data value
        """
        self.report_data[key] = value
    
    def add_multiple(self, data: Dict[str, Any]) -> None:
        """
        Add multiple data items to report.
        
        Args:
            data: Dictionary of data to add
        """
        self.report_data.update(data)
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get data from report.
        
        Args:
            key: Data key
            default: Default value if key not found
        
        Returns:
            Data value or default
        """
        return self.report_data.get(key, default)

    def log_section(self, message: str) -> None:
        """
        Log a section message.
        """
        self.logger.info(message)

    def log_info(self, message: str) -> None:
        """
        Log an info message.
        """
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """
        Log a warning message.
        """
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        """
        Log an error message.
        """
        self.logger.error(message)
    
    def generate_json_report(self, filename: str = None) -> Optional[str]:
        """
        Generate JSON report.
        
        Args:
            filename: Custom filename (optional)
        
        Returns:
            Path to report file or None
        """
        if not self.settings.GENERATE_JSON_REPORT:
            return None
        
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"report_{timestamp}.json"
            
            report_path = self.settings.REPORTS_DIR / filename
            
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(self.report_data, f, indent=2, ensure_ascii=False, default=str)
            
            self.logger.info(f"✓ JSON report saved: {report_path.name}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {str(e)}")
            return None
    
    def generate_html_report(self, filename: str = None) -> Optional[str]:
        """
        Generate HTML report with embedded screenshots.
        
        Args:
            filename: Custom filename (optional)
        
        Returns:
            Path to report file or None
        """
        if not self.settings.GENERATE_HTML_REPORT:
            return None
        
        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"report_{timestamp}.html"
            
            report_path = self.settings.REPORTS_DIR / filename
            
            html_content = self._create_html_report()
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"✓ HTML report saved: {report_path.name}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {str(e)}")
            return None
    
    def _image_to_base64(self, image_path: str) -> Optional[str]:
        """
        Convert image to base64 string.
        
        Args:
            image_path: Path to image file
        
        Returns:
            Base64 encoded string or None
        """
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except:
            return None
    
    def _create_html_report(self) -> str:
        """
        Create HTML report content with embedded screenshots.
        
        Returns:
            HTML content as string
        """
        # Get data
        url = self.report_data.get('url', 'N/A')
        timestamp = self.report_data.get('timestamp', 'N/A')
        status_code = self.report_data.get('status_code')
        navigation_success = self.report_data.get('navigation_success', False)
        header_found = self.report_data.get('header_found', False)
        footer_found = self.report_data.get('footer_found', False)
        exit_code = self.report_data.get('exit_code', 99)
        screenshot_path = self.report_data.get('screenshot_path')
        header_details = self.report_data.get('header_details', {})
        footer_details = self.report_data.get('footer_details', {})
        
        # Status colors
        status_class = 'status-success' if status_code == 200 else 'status-error'
        header_class = 'status-success' if header_found else 'status-error'
        footer_class = 'status-success' if footer_found else 'status-error'
        exit_class = 'status-success' if exit_code == 0 else 'status-error'
        
        # Build header details HTML
        header_html = self._build_header_details_html(header_details)
        
        # Build footer details HTML
        footer_html = self._build_footer_details_html(footer_details)
        
        # Build screenshot HTML
        screenshot_html = self._build_screenshot_html(screenshot_path)
        
        # Build element screenshots HTML
        element_screenshots_html = self._build_element_screenshots_html(header_details)
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Website Validation Report - {timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .info-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }}
        
        .info-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .info-card h3 {{
            color: #34495e;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }}
        
        .info-card p {{
            font-size: 1.4em;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .status-success {{ color: #27ae60; }}
        .status-error {{ color: #e74c3c; }}
        .status-warning {{ color: #f39c12; }}
        
        .details-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        .details-table th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        .details-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
        }}
        
        .details-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .details-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .screenshot-container {{
            margin: 20px 0;
            text-align: center;
        }}
        
        .screenshot-container img {{
            max-width: 100%;
            border: 2px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .element-screenshots {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .element-screenshot {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .element-screenshot h4 {{
            color: #34495e;
            margin-bottom: 10px;
        }}
        
        .element-screenshot img {{
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-error {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Website Validation Report</h1>
            <p>{Settings.PROJECT_NAME} v{Settings.PROJECT_VERSION}</p>
        </div>
        
        <div class="content">
            <!-- Overview Section -->
            <div class="section">
                <h2 class="section-title">📊 Overview</h2>
                <div class="info-grid">
                    <div class="info-card">
                        <h3>Target URL</h3>
                        <p style="font-size: 1em; word-break: break-all;">{url}</p>
                    </div>
                    <div class="info-card">
                        <h3>Validation Date</h3>
                        <p style="font-size: 1.1em;">{timestamp}</p>
                    </div>
                    <div class="info-card">
                        <h3>HTTP Status</h3>
                        <p class="{status_class}">{status_code if status_code else 'N/A'}</p>
                    </div>
                    <div class="info-card">
                        <h3>Navigation</h3>
                        <p class="{'status-success' if navigation_success else 'status-error'}">
                            {'✓ Success' if navigation_success else '✗ Failed'}
                        </p>
                    </div>
                    <div class="info-card">
                        <h3>Header Present</h3>
                        <p class="{header_class}">{'✓ Yes' if header_found else '✗ No'}</p>
                    </div>
                    <div class="info-card">
                        <h3>Footer Present</h3>
                        <p class="{footer_class}">{'✓ Yes' if footer_found else '✗ No'}</p>
                    </div>
                    <div class="info-card">
                        <h3>Exit Code</h3>
                        <p class="{exit_class}">{exit_code}</p>
                    </div>
                    <div class="info-card">
                        <h3>Browser</h3>
                        <p style="font-size: 1.1em;">{Settings.BROWSER_TYPE.capitalize()}</p>
                    </div>
                </div>
            </div>
            
            {header_html}
            
            {footer_html}
            
            {screenshot_html}
            
            {element_screenshots_html}
        </div>
        
        <div class="footer">
            <p>Generated by {Settings.PROJECT_NAME} v{Settings.PROJECT_VERSION}</p>
            <p>© 2025 - Automated Website Validation</p>
        </div>
    </div>
</body>
</html>"""
    
    def _build_header_details_html(self, header_details: Dict) -> str:
        """Build HTML for header validation details."""
        if not header_details:
            return ""
        
        logo_badge = self._get_badge(header_details.get('logo_exists', False))
        login_badge = self._get_badge(header_details.get('login_button_exists', False))
        lang_badge = self._get_badge(header_details.get('language_switcher_exists', False))
        
        dropdowns_count = header_details.get('dropdowns_count', 0)
        dropdowns = header_details.get('dropdowns', [])
        working_dropdowns = sum(1 for d in dropdowns if d.get('opens_menu', False))
        
        return f"""
            <div class="section">
                <h2 class="section-title">🎯 Header Validation Details</h2>
                <table class="details-table">
                    <thead>
                        <tr>
                            <th>Element</th>
                            <th>Status</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Logo</strong></td>
                            <td>{logo_badge}</td>
                            <td>Clickable: {'Yes ✓' if header_details.get('logo_clickable') else 'No'}</td>
                        </tr>
                        <tr>
                            <td><strong>Login Button</strong></td>
                            <td>{login_badge}</td>
                            <td>Clickable: {'Yes ✓' if header_details.get('login_button_clickable') else 'No'}</td>
                        </tr>
                        <tr>
                            <td><strong>Language Switcher</strong></td>
                            <td>{lang_badge}</td>
                            <td>Clickable: {'Yes ✓' if header_details.get('language_switcher_clickable') else 'No'}</td>
                        </tr>
                        <tr>
                            <td><strong>Dropdown Menus</strong></td>
                            <td><span class="badge badge-success">{dropdowns_count} Found</span></td>
                            <td>Working: {working_dropdowns}/{dropdowns_count}</td>
                        </tr>
                        <tr>
                            <td><strong>Navigation Items</strong></td>
                            <td><span class="badge badge-success">{header_details.get('nav_items_count', 0)} Found</span></td>
                            <td>-</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        """
    
    def _build_footer_details_html(self, footer_details: Dict) -> str:
        """Build HTML for footer validation details."""
        if not footer_details:
            return ""
        
        newsletter_badge = self._get_badge(footer_details.get('newsletter_exists', False))
        
        return f"""
            <div class="section">
                <h2 class="section-title">📄 Footer Validation Details</h2>
                <table class="details-table">
                    <thead>
                        <tr>
                            <th>Element</th>
                            <th>Count/Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Social Media Links</strong></td>
                            <td><span class="badge badge-success">{footer_details.get('social_links_count', 0)} Found</span></td>
                        </tr>
                        <tr>
                            <td><strong>Footer Links</strong></td>
                            <td><span class="badge badge-success">{footer_details.get('footer_links_count', 0)} Found</span></td>
                        </tr>
                        <tr>
                            <td><strong>Newsletter Signup</strong></td>
                            <td>{newsletter_badge}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        """
    
    def _build_screenshot_html(self, screenshot_path: Optional[str]) -> str:
        """Build HTML for main screenshot."""
        if not screenshot_path:
            return ""
        
        screenshot_html = ""
        
        if self.settings.EMBED_SCREENSHOTS_IN_HTML:
            base64_img = self._image_to_base64(screenshot_path)
            if base64_img:
                screenshot_html = f'<img src="data:image/png;base64,{base64_img}" alt="Page Screenshot">'
        else:
            screenshot_html = f'<p><strong>Screenshot Path:</strong> {screenshot_path}</p>'
        
        return f"""
            <div class="section">
                <h2 class="section-title">📸 Page Screenshot</h2>
                <div class="screenshot-container">
                    {screenshot_html}
                </div>
            </div>
        """
    
    def _build_element_screenshots_html(self, header_details: Dict) -> str:
        """Build HTML for element screenshots."""
        screenshots = header_details.get('screenshots', [])
        
        if not screenshots or not self.settings.EMBED_SCREENSHOTS_IN_HTML:
            return ""
        
        screenshots_html = ""
        
        for screenshot_name in screenshots:
            screenshot_path = self.settings.SCREENSHOT_DIR / f"{screenshot_name}.{self.settings.SCREENSHOT_FORMAT}"
            
            if screenshot_path.exists():
                base64_img = self._image_to_base64(str(screenshot_path))
                if base64_img:
                    title = screenshot_name.replace('_', ' ').title()
                    screenshots_html += f"""
                        <div class="element-screenshot">
                            <h4>{title}</h4>
                            <img src="data:image/png;base64,{base64_img}" alt="{title}">
                        </div>
                    """
        
        if screenshots_html:
            return f"""
                <div class="section">
                    <h2 class="section-title">🖼️ Element Screenshots</h2>
                    <div class="element-screenshots">
                        {screenshots_html}
                    </div>
                </div>
            """
        
        return ""
    
    def _get_badge(self, status: bool) -> str:
        """Get HTML badge based on status."""
        if status:
            return '<span class="badge badge-success">✓ Found</span>'
        else:
            return '<span class="badge badge-error">✗ Not Found</span>'
