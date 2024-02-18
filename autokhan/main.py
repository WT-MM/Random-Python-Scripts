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
    # Add any additional logic needed for interaction with the exercise

def clickTextandCheck(letter):
    WebDriverWait(driver, 0.2).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{letter}')]/ancestor::li//button"))).click()
    #answer = driver.find_element(By.XPATH, f"//div[contains(text(), '{letter}')]/ancestor::li//button")
    #answer.click()
    WebDriverWait(driver, 0.2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="exercise-check-answer"]'))).click()
    #check = driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="exercise-check-answer"]')
    #check.click()
    #time.sleep(0.5)
    try:
        WebDriverWait(driver, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-test-id="exercise-next-question"]'))).click()
        #nextQuestion = driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="exercise-next-question"]')
        #nextQuestion.click()
        return True
    except:
        return False
    
def clickLetsGo():
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Let’s go']]"))).click()
    #LetsGo = driver.find_element(By.XPATH, "//button[.//span[text()='Let’s go']]")
    #LetsGo.click()


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
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Try again')]]"))).click()
            #try_again_button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Try again')]]")
            #try_again_button.click()
            #time.sleep(1)
            clickLetsGo()
            #time.sleep(1)
        except:
            continue
        


# URL of the specific exercise or page you want to access
specific_exercise_url = "https://www.khanacademy.org/humanities/grammar/punctuation-the-colon-semicolon-and-more/introduction-to-semicolons/e/introduction-to-semicolons"

# Perform login
#login_khan_academy(EMAIL, PASSWORD)

#Await user login
driver.get("https://www.khanacademy.org/login")
input("Please login to Khan Academy and press Enter to continue...")
# Navigate to the specific exercise

#driver.implicitly_wait(10)
navigate_to_exercise(specific_exercise_url)
#time.sleep(5)
run_exercise()

# Add any additional code for interaction or waiting here

# Optionally, close the browser when done
# driver.quit()
