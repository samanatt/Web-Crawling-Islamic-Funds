

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Headless Chrome settings
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
driver.get("https://seei.ir/default.aspx?tabid=113")
wait = WebDriverWait(driver, 15)

# Feature lists
names = []
province = []
country = []
city = []
Village = []
address = []
code_tel = []
tel_alt = []  
reg_num = []
national_code = []

def get_text_or_null(tag):
    return tag.text.strip() if tag and tag.text.strip() else "NULL"

while True:
    # Retry loading table if needed
    for attempt in range(2):
        try:
            wait.until(EC.presence_of_element_located((By.ID, 'ctl13_ctl03_ctl00_SearchrgFunds_ctl00')))
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            table = soup.find('table', {'id': 'ctl13_ctl03_ctl00_SearchrgFunds_ctl00'})
            rows = table.find_all('tr', class_='FundStatusLicensed')
            if rows:
                break
        except:
            if attempt == 1:
                driver.quit()
                raise Exception("Table not loaded after retries.")
            driver.refresh()
            time.sleep(2)

    for i, row in enumerate(rows):
        try:
            btn_id = f'ctl13_ctl03_ctl00_Search__rgFunds_ctl00_ctl{str(2*i+4).zfill(2)}__imgbDetail'
            detail_button = driver.find_element(By.ID, btn_id)
            driver.execute_script("arguments[0].scrollIntoView(true);", detail_button)
            time.sleep(0.5)
            detail_button.click()

            time.sleep(1)
            modal_soup = BeautifulSoup(driver.page_source, 'html.parser')
            detail_items = modal_soup.find_all("div", class_=["col-6 col-md-6 detailItem", "col-12 col-md-6 detailItem"])
            row_data = []

            for div in detail_items:
                spans = div.find_all("span")
                row_data.append(get_text_or_null(spans[1]) if len(spans) >= 2 else "NULL")

            while len(row_data) < 9:
                row_data.append("NULL")

            names.append(row_data[0])
            province.append(row_data[1])
            country.append(row_data[2])
            city.append(row_data[3])
            Village.append(row_data[4])
            address.append(row_data[5])

        
	#Phone number 1 & 2
            tel_parts = str(row_data[6]).split('-')
            if len(tel_parts) == 2:
                code_tel.append(tel_parts[0].strip())
                tel_alt.append(tel_parts[1].strip())
            else:
                code_tel.append(str(row_data[6]).strip())
                tel_alt.append("NULL")

            reg_num.append(row_data[7])
            national_code.append(row_data[8])

            driver.execute_script("$('.modal.fade.show').modal('hide');")
            time.sleep(0.5)

        except:
            continue

    # try to go to the next page
    try:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pager_div = soup.find('div', {'class': 'rgWrap rgNumPart'})
        current_page_tag = pager_div.find('a', class_='rgCurrentPage')
        all_page_tags = pager_div.find_all('a')

        if not current_page_tag:
            break

        current_page = int(current_page_tag.text.strip())

        # Try to find Next button
        next_button = driver.find_element(By.XPATH,
            '/html/body/form/div[4]/div[8]/div/div/div[2]/div/div/div[3]/div/div/table/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]'
        )

        # Scroll and click next
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(0.5)
        old_page = current_page
        next_button.click()

        # Wait for page number to update (otherwise break)
        try:
            WebDriverWait(driver, 15).until(
                lambda d: int(BeautifulSoup(d.page_source, 'html.parser')
                              .find('a', class_='rgCurrentPage').text.strip()) != old_page
            )
        except:
            break

        time.sleep(1)

    except:
        break


df = pd.DataFrame({
    "Name": names,
    "Province": province,
    "Country": country,
    "City": city,
    "Village": Village,
    "Address": address,
    "Phone Code": code_tel,
    "Phone Code 2": tel_alt,
    "Reg Number": reg_num,
    "National Code": national_code
})

print(df.head())

df.to_csv("funds_data.csv", index=False, encoding='utf-8-sig')
