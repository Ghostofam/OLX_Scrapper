# OLX Mobile Phone Scraper

A Python-based web scraper designed to extract mobile phone listings from OLX Pakistan, with customizable filters for location and price range.

## Project Overview

This project automates the process of collecting mobile phone listings data from OLX Pakistan. It navigates to the mobile phones section, applies location and price filters, and extracts detailed information about each listing including:

- Product name
- Price
- Location
- Posting date
- Product description
- Original listing URL

The scraper uses Selenium WebDriver to interact with the OLX website, simulating user actions like clicking, scrolling, and form input. Data is saved in CSV format for easy analysis and processing.

## File and Directory Structure

```
OLX_Bot/
├── .env                    # Environment variables and configuration
├── .gitignore              # Git ignore file
├── scrapper.py             # Main scraper script
├── extracted_links.csv     # Intermediate file storing listing URLs
├── scrapped_data_1.csv     # Final output file with scraped data
└── .venv/                  # Python virtual environment
```

## Dependencies

The project relies on the following Python packages:
- Selenium: For browser automation and web scraping
- webdriver_manager: For automatic ChromeDriver management
- python-dotenv: For environment variable management
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
max_price_value = "20000"
city = "Lahore"
province = "Punjab"
input_csv = "extracted_links.csv"
output_csv = "scrapped_data.csv"
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
5. Set price range filters (10,000 - 20,000 PKR by default)
6. Scroll and load more listings (limited to 2 scrolls in the current implementation)
7. Extract listing URLs to `extracted_links.csv`
8. Visit each listing URL and extract detailed information
9. Save all scraped data to `scrapped_data.csv`
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
2. **navigate_to_mobiles()**: Navigates to the Mobile Phones section on OLX
3. **select_location()**: Applies location filters (province and city)
4. **set_price_range()**: Sets minimum and maximum price filters
5. **scroll_and_click_load_more()**: Scrolls down the page and clicks "Load more" button
6. **link_extracter()**: Extracts listing URLs and saves them to CSV
7. **to_csv()**: Helper function to save data to CSV files
8. **link_open()**: Opens each listing URL and extracts detailed information
9. **data_scrap()**: Extracts specific data fields from a listing page
10. **main()**: Orchestrates the entire scraping process

## Troubleshooting and Common Issues

### Browser Automation Issues
- **Element not found errors**: The script uses explicit waits, but OLX's website structure might change. If elements can't be found, check the XPath selectors in the code.
- **Timeout errors**: Increase the wait time in WebDriverWait instances if the website is loading slowly.
- **CAPTCHA challenges**: If OLX detects automated access, it might show CAPTCHA challenges. Consider adding delays between actions.

### Data Extraction Issues
- **Missing data**: The script handles exceptions for missing elements, but check the output CSV for "N/A" values that might indicate missing data.
- **Encoding issues**: If special characters appear incorrectly in the CSV, ensure proper UTF-8 encoding.

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
