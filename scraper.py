from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

def scrape_twitter():
    # Set up Chrome options for Incognito mode, ProxyMesh, and other settings
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Maximize the window
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--incognito")  # Launch in incognito mode to avoid session issues

    # Set ProxyMesh proxy configuration
    proxy = "http://richyboy:qwER12@#@proxy.proxymesh.com:31280"  # Replace with your ProxyMesh credentials
    chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # Path to chromedriver (make sure it's correct)
    service = Service()  # Change path if necessary
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the Twitter login page
        driver.get("https://x.com/login")
        print("Opened Twitter login page. Please log in manually within 60 seconds.")
        
        # Wait for the user to log in manually
        time.sleep(60)  # Wait for manual login
        
        # Confirm login by checking if the URL has changed to Twitter's home page
        if "home" not in driver.current_url:
            raise Exception("Login not detected. Please ensure you're logged in.")

        print("Login detected. Fetching trending topics...")

        # Locate the "What’s Happening" section
        whats_happening_xpath = '//section[contains(., "What’s happening")]'
        try:
            whats_happening_section = driver.find_element(By.XPATH, whats_happening_xpath)
        except Exception as e:
            print(f"Error locating 'What’s Happening' section: {e}")
            driver.quit()
            return
        
        # Extract top 5 trends
        try:
            trending_topics = whats_happening_section.find_elements(By.XPATH, './/div[@dir="ltr"]')[:5]
            if not trending_topics:
                raise Exception("Could not find trending topics.")
            return [topic.text for topic in trending_topics]
        except Exception as e:
            print(f"Error extracting trending topics: {e}")
            driver.quit()
            return
        
    finally:
        driver.quit()

# To trigger the scraper function
if __name__ == "__main__":
    trends = scrape_twitter()
    if trends:
        print("Top 5 Twitter Trends:")
        for trend in trends:
            print(f"- {trend}")
    else:
        print("Failed to fetch trends.")
