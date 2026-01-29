import requests
import os
from datetime import datetime


AIRTABLE_BASE_ID = "appOYqZxm2uaHjCxF"
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")

PRODUCT_ALIASES = {
    "şeker": "AS",
    "şeker gübresi": "AS",
    "amonyum sülfat": "AS",
    "beyaz gübre": "AS",

    "3 15": "15.15.15",
    "üç onbeş": "15.15.15",
    "15 15 15": "15.15.15",
    "toprak altı": "15.15.15",

    "üre": "ÜRE %46",
    "azot": "ÜRE %46",
    "beyaz inci": "ÜRE %46",

    "dap": "DAP 18-46",
    "taban gübresi": "DAP 18-46",
    "kara gübre": "DAP 18-46",

    "20 20": "20.20.0",

    "nitrat": "Amonyum Nitrat", # 'nitrat' derse diğerine gitsin
    "26 nitrat": "Amonyum Nitrat",
    "can gübresi": "Amonyum Nitrat",

}


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


def get_all_products():
    # Ürünlerinin olduğu tablonun adı (Örn: "Inventory" veya "Products")
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Products"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        records = response.json().get("records", [])

        product_list = [r["fields"].get("ProductName").strip() for r in records if r["fields"].get("ProductName")]
        return product_list
    return "Ürün listesi şu an alınamıyor."


def get_product_search_pool():
    """
    Airtable'daki resmi ürün listesi ile PRODUCT_ALIASES sözlüğünü birleştirir.
    Geriye { "aranacak_kelime": "RESMİ_ÜRÜN_ADI" } formatında tek bir sözlük döndürür.
    """
    # 1. Senin yazdığın get_all_products fonksiyonunu kullanıyoruz
    official_products = get_all_products()

    # Eğer hata dönerse veya liste boşsa boş dön
    if not isinstance(official_products, list):
        return {}

    # 2. Önce resmi isimleri havuza at: { "as": "AS", "15.15.15": "15.15.15" }
    # Hepsini küçük harfe çeviriyoruz ki arama kolay olsun
    pool = {name.lower(): name for name in official_products}

    # 3. Senin tanımladığın ALIAS'ları ekle
    # PRODUCT_ALIASES sözlüğünü dosyanın başından okuyor
    for alias, official_name in PRODUCT_ALIASES.items():
        # Sadece hedef ürün gerçekten listede varsa alias'ı ekle (Güvenlik)
        # Böylece stokta olmayan bir şeye yönlendirmeyiz
        if official_name in official_products:
            pool[alias.lower()] = official_name

    return pool
