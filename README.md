# Selenium MU (Mini Utils)

Utility library to facilitate Selenium WebDriver usage.

## Installation
```bash
pip install --upgrade git+https://github.com/rodolfocasan/selenium_mu.git
```

## Usage
```python
from selenium_mu import (
    install_and_get_chrome_driver,
    install_and_get_chromium_driver,
    install_and_get_firefox_driver
)

# Get Chrome driver
chrome_driver_path = install_and_get_chrome_driver()

# Get Chromium driver
chromium_driver_path = install_and_get_chromium_driver()

# Get Firefox driver
firefox_driver_path = install_and_get_firefox_driver()
```

## Features

- Automatic download of drivers compatible with installed browser version
- Support for Windows, Linux and macOS
- Organized storage in `~/.selenium_mu/`
- Automatic system architecture detection
- Progress bar during download

## Requirements

- Python 3.6+
- requests
- tqdm

## License

MIT