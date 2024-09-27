from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service

# Set up the Chrome WebDriver
service = Service('/Users/qi/Downloads/msedgedriver')
driver = webdriver.Edge(service=service)

page_url = "http://discovery.informatics.uab.edu/PAGER/index.php/browse/browse_by_go/GO:0015205"

def download_csv(page_url):
    # Open the webpage
    driver.get(page_url)

    # Find the button by its ID or other attributes
    element = driver.find_element(By.XPATH, "//a[span[text()='Download As']]")
    element.click()

    # sample of the tag <a class="dt-button buttons-csv buttons-html5" tabindex="0" aria-controls="results" href="#"><span>CSV</span></a>
    a_tag = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "//a[span[text()='CSV']]")))
    a_tag.click()
    
    # Close the browser
    driver.quit()

