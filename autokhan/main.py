from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver
options = Options()

# Add the excludeSwitches option
options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Add additional arguments as needed
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Function to navigate to a specific exercise or page
def navigate_to_exercise(url):
    driver.get(url)

def clickTextandCheck(letter):
    try:
        WebDriverWait(driver, 0.2).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{letter}')]/ancestor::li//button"))).click()
        WebDriverWait(driver, 0.2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="exercise-check-answer"]'))).click()
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="exercise-next-question"]'))).click()
        return True
    except:
        return False
    
def clickLetsGo():
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Let’s go']]"))).click()


def run_exercise():
    try:
        clickLetsGo()
    except:
        pass
    #time.sleep(2)
    while True:
        for letter in ["A", "B"]:
            if(clickTextandCheck(letter)):
                break
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Try again')]]"))).click()
            clickLetsGo()
        except:
            continue


specific_exercise_url = "https://www.khanacademy.org/humanities/grammar/punctuation-the-colon-semicolon-and-more/introduction-to-semicolons/e/introduction-to-semicolons"
#specific_exercise_url = "https://www.khanacademy.org/humanities/grammar/punctuation-the-colon-semicolon-and-more/introduction-to-semicolons/e/using-semicolons-and-commas"


#Await user login
driver.get("https://www.khanacademy.org/login")
input("Please login to Khan Academy and press Enter to continue...")
#driver.implicitly_wait(10)
navigate_to_exercise(specific_exercise_url)
run_exercise()
