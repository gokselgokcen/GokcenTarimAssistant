import requests
import os

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


def create_lead(name, surname, phone, email=""):
    # Sadece Customers tablosuna gider
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Customers"

    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "Surname": surname,
                    "Phone": phone,
                    "Email": email
                }
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return "Kayıt başarılı." if response.status_code == 200 else "Kayıt başarısız."