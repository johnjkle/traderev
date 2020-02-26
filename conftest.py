import pytest
from selenium import webdriver


# This PyTest fixture is used to start and stop our selected browser
# before and after each test:
@pytest.fixture()
def driver(request):
    # Comment this line out and uncomment the next to run tests in FF:
    driver = webdriver.Chrome(executable_path="bin/chromedriver.exe")
    # driver = webdriver.Firefox(executable_path="bin/geckodriver.exe")
    # Set the window size to avoid responsive design or other discrepancies:
    driver.set_window_size(1366, 768)
    request.node.driver = driver
    yield driver
    driver.quit()
