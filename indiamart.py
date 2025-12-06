from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from collections import OrderedDict

# --------------- CONFIG --------------- #
keyword = "Wind Sensor"
output_file = "indiamart_wind_sensor.csv"
scroll_pause = 3
max_clicks = 60  
cooldown_every = 10
# ------------------------------------- #

# ✅ Chrome setup
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--headless")  # Uncomment for background run

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://dir.indiamart.com/impcat/solar-panels.html")
print(f"🔍 Searching for: {keyword}\n")

input("⏸️ Please log in manually (mobile + OTP). Once logged in and results appear, press ENTER here...")

# ✅ Ordered City-State Map
city_state_map = OrderedDict([
    # 🌆 North India
    ("New Delhi", "Delhi"), ("Noida", "Uttar Pradesh"), ("Gurugram", "Haryana"), ("Ghaziabad", "Uttar Pradesh"),
    ("Faridabad", "Haryana"), ("Lucknow", "Uttar Pradesh"), ("Kanpur", "Uttar Pradesh"),
    ("Bareilly", "Uttar Pradesh"), ("Prayagraj", "Uttar Pradesh"), ("Agra", "Uttar Pradesh"),
    ("Varanasi", "Uttar Pradesh"), ("Meerut", "Uttar Pradesh"), ("Aligarh", "Uttar Pradesh"),
    ("Moradabad", "Uttar Pradesh"), ("Mathura", "Uttar Pradesh"), ("Firozabad", "Uttar Pradesh"),
    ("Amritsar", "Punjab"), ("Mohali", "Punjab"), ("Ludhiana", "Punjab"), ("Jalandhar", "Punjab"), ("Patiala", "Punjab"),
    ("Jaipur", "Rajasthan"), ("Jodhpur", "Rajasthan"), ("Udaipur", "Rajasthan"), ("Kota", "Rajasthan"),
    ("Ajmer", "Rajasthan"), ("Bikaner", "Rajasthan"), ("Jaisalmer", "Rajasthan"), ("Sikar", "Rajasthan"),
    ("Shimla", "Himachal Pradesh"), ("Dharamshala", "Himachal Pradesh"),
    ("Srinagar", "Jammu and Kashmir"), ("Jammu", "Jammu and Kashmir"), ("Leh", "Ladakh"),
    ("Dehradun", "Uttarakhand"), ("Haridwar", "Uttarakhand"), ("Rishikesh", "Uttarakhand"),

    # 🌅 West India
    ("Ahmedabad", "Gujarat"), ("Surat", "Gujarat"), ("Vadodara", "Gujarat"), ("Rajkot", "Gujarat"),
    ("Gandhinagar", "Gujarat"), ("Bhavnagar", "Gujarat"), ("Jamnagar", "Gujarat"), ("Junagadh", "Gujarat"),
    ("Palanpur", "Gujarat"), ("Morbi", "Gujarat"),
    ("Mumbai", "Maharashtra"), ("Pune", "Maharashtra"), ("Nagpur", "Maharashtra"),
    ("Aurangabad", "Maharashtra"), ("Nashik", "Maharashtra"), ("Amaravati", "Maharashtra"),
    ("Kolhapur", "Maharashtra"), ("Solapur", "Maharashtra"), ("Thane", "Maharashtra"), ("Sangli", "Maharashtra"),
    ("Panaji", "Goa"), ("Margao", "Goa"),
    ("Bhubaneswar", "Odisha"), ("Cuttack", "Odisha"), ("Rourkela", "Odisha"), ("Puri", "Odisha"), ("Sambalpur", "Odisha"),

    # 🌴 South India
    ("Chennai", "Tamil Nadu"), ("Coimbatore", "Tamil Nadu"), ("Madurai", "Tamil Nadu"), ("Salem", "Tamil Nadu"),
    ("Tiruchirappalli", "Tamil Nadu"), ("Erode", "Tamil Nadu"), ("Vellore", "Tamil Nadu"), ("Tirunelveli", "Tamil Nadu"),
    ("Bengaluru", "Karnataka"), ("Mysuru", "Karnataka"), ("Mangaluru", "Karnataka"),
    ("Hubballi", "Karnataka"), ("Belagavi", "Karnataka"), ("Davanagere", "Karnataka"), ("Kalaburagi", "Karnataka"),
    ("Ballari", "Karnataka"),
    ("Hyderabad", "Telangana"), ("Warangal", "Telangana"), ("Nizamabad", "Telangana"), ("Karimnagar", "Telangana"),
    ("Mahbubnagar", "Telangana"),
    ("Vijayawada", "Andhra Pradesh"), ("Visakhapatnam", "Andhra Pradesh"), ("Tirupati", "Andhra Pradesh"),
    ("Nellore", "Andhra Pradesh"), ("Guntur", "Andhra Pradesh"), ("Kurnool", "Andhra Pradesh"),
    ("Kadapa", "Andhra Pradesh"), ("Anantapur", "Andhra Pradesh"),
    ("Kochi", "Kerala"), ("Thiruvananthapuram", "Kerala"), ("Kozhikode", "Kerala"), ("Thrissur", "Kerala"),
    ("Palakkad", "Kerala"),
    ("Pondicherry", "Puducherry"),

    # 🌄 East & Northeast India
    ("Kolkata", "West Bengal"), ("Howrah", "West Bengal"), ("Durgapur", "West Bengal"),
    ("Asansol", "West Bengal"), ("Siliguri", "West Bengal"), ("Darjeeling", "West Bengal"),
    ("Guwahati", "Assam"), ("Silchar", "Assam"), ("Dibrugarh", "Assam"), ("Tezpur", "Assam"),
    ("Agartala", "Tripura"), ("Itanagar", "Arunachal Pradesh"), ("Naharlagun", "Arunachal Pradesh"),
    ("Shillong", "Meghalaya"), ("Tura", "Meghalaya"),
    ("Imphal", "Manipur"), ("Aizawl", "Mizoram"), ("Kohima", "Nagaland"), ("Dimapur", "Nagaland"),
    ("Gangtok", "Sikkim"), ("Pasighat", "Arunachal Pradesh"),

    # 🌾 Central India
    ("Bhopal", "Madhya Pradesh"), ("Indore", "Madhya Pradesh"), ("Gwalior", "Madhya Pradesh"),
    ("Jabalpur", "Madhya Pradesh"), ("Ujjain", "Madhya Pradesh"), ("Sagar", "Madhya Pradesh"),
    ("Rewa", "Madhya Pradesh"), ("Neemuch", "Madhya Pradesh"), ("Rajgarh", "Madhya Pradesh"),
    ("Raipur", "Chhattisgarh"), ("Bhilai", "Chhattisgarh"), ("Bilaspur", "Chhattisgarh"), ("Korba", "Chhattisgarh"),
    ("Patna", "Bihar"), ("Gaya", "Bihar"), ("Muzaffarpur", "Bihar"), ("Bhagalpur", "Bihar"), ("Darbhanga", "Bihar"),
    ("Ranchi", "Jharkhand"), ("Dhanbad", "Jharkhand"), ("Jamshedpur", "Jharkhand"), ("Bokaro", "Jharkhand"),
    ("Hazaribagh", "Jharkhand")
])

wait = WebDriverWait(driver, 25)
all_data = []

for idx, (city, state) in enumerate(city_state_map.items(), 1):
    print(f"\n🏙️ [{idx}/{len(city_state_map)}] Scraping: {city}, {state}")

    try:
        # Build URL with city filter
        url = f"https://dir.indiamart.com/search.mp?ss={keyword.replace(' ', '%20')}&cq={city.replace(' ', '%20')}"
        driver.get(url)
        time.sleep(5)

        # Wait until some products appear
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".card")))
            print(f"✅ Listings loaded for {city}")
        except:
            print(f"⚠️ No listings for {city}, skipping.")
            continue

        # Infinite scroll and Show More clicks
        click_count = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause)
            try:
                show_more = driver.find_element(By.XPATH, "//span[normalize-space()='Show More Results']")
                driver.execute_script("arguments[0].click();", show_more)
                click_count += 1
                print(f"🟢 Clicked 'Show More Results' ({click_count}) for {city}")
                time.sleep(scroll_pause + 1)
            except:
                print(f"⚙️ No more results for {city}.")
                break
            if click_count % cooldown_every == 0:
                time.sleep(10)
            if click_count >= max_clicks:
                break

        # Parse product data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.select(".card")
        print(f"📦 Found {len(cards)} products in {city}")

        for card in cards:
            name_tag = card.select_one("a.cardlinks[href*='proddetail']")
            product_name = name_tag.get_text(strip=True) if name_tag else "N/A"
            product_link = name_tag["href"] if name_tag and name_tag.has_attr("href") else "N/A"
            company_tag = card.select_one("a.cardlinks[data-click*='CompanyName']")
            company_name = company_tag.get_text(strip=True) if company_tag else "N/A"
            price_tag = card.select_one(".price")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            location_tag = card.select_one("span.cmp-loc")
            location = location_tag.get_text(strip=True) if location_tag else city
            rating_tag = card.select_one("span.bo.color")
            review_tag = card.select_one("span.color")
            rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"
            reviews = review_tag.get_text(strip=True).strip("()") if review_tag else "N/A"

            all_data.append({
                "State": state,
                "City": city,
                "Product Name": product_name,
                "Price": price,
                "Company": company_name,
                "Location": location,
                "Rating": rating,
                "Reviews": reviews,
                "Product Link": product_link
            })

        # Save progress after each city
        df = pd.DataFrame(all_data)
        df.drop_duplicates(subset=["Product Name", "Company", "City"], inplace=True)
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"💾 Progress saved ({len(df)} rows total).")

    except Exception as e:
        print(f"❌ Error scraping {city}: {e}")
        continue

# ✅ Done
driver.quit()
print(f"\n✅ Scraping completed — Total {len(all_data)} products saved to {output_file}")
