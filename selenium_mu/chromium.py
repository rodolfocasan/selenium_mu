# selenium_mu/chromium.py
import os
import shutil
import zipfile
import requests

from .utils import (
    get_os_name,
    get_architecture,
    get_selenium_mu_directory,
    get_chromium_version,
    get_chromedriver_version,
    download_file_with_progress,
    set_execution_permissions
)





'''
>>> Instalacion de ChromiumDriver
'''
def install_and_get_chromium_driver():
    print("\n[ Chromium Driver Download ]")
    try:
        system = get_os_name()
        architecture = get_architecture()
        
        if not architecture:
            raise Exception("Unsupported architecture")
        
        print(f" - Detected system: {system.upper()}")
        print(f" - Detected architecture: {architecture}")
        
        selenium_mu_dir = get_selenium_mu_directory()
        chromium_dir = os.path.join(selenium_mu_dir, 'Chromium')
        if not os.path.exists(chromium_dir):
            os.makedirs(chromium_dir)
        
        if system == 'windows':
            driver_name = 'chromedriver.exe'
        else:
            driver_name = 'chromedriver'
        
        chromedriver_path = os.path.join(chromium_dir, driver_name)
        
        chromium_version = get_chromium_version()
        print(f" - Detected Chromium version: {chromium_version}")
        
        if os.path.exists(chromedriver_path):
            driver_version = get_chromedriver_version(chromedriver_path)
            if driver_version:
                if driver_version == chromium_version:
                    print(f" - Installed chromedriver (version {driver_version}) matches Chromium. No update needed.")
                    return chromedriver_path
                else:
                    print(f"( Version mismatch detected )")
                    print(f" - Chromium version     : {chromium_version}")
                    print(f" - Chromedriver version : {driver_version}")
                    print(" [!!] Removing old version to download the correct one...")
                    os.remove(chromedriver_path)
        
        if architecture == 'win32':
            arch_suffix = 'win32'
        elif architecture == 'win64':
            arch_suffix = 'win64'
        elif architecture == 'mac-arm64':
            arch_suffix = 'mac-arm64'
        elif architecture == 'mac-x64':
            arch_suffix = 'mac-x64'
        elif architecture == 'linux-aarch64':
            arch_suffix = 'linux64'
        else:
            arch_suffix = 'linux64'
        
        url_chromedriver = f"https://storage.googleapis.com/chrome-for-testing-public/{chromium_version}/{arch_suffix}/chromedriver-{arch_suffix}.zip"
        
        response = requests.head(url_chromedriver)
        if response.status_code == 404:
            raise Exception(f"Chromedriver not found for version {chromium_version}. This exact version may not be available in the repository.")
        
        zip_path = os.path.join(chromium_dir, 'chromedriver.zip')
        
        download_file_with_progress(url_chromedriver, zip_path)
        
        print(" - Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(chromium_dir)
        
        extracted_folder = os.path.join(chromium_dir, f'chromedriver-{arch_suffix}')
        extracted_driver = os.path.join(extracted_folder, driver_name)
        
        if os.path.exists(extracted_driver):
            shutil.move(extracted_driver, chromedriver_path)
            shutil.rmtree(extracted_folder)
        
        os.remove(zip_path)
        set_execution_permissions(chromedriver_path)
        
        print(f"Chromedriver (Chromium) successfully installed at: {chromedriver_path}")
        return chromedriver_path
    except Exception as e:
        print(f" [!!] Error during chromedriver (Chromium) installation: {str(e)}")
        return None