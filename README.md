The following tests were executed on a Windows 10 system, running Python 3.7.6. If Python is currently not installed, open a command prompt (cmd) and just enter the command:

    python
This will open a link to the Microsoft store to install the latest Python version.

Once installed, close and re-open your command prompt. Check that pip is installed, by executing the command:

    pip -V
If everything is working as expected, go ahead and install the PyTest and Selenium modules:

    pip install selenium
    pip install pytest
You can run the tests on either Chrome or Firefox. Simply edit conftest.py so that either line 10 (Chrome) or line 11 (Firefox) is un-commented and the other line is commented out. By default, the tests will run in Chrome.

ChromeDriver and GeckoDriver are distributed with this code in the bin folder and do not need to be downloaded, unless you are using different browser versions than the latest. This code was tested with Chrome 80.0.3987.122 and Firefox 73.0.1. If you are using other versions, you should download a suitable version of ChromeDriver from [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) or GeckoDriver from https://github.com/mozilla/geckodriver/releases, extract it and replace the version(s) in the bin folder.

You can now run the tests. With this project checked out, cd to the root folder (e.g C:\code\traderev) and execute the following command:

    python -m pytest tests\test_traderev.py -s
This will execute all 3 tests included in the file. A new browser instance will be opened before each test and closed after it.