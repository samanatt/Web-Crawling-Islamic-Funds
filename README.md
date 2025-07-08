# 🕌 Islamic Funds Scraper - SEEI.ir 🇮🇷

A **Python-based web scraper** that extracts detailed records of Islamic investment funds from [SEEI.ir](https://seei.ir/default.aspx?tabid=113). This project automates data collection from a **complex ASP.NET-powered web portal** using `Selenium` and `BeautifulSoup`.

---

## 🔍 Overview

The SEEI.ir website presents paginated and JavaScript-driven data about Islamic financial funds and cooperatives. Each row in the fund table contains a “Details” button that triggers a **modal popup** with deeper information. This scraper is capable of:

- Navigating through paginated results.
- Clicking modal detail buttons dynamically for each fund.
- Extracting 9 key fields per fund.
- Storing all results in a structured **CSV file** with proper Unicode support.

---

## ⚙️ Technologies Used

| Library         | Purpose                                       |
|----------------|-----------------------------------------------|
| `Selenium`      | Browser automation, JavaScript execution     |
| `BeautifulSoup` | DOM parsing and HTML element extraction      |
| `pandas`        | Structuring and exporting final dataset       |
| `ChromeDriver`  | Headless/GUI browser interaction             |

---

## 📁 Extracted Fields

Each fund entry includes the following features:

- `Name`
- `Province`
- `Country`
- `City`
- `Village`
- `Address`
- `Phone Code` and `Second Phone`
- `Registration Number`
- `National Code`

All values are normalized — if a field is missing, it is replaced with `"NULL"`.

---

## 🚦 How It Works

1. **Open SEEI.ir and wait for the fund table.**
2. **Find and iterate over each table row** with class `FundStatusLicensed`.
3. For each row:
   - **Construct the dynamic ID** for the detail button (e.g. `ctl13_ctl03_ctl00_Search__rgFunds_ctl00_ctl04__imgbDetail`).
   - Click the button using Selenium and wait for the modal popup.
   - Parse all span values from the modal using `BeautifulSoup`.
4. Store structured data into lists, mapping each fund to its modal contents.
5. Move to the next page using the `.rgPageNext` button and repeat the process.
6. Save everything into `funds_data.csv`.

---

## 💻 Example: Switching to GUI Mode

By default, Chrome is launched headlessly. To **enable GUI** mode for debugging:

```python
options = Options()
# Comment out the headless flag:
# options.add_argument("--headless")


📦 Output Sample (CSV)

Name,Province,Country,City,Village,Address,Phone Code,Phone Code 2,Reg Number,National Code
ولی عصر(عج),مازندران,ساری,ساری,میاندرود,"مازندران - ساری - میاندرود ...",01132,2345,28,10760007282
ثامن الائمه(ع),مازندران,ساری,ساری,میاندرود,"مازندران - ساری - میاندرود ...",01132,6789,25,10760006623
...

...
CSV is encoded as utf-8-sig for compatibility with Excel and Persian text.

📌 Business Motivation
The Islamic Funds Registry maintained by SEEI is a crucial dataset for:

Financial analysts assessing Islamic cooperative activities in Iran.

Governmental/regulatory use (e.g., mapping fund location to economic zones).

Researchers studying rural development or social finance networks.

Data platforms aggregating Sharia-compliant institutions.

🔒 Disclaimer
This scraper is built for educational and research purposes only.
Ensure you have permission before using automated tools on any third-party website.


