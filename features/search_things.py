'''
import pyautogui
import time
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

      
class search_things:
    @staticmethod
    def process_command(c):
        if c.lower().startswith("search"):
            query = c[7:].strip()  # remove the word "search"
            
            #opens google to sear
            if "on google" in query.lower():
                queryg = query.lower().replace("on google", "").strip()
                site = "https://www.google.com"
                search_box_name = "q"  # Google's search box name

            elif "on youtube" in query.lower():
                queryg = query.lower().replace("on youtube", "").strip()
                site = "https://www.youtube.com"
                search_box_name = "search_query"  # YouTube's search box name
            
            if "on" in query.lower():
                parts = query.lower().split("on", 1)  # Split into two parts: before 'on' and after 'on'
                queryg = parts[0].strip()  # This is what we search
                site_name = parts[1].strip()  # This is the site name after 'on'
                
                # Build the URL dynamically
                site = f"https://www.{site_name}.com"
                
                # Default search box name (may vary by site)
                search_box_name = "q"  
    
            else:
                print(query)
                return


             # Start Selenium browser
            driver = webdriver.Chrome()  # Make sure ChromeDriver is installed
            driver.get(site)

             # Wait for page to load
            time.sleep(2)

            # Find search box and type query
            search_box = driver.find_element(By.NAME, search_box_name)
            search_box.send_keys(queryg)
            search_box.send_keys(Keys.RETURN) #press enter
'''
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def human_typing(element, text):
    """Type characters with wider random delays (100ms to 600ms)"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.6))

def human_scroll(driver, down_scrolls=3, up_scrolls=2):
    """Scroll down and then up with random delays"""
    for _ in range(down_scrolls):
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
        time.sleep(random.uniform(1.5, 4))
    for _ in range(up_scrolls):
        driver.execute_script("window.scrollBy(0, -window.innerHeight / 2);")
        time.sleep(random.uniform(1.5, 4))

class SearchThings:
    @staticmethod
    def process_command(c):
        if not c.lower().startswith("search"):
            return

        query = c[7:].strip()
        # Default to DuckDuckGo if no site specified
        if " on " in query.lower():
            parts = query.lower().split(" on ", 1)
            queryg = parts[0].strip()
            site_name = parts[1].strip()
        else:
            queryg = query
            site_name = "google"

        search_boxes = {
            "duckduckgo": "q",
            "youtube": "search_query",
            "google": "q",
            "bing": "q",
            "amazon": "field-keywords",
            "linkedin": "q"
        }

        site_url = f"https://www.{site_name}.com"
        search_box_name = search_boxes.get(site_name)

        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        driver.get(site_url)

        time.sleep(random.uniform(2, 5))  # Wait for page to load with wider delay

        try:
            if search_box_name:
                search_box = driver.find_element(By.NAME, search_box_name)
                human_typing(search_box, queryg)
                search_box.send_keys(Keys.RETURN)

                time.sleep(random.uniform(3, 8))  # Wait for results with wider delay

                if site_name == "youtube":
                    human_scroll(driver, scrolls=2)
                    videos = driver.find_elements(By.ID, "video-title")
                    if videos:
                        time.sleep(random.uniform(1, 4))
                        videos[0].click()
                    else:
                        print("No videos found to play.")
                else:
                    human_scroll(driver, scrolls=3)
            else:
                print(f"No search box mapping for {site_name}, opened site only.")
        except Exception as e:
            print(f"Error during search or interaction: {e}")
