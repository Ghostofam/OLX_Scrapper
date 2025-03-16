# OLX Mobile Phone Scraper

A Python-based web scraper designed to extract mobile phone listings from OLX Pakistan, with customizable filters for location and price range. The scraper stores data in both CSV files and a SQLite database for easy access and analysis.

## Project Overview

This project automates the process of collecting mobile phone listings data from OLX Pakistan. It navigates to the mobile phones section, applies location and price filters, and extracts detailed information about each listing including:

- Product name
- Price
- Location
- Posting date
- Product description
- Original listing URL

The scraper uses Selenium WebDriver to interact with the OLX website, simulating user actions like clicking, scrolling, and form input. Data is saved in both CSV format and a SQLite database for easy analysis and processing.

## File and Directory Structure

```
OLX_Bot/
├── .env                    # Environment variables and configuration
├── .gitignore              # Git ignore file
├── scrapper.py             # Main scraper script
├── olx_db                  # SQLite database file (created during execution)
├── extracted_links.csv     # Intermediate file storing listing URLs
├── scrapped_data_1.csv     # Final output file with scraped data
├── chrome_temp/            # Temporary Chrome browser data
└── .venv/                  # Python virtual environment
```

## Database Schema

The scraper uses a SQLite database with the following tables:

1. **Link** - Stores unique listing URLs
   - `link_id` (Primary Key)
   - `link_url` (Unique URL of the listing)

2. **Mobiles** - Stores detailed information about each mobile phone listing
   - `mobile_id` (Primary Key)
   - `name` (Product name)
   - `price` (Price in numeric format)
   - `location` (Location of the seller)
   - `date` (Posting date)
   - `description` (Product description)
   - `links` (URL to the original listing)

## Dependencies

The project relies on the following Python packages:
- Selenium: For browser automation and web scraping
- webdriver_manager: For automatic ChromeDriver management
- python-dotenv: For environment variable management
- sqlite3: For database operations
- Standard libraries: time, csv, os

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- Chrome browser installed
- Internet connection

### Step 1: Clone the repository
```bash
git clone <repository-url>
cd OLX_Bot
```

### Step 2: Set up a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install selenium webdriver-manager python-dotenv
```

### Step 4: Configure environment variables
Create or modify the `.env` file with your desired parameters:
```
min_price_value = "10000"
max_price_value = "50000"
city = "Lahore"
province = "Punjab"
input_csv = "extracted_links.csv"
output_csv = "scrapped_data.csv"
```

### Step 5: Database Setup
The database is automatically created and initialized when you run the script. However, you need to ensure that the database tables are properly created before running the script for the first time. The script assumes the following tables exist:

```sql
CREATE TABLE IF NOT EXISTS Link (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    link_url TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Mobiles (
    mobile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    location TEXT,
    date TEXT,
    description TEXT,
    links TEXT
);
```

## Usage

### Running the Scraper
Execute the main script to start the scraping process:
```bash
python scrapper.py
```

The script will:
1. Open a Chrome browser window
2. Navigate to OLX Pakistan
3. Go to the Mobile Phones section
4. Apply location filters (Punjab > Lahore by default)
5. Set price range filters (10,000 - 50,000 PKR by default)
6. Scroll and load more listings (limited to 2 scrolls in the current implementation)
7. Extract listing URLs to `extracted_links.csv` and the database
8. Visit each listing URL and extract detailed information
9. Save all scraped data to `scrapped_data.csv` and the database
10. Wait for user input before closing the browser

### Customizing the Scraper
You can customize the scraper's behavior by modifying the `.env` file:
- `min_price_value`: Minimum price filter
- `max_price_value`: Maximum price filter
- `province`: Province filter (e.g., "Punjab")
- `city`: City filter (e.g., "Lahore")
- `input_csv`: Filename for storing extracted links
- `output_csv`: Filename for storing scraped data

## Code Structure and Components

### Main Functions

1. **setup_driver()**: Initializes and configures the Chrome WebDriver
2. **connect_to_db()**: Establishes a connection to the SQLite database
3. **navigate_to_mobiles()**: Navigates to the Mobile Phones section on OLX
4. **select_location()**: Applies location filters (province and city)
5. **set_price_range()**: Sets minimum and maximum price filters
6. **scroll_and_click_load_more()**: Scrolls down the page and clicks "Load more" button
7. **link_extracter()**: Extracts listing URLs and saves them to CSV and database
8. **to_csv()**: Helper function to save data to CSV files
9. **link_open()**: Opens each listing URL and extracts detailed information
10. **data_scrap()**: Extracts specific data fields from a listing page
11. **insert_links()**: Inserts extracted links into the database
12. **insert_mobile_data()**: Inserts mobile phone data into the database
13. **main()**: Orchestrates the entire scraping process

### Database Operations

The scraper performs the following database operations:
1. Connects to the SQLite database
2. Inserts unique listing URLs into the Link table
3. Extracts detailed information from each listing
4. Inserts the extracted data into the Mobiles table

## Troubleshooting and Common Issues

### Browser Automation Issues
- **Element not found errors**: The script uses explicit waits, but OLX's website structure might change. If elements can't be found, check the XPath selectors in the code.
- **Timeout errors**: Increase the wait time in WebDriverWait instances if the website is loading slowly.
- **CAPTCHA challenges**: If OLX detects automated access, it might show CAPTCHA challenges. Consider adding delays between actions.

### Data Extraction Issues
- **Missing data**: The script handles exceptions for missing elements, but check the output CSV for "N/A" values that might indicate missing data.
- **Encoding issues**: If special characters appear incorrectly in the CSV, ensure proper UTF-8 encoding.

### Database Issues
- **Database locked errors**: Ensure no other process is accessing the database file when running the script.
- **Table does not exist errors**: Make sure the database tables are properly created before running the script.
- **Unique constraint failures**: The Link table has a unique constraint on the link_url column, so duplicate links will be ignored.

## Future Improvements

Potential enhancements for the project:
- Add proxy support to avoid IP blocking
- Implement more robust error handling and retry mechanisms
- Add support for additional filters (brand, condition, etc.)
- Create a user interface for easier configuration
- Implement data analysis and visualization tools
- Add support for other OLX categories beyond mobile phones
- Optimize the scraping speed by using headless browser mode
- Add logging for better debugging and monitoring
- Implement a more sophisticated database schema with relationships between tables
- Add data validation and cleaning before database insertion
- Create database migration scripts for easier schema updates

## Known Limitations

- The scraper is limited to 2 scrolls, which may not capture all available listings
- The script uses fixed XPath selectors that may break if OLX changes its website structure
- There's no built-in mechanism to handle CAPTCHA challenges
- The script doesn't implement rate limiting, which might lead to IP blocking
- Error handling is basic and may not recover from all types of failures
- The database schema doesn't enforce relationships between tables

## Legal and Ethical Considerations

Web scraping may be subject to legal restrictions and website terms of service. Consider the following:
- Respect OLX's robots.txt file and terms of service
- Implement reasonable delays between requests to avoid overloading the server
- Use the data for personal or research purposes only
- Do not use the scraper for commercial purposes without proper authorization
- Be aware that excessive scraping might lead to IP blocking

## License

This project is provided for educational purposes only. Use at your own risk and responsibility.

## Credits and Acknowledgments

This project was developed as a tool for data collection and analysis of the mobile phone market in Pakistan. 