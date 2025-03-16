import time
import csv
import os
import dotenv
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  



def setup_driver():
    """Set up and return the WebDriver instance."""
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def navigate_to_mobiles(driver, base_url):
    """Navigate to the Mobile Phones section on OLX."""
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
    time.sleep(20)  # Consider replacing this with explicit waits
    mobiles = driver.find_element(By.XPATH, "//div[.//span[contains(text(),'Mobile Phones')]]/a")
    mobiles.click()
    print("Mobiles Clicked")

def select_location(driver, province, city):
    """Select the location (province and city) on OLX."""
    wait = WebDriverWait(driver, 10)
    time.sleep(10)  # Consider replacing this with explicit waits
    province_element = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[.//span[text()='Punjab']]")))
    province_element.click()
    print("Punjab Clicked")
    driver.refresh()
    time.sleep(10)  # Consider replacing this with explicit waits
    city_element = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[.//span[text()='Lahore']]")))
    city_element.click()
    print("Lahore clicked")

def set_price_range(driver, min_price_value, max_price_value):
    """Set the price range filter on OLX."""
    wait = WebDriverWait(driver, 10)
    time.sleep(10)  # Consider replacing this with explicit waits

    # Set minimum price
    min_price = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Min']")))
    min_price.click()
    min_price.send_keys(Keys.CONTROL + "a")
    min_price.send_keys(Keys.DELETE)
    min_price.send_keys(min_price_value)
    min_price.send_keys(Keys.ENTER)
    print("min_price entered")

    # Set maximum price
    max_price = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Max']")))
    max_price.click()
    max_price.send_keys(Keys.CONTROL + "a")
    max_price.send_keys(Keys.DELETE)
    max_price.send_keys(max_price_value)
    max_price.send_keys(Keys.ENTER)
    print("max_price entered")

def scroll_and_click_load_more(driver):
    """
    Scroll down the page, click the 'Load more' button if found, and repeat the process.
    Stop after two successful scrolls or when the 'Load more' button is no longer found.
    """
    wait = WebDriverWait(driver, 10)
    scroll_count = 0
    max_scrolls = 2  # Limit the number of scrolls to 2

    while scroll_count < max_scrolls:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to load new content

        print(f"Scroll {scroll_count}: Scrolled to the bottom of the page.")

        try:
            load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Load more']]")))
            print("Found 'Load more' button. Attempting to click...")
            load_more_button.click()
            time.sleep(2)  
            print("Clicked 'Load more' button.")

            
            scroll_count += 1  
        except TimeoutException:
            
            print(f"Scroll {scroll_count}: 'Load more' button not found, continuing to scroll...")

    print("Reached maximum scroll limit (2 scrolls). 'Load more' button not found.")

def link_extracter(driver, url):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='_1aad128c ec65250d']")))
    
    links = driver.find_elements(By.XPATH, "//ul[@class='_1aad128c ec65250d']/li")
    
    print("Counting links...")
    count = len(links)
    print(f"Total links found: {count}")
    extracted_links = []
    for index, li in enumerate(links, start=1):
        try:
            # Find the <a> tag inside the <li> > <article> > <div> and get its href attribute
            href = li.find_element(By.XPATH, ".//article/div/a").get_attribute("href")
            if href:  # Only add non-empty hrefs
                extracted_links.append(href)
                print(f"Link {index}: {href}")
        except Exception as e:
            print(f"Link {index}: No <a> tag found in this <li>. Error: {e}")
    
    db_name = "olx_db"
    conn = connect_to_db(db_name)
    insert_links(conn, extracted_links)
            
    to_csv(extracted_links,url)
    return extracted_links
    
def to_csv(links,url, filename = "extracted_links.csv"):
    with open(filename, mode='w', newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Links"])
        for i in links:
              writer.writerow([i])
        print("Saved in CSV")
        
def link_open(driver,input_csv ="extracted_links.csv", output_csv="scrapped_data.csv"):
    with open(input_csv, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
         
        with open(output_csv, mode="w", newline="",encoding="utf-8") as outfile:
            fieldnames = ["Links","Name","Price","Location","Date","Description"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            db_name = "olx_db"
            conn = connect_to_db(db_name)   
            for row in rows:
                link = row["Links"]
                print(f"Processing link: {link}")
                data = data_scrap(driver,link)
                    
                writer.writerow({
                    "Links": link,
                    "Name": data["Name"],
                    "Price": data["Price"],
                    "Location": data["Location"],
                    "Date": data["Date"],
                    "Description": data["Description"]
                })
                print(f"Scraped data: Name={data['Name']}, Price={data['Price']},Location={data['Location']}, Date={data['Date']},Description={data['Description']}")
                insert_mobile_data(
                    conn,
                    data["Name"],
                    data["Price"],
                    data["Location"],
                    data["Date"],
                    data["Description"],
                    link
                )
def data_scrap(driver, links):
    driver.get(links)
    wait= WebDriverWait(driver,1000)
    try:
        name = driver.find_element(By.XPATH,"//h1[@class='_75bce902']").text
        print (name)
    except Exception:
        name = "N/A"
    try:
        price = driver.find_element(By.XPATH,"//span[@class='_24469da7']").text
        print(price)
    except Exception:
        price = "N/A"
    try:
        location = driver.find_element(By.XPATH,"//div[@class='_1ee53078']").text
        print(location)
    except Exception:
        location = "N/A"
    try:    
        date = driver.find_element(By.XPATH,"//span[@aria-label='Creation date']").text
        print(date)
    except Exception:
        date="N/A"
    try:
        description = driver.find_element(By.XPATH,"//div[@class='_472bfbef']").text
        print(description)
    except Exception:
        description = "N/A"
    link = links
    return {
        "Links": link,
        "Name": name,
        "Price": price,
        "Location": location,
        "Date": date,
        "Description": description
    }

def insert_links(conn, links):
    cursor = conn.cursor()
    for link in links:
        try:
            # Insert each link into the Links table if it doesn't already exist
            cursor.execute("INSERT OR IGNORE INTO Link (link_url) VALUES (?)", (link,))
        except Exception as e:
            print(f"Error inserting link {link}: {e}")
    conn.commit()

def insert_mobile_data(conn, name, price, location, date, description, link):
    cursor = conn.cursor()
    try:
        # Clean the price to remove non-numeric characters
        cleaned_price = int("".join(filter(str.isdigit, price))) if price != "N/A" else None
        
        # Insert the data into the Mobiles table
        cursor.execute("""
            INSERT INTO Mobiles (name, price, location, date, description, links)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, cleaned_price, location, date, description, link))
        print(f"Inserted data for {name} into the Mobiles table.")
    except Exception as e:
        print(f"Error inserting data for {name}: {e}")
    conn.commit()


def main():
    dotenv.load_dotenv()
    base_url = "https://www.olx.com.pk/"
    province = os.getenv("province", "Punjab")
    city = os.getenv("city", "Lahore")
    min_price_value = os.getenv("min_price_value", "10000")
    max_price_value = os.getenv("max_price_value", "50000")
    input_csv = os.getenv("input_csv", "extracted_links.csv")
    output_csv = os.getenv("output_csv", "scrapped_data.csv")
    # Setup WebDriver
    driver = setup_driver()

    try:
        # Navigate to Mobile Phones section
        navigate_to_mobiles(driver, base_url)

        # Select location (Punjab -> Lahore)
        select_location(driver, province, city)

        # Set price range
        set_price_range(driver, min_price_value, max_price_value)

        scroll_and_click_load_more(driver)
        
        link_extracter(driver, base_url)
        
        link_open(driver, input_csv, output_csv)
        # Keep browser open until user presses Enter
        input("Press Enter to close the browser...")
    finally:
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    
    main()