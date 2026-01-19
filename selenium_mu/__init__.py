# selenium_mu/__init__.py
from .chrome import install_and_get_chrome_driver
from .chromium import install_and_get_chromium_driver
from .firefox import install_and_get_firefox_driver

from .utils import (
    get_os_name,
    get_home_directory,
    get_selenium_mu_directory,
    get_architecture
)





__version__ = '1.0.0'
__all__ = [
    'install_and_get_chrome_driver',
    'install_and_get_chromium_driver',
    'install_and_get_firefox_driver',
    
    'get_os_name',
    'get_home_directory',
    'get_selenium_mu_directory',
    'get_architecture'
]