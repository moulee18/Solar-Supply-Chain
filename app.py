from flask import Flask, render_template, request
import csv
import re
from decimal import Decimal
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "products.csv")
# keyword-based category inference (extend as needed)
CATEGORY_KEYWORDS = {
    "Solar Panel": ["panel", "pv module", "solar panel", "module"],
    "Inverters": ["inverter", "microinverter"],
    "Surge Protection Devices": ["surge", "spd", "surge protection"],
    "Energy Meter": ["meter", "energy meter"],
    "Combiner & Fuse Boxes": ["combiner", "fuse", "junction box"],
    "Data Logger": ["logger", "data logger"],
    "DC Cables": ["cable", "dc cable"],
    "Monitoring System": ["monitor", "monitoring"],
    "Solar Sensor": ["pyranometer", "sensor"],
    "Solar Tracker": ["tracker"],
    "Solar Tester": ["tester", "test kit", "multimeter", "solar tester"]
}

def infer_category(product_name: str):
    if not product_name:
        return "Other"
    s = product_name.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in s:
                return cat
    return "Other"

def parse_price(price_str):
    if not price_str:
        return None
    s = re.sub(r'[^\d\.,]', '', price_str)
    s = s.replace(',', '')
    try:
        return Decimal(s)
    except:
        return None

def load_data():
    items = []
    with open(DATA_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # detect if CSV contains Category column
        has_category_col = 'Category' in reader.fieldnames if reader.fieldnames else False
        for row in reader:
            row_clean = dict(row)
            row_clean['PriceNum'] = parse_price(row.get('Price', ''))
            try:
                row_clean['RatingNum'] = float(row.get('Rating') or 0)
            except:
                row_clean['RatingNum'] = 0.0
            # set Category: CSV column preferred, else infer from product name
            if has_category_col and row.get('Category'):
                row_clean['Category'] = row.get('Category').strip()
            else:
                row_clean['Category'] = infer_category(row.get('Product Name',''))
            items.append(row_clean)
    return items

@app.template_filter('currency_format')
def currency_format(value):
    if value is None:
        return ""
    return f"₹{value:,.2f}"

@app.route("/", methods=["GET"])
def index():
    items = load_data()

    # unique filter values
    states = sorted({i.get('State','').strip() for i in items if i.get('State')})
    cities = sorted({i.get('City','').strip() for i in items if i.get('City')})
    companies = sorted({i.get('Company','').strip() for i in items if i.get('Company')})
    categories = sorted({i.get('Category','').strip() for i in items if i.get('Category')})

    # params
    q = request.args.get('q', '').strip().lower()
    state_f = request.args.get('state', '')
    city_f = request.args.get('city', '')
    company_f = request.args.get('company', '')
    category_f = request.args.get('category', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    min_rating = request.args.get('min_rating', '')

    try:
        min_price_val = Decimal(min_price) if min_price else None
    except:
        min_price_val = None
    try:
        max_price_val = Decimal(max_price) if max_price else None
    except:
        max_price_val = None
    try:
        min_rating_val = float(min_rating) if min_rating else None
    except:
        min_rating_val = None

    def matches(item):
        if q:
            hay = " ".join([
                str(item.get('Product Name','')),
                str(item.get('Company','')),
                str(item.get('City','')),
                str(item.get('Location',''))
            ]).lower()
            if q not in hay:
                return False
        if state_f and item.get('State','') != state_f:
            return False
        if city_f and item.get('City','') != city_f:
            return False
        if company_f and item.get('Company','') != company_f:
            return False
        if category_f and item.get('Category','') != category_f:
            return False
        if min_price_val is not None:
            if item.get('PriceNum') is None or item['PriceNum'] < min_price_val:
                return False
        if max_price_val is not None:
            if item.get('PriceNum') is None or item['PriceNum'] > max_price_val:
                return False
        if min_rating_val is not None:
            if item.get('RatingNum') is None or item['RatingNum'] < min_rating_val:
                return False
        return True

    filtered_all = [i for i in items if matches(i)]
    filtered = filtered_all[:20]  # keep the top 20 limit as requested

    return render_template(
        "index.html",
        items=filtered,
        count=len(filtered_all),
        states=states,
        cities=cities,
        companies=companies,
        categories=categories,
        filters=request.args
    )

if __name__ == "__main__":
    app.run(debug=True)
