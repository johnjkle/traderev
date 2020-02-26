import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# The dropdown select lists on "https://jobs.lever.co/traderev" aren't actually select elements and
# as a result, we cannot use Selenium's Select functionality. Since we will be interacting with these
# elements throughout the tests, a small function was added here to simplify this interaction, which
# makes the tests shorter and easier to use:
def filter_by(type, option, driver):
        # Find and click the appropriate filter type (Location/Team/Work Type):
        filter = driver.find_element(By.CSS_SELECTOR, "[aria-label*='Filter by {}']".format(type))
        filter.click()
        # Wait for the appropriate options "popup" to be visible:
        WebDriverWait(driver, 10).until(
            lambda condition: filter.find_element(By.CLASS_NAME, "filter-popup").is_displayed()
        )
        # Parse through the list of options in the "popup", click the one that matches the option argument
        # passed into this function and break out of the loop:
        for element in driver.find_elements(By.CSS_SELECTOR, "[aria-label*='Filter by {}'] a".format(type)):
            if element.text == option:
                element.click()
                break

# Use a PyTest fixture from conftest.py to start and stop the browser before each test. The fixture can
# easily be modify to start and stop the browser only once, before and after all tests if that behaviour
# was desired instead:
@pytest.mark.usefixtures('driver')
class TestTradeRev:
    def test_careers_page_displayed_properly(self, driver):
        # Navigate to "https://www.traderev.com/en-ca/":
        driver.get("https://www.traderev.com/en-ca/")
        # Find and click the "Careers" link:
        careers = driver.find_element(By.CSS_SELECTOR, "[href='https://work.traderev.com/']")
        careers.click()
        # The "Careers" link opens a new tab, so wait until we have 2 tabs present and switch to
        # the 2nd one:
        WebDriverWait(driver, 10).until(lambda condition: len(driver.window_handles) == 2)
        driver.switch_to.window(driver.window_handles[1])
        # Firefox does not deal with the tab switch as gracefully as Chrome, so lets also wait for
        # a suitable element to be present, in this case, the page header:
        WebDriverWait(driver, 5).until(lambda condition: driver.find_element(By.ID, "masthead"))
        # We could check if the page is diplayed properly by checking something like document.readyState 
        # but that would not guarantee elements have loaded, etc. So we can check for any number of 
        # suitable elements to be present and visible on the page. In this case, we are checking for
        # a header, a main banner and a footer - are actually present and visible:
        header = driver.find_element(By.ID, "masthead")
        widget = driver.find_element(By.ID, "main")
        footer = driver.find_element(By.CLASS_NAME, "site-footer")

        assert header.is_displayed()
        assert widget.is_displayed()
        assert footer.is_displayed()
        # Find and click the "Canadian Opportunities" button:
        canadian_opportunities = driver.find_element(By.CSS_SELECTOR, "a[title='Canadian Jobs']")
        canadian_opportunities.click()
        # The "Canadian Opportunities" button also opens a new tab, so now we can wait until we have 3 tabs open
        # and then switch to the 3rd one:
        WebDriverWait(driver, 10).until(lambda condition: len(driver.window_handles) == 3)
        driver.switch_to.window(driver.window_handles[2])  
        # Just as in the first tab switch, Firefox does not deal with the switch as well as Chrome, so again we wait for
        # the appropriate header to be present:  
        WebDriverWait(driver, 5).until(
            lambda condition: driver.find_element(By.CSS_SELECTOR, "div[class='main-header page-full-width section-wrapper']")
        )
        # And we check this page is displayed properly by by checking that the header, footer and at least one job posting
        # are actually present and visible:
        header = driver.find_element(By.CSS_SELECTOR, "div[class='main-header page-full-width section-wrapper']")
        job_postings = driver.find_elements(By.CLASS_NAME, "posting")
        footer = driver.find_element(By.CSS_SELECTOR, "div[class='main-footer page-full-width']")

        assert header.is_displayed()
        assert len(job_postings) >= 1
        assert footer.is_displayed()

    def test_location_filter(self, driver):
        # Navigate to "https://jobs.lever.co/traderev":
        driver.get("https://jobs.lever.co/traderev")
        # Call our "filter_by" function to filter location by "Toronto, Ontario, Canada":
        filter_by("Location", "Toronto, Ontario, Canada", driver)
        # Parse through the list of job postings and assert the location for each one is indeed "Toronto, Ontario, Canada":
        for element in driver.find_elements(By.CLASS_NAME, "posting"):
            assert element.find_element(By.CSS_SELECTOR, "span[class*=sort-by-location]").text.title() == "Toronto, Ontario, Canada"

    def test_location_and_team_filters(self, driver):
        # Navigate to "https://jobs.lever.co/traderev":
        driver.get("https://jobs.lever.co/traderev")
        # Call our "filter_by" function to filter location by "Toronto, Ontario, Canada":
        filter_by("Location", "Toronto, Ontario, Canada", driver)
        # Call our "filter_by" function again - to filter team by "Engineering":
        filter_by("Team", "Engineering", driver)
        # Parse through the list of job postings and assert both location is equal to "Toronto, Ontario, Canada" and all team
        # descriptions begin with "Engineering":
        for element in driver.find_elements(By.CLASS_NAME, "posting"):
            assert element.find_element(By.CSS_SELECTOR, "span[class*=sort-by-location]").text.title() == "Toronto, Ontario, Canada"
            assert element.find_element(By.CSS_SELECTOR, "span[class*=sort-by-team]").text.title().startswith("Engineering")
        # Check how many job postings are displayed and output to the console - this code does not currently cater for a scenario 
        # where 0 job postings are available but could easily be modified to do so:
        if (len(driver.find_elements(By.CLASS_NAME, "posting"))) == 1:
            print("There is 1 job posting available at this time.")
        elif (len(driver.find_elements(By.CLASS_NAME, "posting"))) > 1:
            print("There are {} job postings available at this time.".format((len(driver.find_elements(By.CLASS_NAME, "posting")))))
