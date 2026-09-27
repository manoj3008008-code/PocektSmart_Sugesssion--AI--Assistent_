from urllib.parse import quote_plus

PLATFORMS = {
    "amazon": "Amazon",
    "flipkart": "Flipkart",
    "ikea": "IKEA",
    "swiggy": "Swiggy",
    "zomato": "Zomato",
    "oyo": "OYO",
}

def search_url(platform: str, query: str) -> str:
    q = quote_plus(query)
    mapping = {
        "Amazon": f"https://www.amazon.in/s?k={q}",
        "Flipkart": f"https://www.flipkart.com/search?q={q}",
        "IKEA": f"https://www.ikea.com/in/en/search/?q={q}",
        "Swiggy": f"https://www.swiggy.com/search?query={q}",
        "Zomato": f"https://www.zomato.com/chennai/restaurants?query={q}",
        "OYO": f"https://www.oyorooms.com/search?location={q}",
    }
    return mapping.get(platform, f"https://www.google.com/search?q={q}")

HOME_CATALOG = [
    {"name": "LED ceiling light", "category": "lighting", "min": 700, "max": 4500, "platform": "Amazon"},
    {"name": "Modern ceiling fan", "category": "fan", "min": 2200, "max": 7500, "platform": "Amazon"},
    {"name": "Compact study table", "category": "furniture", "min": 3500, "max": 12000, "platform": "IKEA"},
    {"name": "6-seater dining table", "category": "furniture", "min": 9000, "max": 30000, "platform": "IKEA"},
    {"name": "Accent wall art", "category": "decor", "min": 800, "max": 6000, "platform": "Flipkart"},
    {"name": "Decorative indoor plant", "category": "decor", "min": 500, "max": 3000, "platform": "IKEA"},
    {"name": "Curtain set", "category": "decor", "min": 900, "max": 5000, "platform": "Amazon"},
]

PARTY_CATALOG = [
    {"name": "Catering package", "category": "food", "min": 180, "max": 650, "platform": "Zomato"},
    {"name": "Party food package", "category": "food", "min": 150, "max": 550, "platform": "Swiggy"},
    {"name": "Venue / stay option", "category": "venue", "min": 1500, "max": 12000, "platform": "OYO"},
    {"name": "Balloon decoration package", "category": "decoration", "min": 1500, "max": 10000, "platform": "Amazon"},
    {"name": "Table decoration kit", "category": "decoration", "min": 800, "max": 4500, "platform": "Flipkart"},
]

JEWELRY_CATALOG = [
    {"name": "Minimal pendant necklace", "category": "necklace", "min": 700, "max": 5000, "platform": "Amazon"},
    {"name": "Statement earrings", "category": "earrings", "min": 500, "max": 4000, "platform": "Flipkart"},
    {"name": "Elegant bracelet", "category": "bracelet", "min": 600, "max": 4500, "platform": "Amazon"},
    {"name": "Classic jewelry set", "category": "set", "min": 1500, "max": 9000, "platform": "Flipkart"},
]
