import json
from app.services.catalog import HOME_CATALOG, PARTY_CATALOG, JEWELRY_CATALOG, search_url

def _pick(catalog, budget, keywords=()):
    results = []
    target = max(budget, 1)
    for item in catalog:
        score = 1
        hay = f"{item['name']} {item['category']}".lower()
        for k in keywords:
            if k.lower() in hay:
                score += 3
        midpoint = (item["min"] + item["max"]) / 2
        if midpoint <= target:
            score += 2
        results.append((score, item))
    results.sort(key=lambda x: (-x[0], x[1]["min"]))
    return [x[1] for x in results[:5]]

def mock_home(data):
    budget = data["budget"]
    chosen = _pick(HOME_CATALOG, budget / max(len(data["items"]), 1),
                   [x["category"] for x in data["items"]])
    items = []
    remaining = budget
    for idx, p in enumerate(chosen):
        price = min(p["max"], max(p["min"], round(budget * (0.12 if idx < 3 else 0.08))))
        if price > remaining:
            price = min(p["min"], remaining)
        if price <= 0:
            continue
        items.append({
            "name": p["name"], "category": p["category"],
            "estimated_price": round(price, 2), "platform": p["platform"],
            "reason": f"Fits a {data['style']} style and keeps the plan within the requested budget.",
            "search_url": search_url(p["platform"], p["name"])
        })
        remaining -= price
    return {
        "planner": "home", "summary": f"A {data['style']} home setup prioritizing the requested rooms and items.",
        "budget": budget, "allocated_total": round(budget - remaining, 2), "items": items,
        "tips": ["Keep 10% of the budget as a contingency.", "Buy high-use items first.", "Measure room dimensions before ordering furniture."],
        "disclaimer": "Prices are estimates and may change. Links are search links, not live inventory guarantees.",
        "ai_source": "mock-fallback"
    }

def mock_party(data):
    budget, guests = data["budget"], data["guests"]
    food = min(budget * 0.45, guests * 300)
    venue = budget * 0.25
    decor = budget * 0.20
    items = [
        {"name": "Catering package", "category": "food", "estimated_price": round(food,2), "platform":"Zomato",
         "reason": f"Food allocation sized for approximately {guests} guests.", "search_url":search_url("Zomato", data["event_type"]+" catering")},
        {"name": "Party food package", "category": "food", "estimated_price": round(max(500, food*0.35),2), "platform":"Swiggy",
         "reason": "Useful as an alternate food sourcing option.", "search_url":search_url("Swiggy", data["event_type"]+" party food")},
        {"name": "Venue / stay option", "category": "venue", "estimated_price": round(venue,2), "platform":"OYO",
         "reason": "Provides a starting point for venue or stay research.", "search_url":search_url("OYO", data["city"]+" event stay")},
        {"name": "Balloon decoration package", "category": "decoration", "estimated_price": round(decor,2), "platform":"Amazon",
         "reason": "A flexible decoration option for the event type.", "search_url":search_url("Amazon", data["event_type"]+" decoration")}
    ]
    total = sum(x["estimated_price"] for x in items)
    return {"planner":"party","summary":f"Budget plan for a {data['event_type']} with {guests} guests.",
            "budget":budget,"allocated_total":round(total,2),"items":items,
            "tips":["Confirm guest count before final catering.", "Reserve a contingency for last-minute expenses.", "Compare delivery and venue charges separately."],
            "disclaimer":"Vendor prices and availability are estimates; verify current prices before purchase.",
            "ai_source":"mock-fallback"}

def mock_jewelry(data):
    chosen = _pick(JEWELRY_CATALOG, data["budget"], [data["style"], "jewelry"])
    items=[]
    for p in chosen[:4]:
        price=min(p["max"], max(p["min"], data["budget"]*0.22))
        items.append({"name":p["name"],"category":p["category"],"estimated_price":round(price,2),
                      "platform":p["platform"],
                      "reason":f"Suggested for a {data['style']} look and {data['occasion']} occasion.",
                      "search_url":search_url(p["platform"], p["name"])})
    return {"planner":"jewelry","summary":f"Jewelry ideas for a {data['occasion']} occasion with a {data['style']} preference.",
            "budget":data["budget"],"allocated_total":round(sum(x["estimated_price"] for x in items),2),
            "items":items,"tips":["Match metal tone with the outfit details.", "For a statement piece, keep the other accessories simpler.", "Verify dimensions and return policy before ordering."],
            "disclaimer":"AI recommendations are style guidance; verify product details and current prices on the retailer page.",
            "ai_source":"mock-fallback"}
