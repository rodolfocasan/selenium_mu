# setup.py
from setuptools import setup, find_packages





with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'selenium_mu',
    version = '1.0.0',
    author = 'Rodolfo Casan',
    author_email = 'contact.christcastr@gmail.com',
    description = 'Selenium Mini Utils - Utilities to facilitate Selenium usage',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/rodolfocasan/selenium_mu',
    packages = find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
    python_requires = '>=3.6',
    install_requires = [
        'requests>=2.32.5',
        'tqdm>=4.67.1',
    ],
    keywords = 'selenium webdriver automation testing chrome firefox chromium',
    project_urls = {
        'Bug Reports': 'https://github.com/rodolfocasan/selenium_mu/issues',
        'Source': 'https://github.com/rodolfocasan/selenium_mu',
    },
)