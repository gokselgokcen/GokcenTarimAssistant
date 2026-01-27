import requests
import os
from datetime import datetime

# Sabit Bilgiler
AIRTABLE_BASE_ID = "appOYqZxm2uaHjCxF"
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")


def get_product_price(product_name):
    # Sadece Products tablosuna gider
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Products"

    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    # Resimdeki ProductName sütununda arama yapar
    params = {"filterByFormula": f"FIND('{product_name}', {{ProductName}})"}

    print(f"--- Ürün Sorgulanıyor: {product_name} ---")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        records = response.json().get("records", [])
        if records:
            fields = records[0].get("fields", {})
            # Resmindeki Price ve Stok sütunlarını alıyoruz
            return {
                "fiyat": fields.get("Price"),
                "stok": fields.get("Stok"),
                "urun": fields.get("ProductName")
            }
    return "Ürün bulunamadı."


def create_lead(name, phone, email="",notes="",**kwargs):
    surname = kwargs.get("surname", "")
    full_name = f"{name} {surname}".strip() if surname else name
    # Sadece Customers tablosuna gider
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Customers"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    today =datetime.now().strftime("%Y-%m-%d")


    data = {
        "records": [
            {
                "fields": {
                    "Name": full_name,
                    "Telefon": phone,
                    "Email": email,
                    "Date":  today,
                    "Notes": notes
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200,201]:
        print("Customer saved...")
        return "Customer saved..."
    else:
        print(f"err: {response.status_code}: {response.text}")
        return f"NOT SAVED err: {response.status_code}: {response.text}"
