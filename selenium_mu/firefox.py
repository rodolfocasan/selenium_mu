# selenium_mu/firefox.py
import os
import zipfile
import tarfile
import requests

from .utils import (
    get_os_name,
    get_architecture,
    get_selenium_mu_directory,
    get_firefox_version,
    get_geckodriver_version,
    download_file_with_progress,
    set_execution_permissions
)





'''
>>> Instalacion de GeckoDriver (Firefox)
'''
def install_and_get_firefox_driver():
    print("\n[ Firefox Driver Download ]")
    try:
        system = get_os_name()
        architecture = get_architecture()
        
        if not architecture:
            raise Exception("Unsupported architecture")
        
        print(f" - Detected system: {system.upper()}")
        print(f" - Detected architecture: {architecture}")
        
        selenium_mu_dir = get_selenium_mu_directory()
        firefox_dir = os.path.join(selenium_mu_dir, 'Firefox')
        if not os.path.exists(firefox_dir):
            os.makedirs(firefox_dir)
        
        if system == 'windows':
            driver_name = 'geckodriver.exe'
        else:
            driver_name = 'geckodriver'
        
        geckodriver_path = os.path.join(firefox_dir, driver_name)
        
        firefox_version = get_firefox_version()
        print(f" - Detected Firefox version: {firefox_version}")
        
        if os.path.exists(geckodriver_path):
            driver_version = get_geckodriver_version(geckodriver_path)
            if driver_version:
                print(f" - Geckodriver already installed (version {driver_version}).")
                return geckodriver_path
        
        print(" - Getting latest geckodriver version...")
        api_url = "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
        response = requests.get(api_url)
        response.raise_for_status()
        release_data = response.json()
        
        latest_version = release_data['tag_name'].lstrip('v')
        print(f" - Latest available version: {latest_version}")
        
        if system == 'windows':
            if architecture == 'win64':
                asset_name = f'geckodriver-v{latest_version}-win64.zip'
            else:
                asset_name = f'geckodriver-v{latest_version}-win32.zip'
        elif system == 'darwin':
            if architecture == 'mac-arm64':
                asset_name = f'geckodriver-v{latest_version}-macos-aarch64.tar.gz'
            else:
                asset_name = f'geckodriver-v{latest_version}-macos.tar.gz'
        elif system == 'linux':
            if architecture == 'linux-aarch64':
                asset_name = f'geckodriver-v{latest_version}-linux-aarch64.tar.gz'
            else:
                asset_name = f'geckodriver-v{latest_version}-linux64.tar.gz'
        else:
            raise Exception("Unsupported operating system")
        
        download_url = None
        for asset in release_data['assets']:
            if asset['name'] == asset_name:
                download_url = asset['browser_download_url']
                break
        
        if not download_url:
            raise Exception(f"Geckodriver not found for {asset_name}")
        
        if system == 'windows':
            download_file = os.path.join(firefox_dir, 'geckodriver.zip')
        else:
            download_file = os.path.join(firefox_dir, 'geckodriver.tar.gz')
        
        download_file_with_progress(download_url, download_file)
        
        print(" - Extracting files...")
        if system == 'windows':
            with zipfile.ZipFile(download_file, 'r') as zip_ref:
                zip_ref.extractall(firefox_dir)
        else:
            with tarfile.open(download_file, 'r:gz') as tar_ref:
                tar_ref.extractall(firefox_dir)
        
        os.remove(download_file)
        set_execution_permissions(geckodriver_path)
        
        print(f"Geckodriver successfully installed at: {geckodriver_path}")
        return geckodriver_path
    except Exception as e:
        print(f" [!!] Error during geckodriver installation: {str(e)}")
        return None