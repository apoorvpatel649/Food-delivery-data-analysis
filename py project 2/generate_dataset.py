"""
generate_dataset.py
-------------------
Generates a realistic synthetic Food Delivery dataset and saves it as CSV.
Run this FIRST before running the main analysis.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

# ── Configuration ────────────────────────────────────────────────────────────
NUM_RECORDS = 1000

RESTAURANTS = [
    "Spice Garden", "Pizza Hub", "Burger Barn", "Noodle House",
    "Sushi World", "Taco Town", "Curry Palace", "The Grill",
    "Wok Express", "Healthy Bites"
]

CUISINES = {
    "Spice Garden": "Indian",  "Pizza Hub": "Italian",
    "Burger Barn": "American", "Noodle House": "Chinese",
    "Sushi World": "Japanese", "Taco Town": "Mexican",
    "Curry Palace": "Indian",  "The Grill": "Continental",
    "Wok Express": "Chinese",  "Healthy Bites": "Healthy"
}

CITIES = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai",
          "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow"]

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Cash", "Wallet"]
ORDER_STATUS    = ["Delivered", "Cancelled", "Pending"]
WEATHER         = ["Sunny", "Rainy", "Cloudy", "Windy"]
TRAFFIC         = ["Low", "Medium", "High"]

# ── Generator ────────────────────────────────────────────────────────────────
def generate_food_delivery_data(n: int) -> pd.DataFrame:
    start_date = datetime(2023, 1, 1)
    records = []

    for i in range(1, n + 1):
        restaurant  = random.choice(RESTAURANTS)
        cuisine     = CUISINES[restaurant]
        city        = random.choice(CITIES)
        payment     = random.choice(PAYMENT_METHODS)
        weather     = random.choice(WEATHER)
        traffic     = random.choice(TRAFFIC)

        # Order date / time
        order_dt = start_date + timedelta(
            days=random.randint(0, 364),
            hours=random.randint(8, 23),
            minutes=random.randint(0, 59)
        )

        # Delivery time influenced by traffic & weather
        base_delivery = random.randint(20, 40)
        if traffic == "High":    base_delivery += random.randint(10, 20)
        if weather == "Rainy":   base_delivery += random.randint(5, 15)
        delivery_time = base_delivery

        # Order value with some outliers
        order_value = round(random.uniform(100, 800), 2)
        if random.random() < 0.05:
            order_value = round(random.uniform(1000, 2000), 2)

        discount     = round(random.uniform(0, 0.3) * order_value, 2)
        final_amount = round(order_value - discount, 2)
        delivery_fee = random.choice([0, 20, 30, 40, 50])
        rating       = round(random.uniform(2.0, 5.0), 1)

        # Cancellations slightly more likely in bad weather/high traffic
        cancel_prob = 0.1
        if traffic == "High" or weather == "Rainy":
            cancel_prob = 0.18
        roll = random.random()
        if roll < cancel_prob:
            status = "Cancelled"
        elif roll < cancel_prob + 0.03:
            status = "Pending"
        else:
            status = "Delivered"

        records.append({
            "Order_ID":         f"ORD{i:05d}",
            "Order_Date":       order_dt.strftime("%Y-%m-%d"),
            "Order_Time":       order_dt.strftime("%H:%M"),
            "Restaurant_Name":  restaurant,
            "Cuisine_Type":     cuisine,
            "City":             city,
            "Order_Value":      order_value,
            "Discount":         discount,
            "Delivery_Fee":     delivery_fee,
            "Final_Amount":     final_amount,
            "Payment_Method":   payment,
            "Delivery_Time_min":delivery_time,
            "Order_Status":     status,
            "Customer_Rating":  rating if status == "Delivered" else None,
            "Weather":          weather,
            "Traffic_Level":    traffic,
            "Day_of_Week":      order_dt.strftime("%A"),
            "Month":            order_dt.strftime("%B"),
            "Hour":             order_dt.hour,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_food_delivery_data(NUM_RECORDS)
    df.to_csv("data/food_delivery_data.csv", index=False)
    print(f"✅  Dataset generated: data/food_delivery_data.csv  ({len(df)} rows)")
    print(df.head(3).to_string())
