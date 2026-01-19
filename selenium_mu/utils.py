# selenium_mu/utils.py
import os
import re
import requests
import platform
import subprocess
from tqdm import tqdm
from pathlib import Path





'''
>>> Funciones de entorno
'''
def get_os_name():
    return str(platform.system()).lower()


def get_home_directory():
    return str(Path.home())


def get_selenium_mu_directory():
    home = get_home_directory()
    selenium_mu_dir = os.path.join(home, '.selenium_mu')
    if not os.path.exists(selenium_mu_dir):
        os.makedirs(selenium_mu_dir)
    return selenium_mu_dir


def get_architecture():
    machine = platform.machine().lower()
    system = get_os_name()
    
    if system == 'windows':
        if 'amd64' in machine or 'x86_64' in machine:
            return 'win64'
        else:
            return 'win32'
    elif system == 'darwin':
        if 'arm' in machine or 'aarch64' in machine:
            return 'mac-arm64'
        else:
            return 'mac-x64'
    elif system == 'linux':
        if 'aarch64' in machine or 'arm64' in machine:
            return 'linux-aarch64'
        else:
            return 'linux64'
    else:
        return None





'''
>>> Funciones de descarga
'''
def download_file_with_progress(url, destination):
    print(f" - Downloading from: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    progress_bar = tqdm(
        total = total_size,
        unit = 'iB',
        unit_scale = True,
        desc = 'Download progress'
    )
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                size = f.write(chunk)
                progress_bar.update(size)
    progress_bar.close()


def set_execution_permissions(file_path):
    system = get_os_name()
    if system != 'windows':
        try:
            os.chmod(file_path, 0o755)
            return True
        except Exception as e:
            print(f" [!!] Could not set execution permissions automatically.")
            print(f" [!!] Run manually: chmod +x {file_path}")
            return False
    return True





'''
>>> Funciones de version para Chrome/Chromium
'''
def get_chrome_version():
    system = get_os_name()
    try:
        if system == 'windows':
            import winreg
            key_path = r'SOFTWARE\Google\Chrome\BLBeacon'
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
            version, _ = winreg.QueryValueEx(key, 'version')
            winreg.CloseKey(key)
            return version
        elif system == 'darwin':
            chrome_version = subprocess.check_output(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'])
            return chrome_version.decode('utf-8').strip().split()[-1]
        elif system == 'linux':
            try:
                chrome_version = subprocess.check_output(['google-chrome', '--version'])
            except:
                chrome_version = subprocess.check_output(['google-chrome-stable', '--version'])
            return chrome_version.decode('utf-8').strip().split()[-1]
        else:
            raise Exception("Unsupported operating system")
    except Exception as e:
        raise Exception(f"Could not detect Google Chrome version. Make sure it is installed. Error: {str(e)}")


def get_chromium_version():
    system = get_os_name()
    try:
        if system == 'windows':
            chromium_path = r'C:\Program Files\Chromium\Application\chrome.exe'
            if not os.path.exists(chromium_path):
                chromium_path = r'C:\Program Files (x86)\Chromium\Application\chrome.exe'
            chromium_version = subprocess.check_output([chromium_path, '--version'])
            return chromium_version.decode('utf-8').strip().split()[-1]
        elif system == 'darwin':
            chromium_version = subprocess.check_output(['/Applications/Chromium.app/Contents/MacOS/Chromium', '--version'])
            return chromium_version.decode('utf-8').strip().split()[-1]
        elif system == 'linux':
            chromium_version = subprocess.check_output(['chromium', '--version'])
            return chromium_version.decode('utf-8').strip().split()[-1]
        else:
            raise Exception("Unsupported operating system")
    except Exception as e:
        raise Exception(f"Could not detect Chromium version. Make sure it is installed. Error: {str(e)}")


def get_chromedriver_version(chromedriver_path):
    try:
        result = subprocess.check_output([chromedriver_path, '--version'])
        version = result.decode('utf-8').split()[1]
        return version
    except (subprocess.CalledProcessError, IndexError, FileNotFoundError):
        return None





'''
>>> Funciones de version para Firefox
'''
def get_firefox_version():
    system = get_os_name()
    try:
        if system == 'windows':
            firefox_path = r'C:\Program Files\Mozilla Firefox\firefox.exe'
            if not os.path.exists(firefox_path):
                firefox_path = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'
            firefox_version = subprocess.check_output([firefox_path, '--version'])
        elif system == 'darwin':
            firefox_version = subprocess.check_output(['/Applications/Firefox.app/Contents/MacOS/firefox', '--version'])
        elif system == 'linux':
            firefox_version = subprocess.check_output(['firefox', '--version'])
        else:
            raise Exception("Unsupported operating system")
        
        full_version = firefox_version.decode('utf-8').strip()
        match = re.search(r'(\d+\.\d+)', full_version)
        if match:
            return match.group(1)
        else:
            raise Exception("Could not extract Firefox version")
    except Exception as e:
        raise Exception(f"Could not detect Firefox version. Make sure it is installed. Error: {str(e)}")


def get_geckodriver_version(geckodriver_path):
    try:
        result = subprocess.check_output([geckodriver_path, '--version'])
        version_text = result.decode('utf-8')
        match = re.search(r'geckodriver\s+(\d+\.\d+\.\d+)', version_text)
        if match:
            return match.group(1)
        return None
    except (subprocess.CalledProcessError, IndexError, FileNotFoundError):
        return None