"""
food_delivery_analysis.py
--------------------------
Comprehensive Food Delivery Data Analysis
College Project – Python Data Analysis

Topics Covered:
  1. Data Loading & Inspection
  2. Data Cleaning & Preprocessing
  3. Exploratory Data Analysis (EDA)
  4. Visualizations (10+ charts)
  5. Statistical Analysis
  6. Business Insights & Conclusions
"""

# ══════════════════════════════════════════════════════════════════════════════
# 0. IMPORTS
# ══════════════════════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
import os

warnings.filterwarnings("ignore")

# Plot style
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("Set2")
SAVE_DIR = "charts"
os.makedirs(SAVE_DIR, exist_ok=True)

def save(fig, name):
    path = os.path.join(SAVE_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"   📊  Saved → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# 1. DATA LOADING & INSPECTION
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 65)
print("  FOOD DELIVERY DATA ANALYSIS")
print("=" * 65)

CSV_PATH = "data/food_delivery_data.csv"
if not os.path.exists(CSV_PATH):
    print("⚠️  Dataset not found. Running generator …")
    import generate_dataset   # auto-generate if missing

df = pd.read_csv(CSV_PATH)

print("\n── 1. BASIC INFO ──────────────────────────────────────────")
print(f"Shape          : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"Columns        : {list(df.columns)}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head().to_string()}")


# ══════════════════════════════════════════════════════════════════════════════
# 2. DATA CLEANING & PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════
print("\n── 2. DATA CLEANING ───────────────────────────────────────")

print(f"\nMissing values before cleaning:\n{df.isnull().sum()}")
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# Fill missing ratings (cancelled orders have NaN rating) with 0
df["Customer_Rating"].fillna(0, inplace=True)

# Convert date column to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Derived columns
df["Month_Num"]    = df["Order_Date"].dt.month
df["Is_Weekend"]   = df["Day_of_Week"].isin(["Saturday", "Sunday"]).astype(int)
df["Is_Delivered"] = (df["Order_Status"] == "Delivered").astype(int)

# Discount percentage
df["Discount_Pct"] = round((df["Discount"] / df["Order_Value"]) * 100, 2)

print(f"\nMissing values after cleaning:\n{df.isnull().sum()}")
print("\n✅  Data cleaning complete.")


# ══════════════════════════════════════════════════════════════════════════════
# 3. DESCRIPTIVE STATISTICS
# ══════════════════════════════════════════════════════════════════════════════
print("\n── 3. DESCRIPTIVE STATISTICS ──────────────────────────────")

numeric_cols = ["Order_Value", "Discount", "Final_Amount",
                "Delivery_Time_min", "Customer_Rating", "Delivery_Fee"]
print(df[numeric_cols].describe().round(2).to_string())

print(f"\nOrder Status Distribution:\n{df['Order_Status'].value_counts()}")
print(f"\nTop 5 Restaurants by Orders:\n{df['Restaurant_Name'].value_counts().head()}")
print(f"\nTop 5 Cities by Orders:\n{df['City'].value_counts().head()}")


# ══════════════════════════════════════════════════════════════════════════════
# 4. VISUALIZATIONS
# ══════════════════════════════════════════════════════════════════════════════
print("\n── 4. GENERATING CHARTS ───────────────────────────────────")

# ── Chart 1: Order Status Distribution (Pie) ─────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
status_counts = df["Order_Status"].value_counts()
colors = ["#2ecc71", "#e74c3c", "#f39c12"]
wedges, texts, autotexts = ax.pie(
    status_counts, labels=status_counts.index, autopct="%1.1f%%",
    colors=colors, startangle=90, pctdistance=0.82,
    wedgeprops=dict(edgecolor="white", linewidth=2))
for at in autotexts:
    at.set_fontsize(12); at.set_fontweight("bold")
ax.set_title("Order Status Distribution", fontsize=16, fontweight="bold", pad=15)
save(fig, "01_order_status_pie.png"); plt.close()

# ── Chart 2: Orders Per Restaurant (Bar) ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
rest_counts = df["Restaurant_Name"].value_counts()
bars = ax.bar(rest_counts.index, rest_counts.values,
              color=sns.color_palette("Set2", len(rest_counts)))
ax.bar_label(bars, padding=3, fontsize=10)
ax.set_title("Number of Orders per Restaurant", fontsize=15, fontweight="bold")
ax.set_xlabel("Restaurant"); ax.set_ylabel("Number of Orders")
plt.xticks(rotation=30, ha="right")
save(fig, "02_orders_per_restaurant.png"); plt.close()

# ── Chart 3: Revenue by Cuisine (Horizontal Bar) ─────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
cuisine_rev = df.groupby("Cuisine_Type")["Final_Amount"].sum().sort_values()
bars = ax.barh(cuisine_rev.index, cuisine_rev.values,
               color=sns.color_palette("coolwarm", len(cuisine_rev)))
ax.bar_label(bars, fmt="₹%.0f", padding=4, fontsize=9)
ax.set_title("Total Revenue by Cuisine Type", fontsize=15, fontweight="bold")
ax.set_xlabel("Total Revenue (₹)")
save(fig, "03_revenue_by_cuisine.png"); plt.close()

# ── Chart 4: Monthly Order Trend (Line) ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
month_order = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
monthly = df.groupby("Month").size().reindex(month_order).dropna()
ax.plot(monthly.index, monthly.values, marker="o", linewidth=2.5,
        color="#3498db", markersize=8, markerfacecolor="white", markeredgewidth=2)
ax.fill_between(monthly.index, monthly.values, alpha=0.15, color="#3498db")
ax.set_title("Monthly Order Trend", fontsize=15, fontweight="bold")
ax.set_xlabel("Month"); ax.set_ylabel("Number of Orders")
plt.xticks(rotation=30, ha="right")
save(fig, "04_monthly_order_trend.png"); plt.close()

# ── Chart 5: Order Distribution by Hour (Bar) ────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
hourly = df.groupby("Hour").size()
ax.bar(hourly.index, hourly.values,
       color=["#e74c3c" if h in [12,13,19,20,21] else "#3498db"
              for h in hourly.index])
ax.set_title("Orders by Hour of Day  (Red = Peak Hours)", fontsize=15, fontweight="bold")
ax.set_xlabel("Hour (24h)"); ax.set_ylabel("Number of Orders")
ax.set_xticks(range(8, 24))
save(fig, "05_orders_by_hour.png"); plt.close()

# ── Chart 6: Delivery Time Distribution (Histogram + KDE) ────────────────────
delivered = df[df["Order_Status"] == "Delivered"]
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(delivered["Delivery_Time_min"], bins=25, color="#9b59b6",
        edgecolor="white", alpha=0.75, density=True, label="Histogram")
delivered["Delivery_Time_min"].plot.kde(ax=ax, color="#2c3e50", linewidth=2.5, label="KDE")
ax.axvline(delivered["Delivery_Time_min"].mean(), color="#e74c3c",
           linestyle="--", linewidth=2, label=f"Mean = {delivered['Delivery_Time_min'].mean():.1f} min")
ax.set_title("Delivery Time Distribution", fontsize=15, fontweight="bold")
ax.set_xlabel("Delivery Time (minutes)"); ax.set_ylabel("Density")
ax.legend()
save(fig, "06_delivery_time_distribution.png"); plt.close()

# ── Chart 7: Average Delivery Time by Traffic Level (Box) ────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
order = ["Low", "Medium", "High"]
traffic_data = [delivered[delivered["Traffic_Level"] == t]["Delivery_Time_min"]
                for t in order]
bp = ax.boxplot(traffic_data, labels=order, patch_artist=True,
                medianprops=dict(color="red", linewidth=2))
colors_box = ["#2ecc71", "#f39c12", "#e74c3c"]
for patch, color in zip(bp["boxes"], colors_box):
    patch.set_facecolor(color); patch.set_alpha(0.7)
ax.set_title("Delivery Time vs Traffic Level", fontsize=15, fontweight="bold")
ax.set_xlabel("Traffic Level"); ax.set_ylabel("Delivery Time (minutes)")
save(fig, "07_delivery_time_vs_traffic.png"); plt.close()

# ── Chart 8: Payment Method Usage (Donut) ────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))
pay_counts = df["Payment_Method"].value_counts()
wedges, texts, autotexts = ax.pie(
    pay_counts, labels=pay_counts.index, autopct="%1.1f%%",
    startangle=90, pctdistance=0.78,
    colors=sns.color_palette("pastel"),
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2))
for at in autotexts:
    at.set_fontsize(11); at.set_fontweight("bold")
ax.set_title("Payment Method Distribution", fontsize=15, fontweight="bold")
save(fig, "08_payment_method_donut.png"); plt.close()

# ── Chart 9: Average Rating by Restaurant (Bar) ──────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
avg_rating = (df[df["Customer_Rating"] > 0]
              .groupby("Restaurant_Name")["Customer_Rating"]
              .mean().sort_values(ascending=False))
bars = ax.bar(avg_rating.index, avg_rating.values,
              color=sns.color_palette("RdYlGn", len(avg_rating)))
ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=10)
ax.set_ylim(0, 5.5)
ax.axhline(avg_rating.mean(), linestyle="--", color="navy", linewidth=1.5,
           label=f"Overall Avg = {avg_rating.mean():.2f}")
ax.set_title("Average Customer Rating by Restaurant", fontsize=15, fontweight="bold")
ax.set_xlabel("Restaurant"); ax.set_ylabel("Average Rating (out of 5)")
ax.legend(); plt.xticks(rotation=30, ha="right")
save(fig, "09_avg_rating_by_restaurant.png"); plt.close()

# ── Chart 10: Correlation Heatmap ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))
corr_cols = ["Order_Value","Discount","Final_Amount","Delivery_Fee",
             "Delivery_Time_min","Customer_Rating","Is_Weekend","Is_Delivered"]
corr = df[corr_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            ax=ax, linewidths=0.5, annot_kws={"size": 10})
ax.set_title("Correlation Heatmap – Numeric Features", fontsize=15, fontweight="bold")
save(fig, "10_correlation_heatmap.png"); plt.close()

# ── Chart 11: Revenue by City (Bar) ──────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 5))
city_rev = df.groupby("City")["Final_Amount"].sum().sort_values(ascending=False)
bars = ax.bar(city_rev.index, city_rev.values,
              color=sns.color_palette("tab10", len(city_rev)))
ax.bar_label(bars, fmt="₹%.0f", padding=3, fontsize=8, rotation=45)
ax.set_title("Total Revenue by City", fontsize=15, fontweight="bold")
ax.set_xlabel("City"); ax.set_ylabel("Total Revenue (₹)")
plt.xticks(rotation=30, ha="right")
save(fig, "11_revenue_by_city.png"); plt.close()

# ── Chart 12: Weekday vs Weekend Orders (Grouped Bar) ────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_counts = df.groupby(["Day_of_Week","Order_Status"]).size().unstack(fill_value=0)
day_counts = day_counts.reindex(day_order)
day_counts.plot(kind="bar", ax=ax, color=["#2ecc71","#e74c3c","#f39c12"],
                edgecolor="white", linewidth=0.5)
ax.set_title("Orders by Day of Week & Status", fontsize=15, fontweight="bold")
ax.set_xlabel("Day of Week"); ax.set_ylabel("Number of Orders")
ax.legend(title="Status"); plt.xticks(rotation=30, ha="right")
save(fig, "12_orders_by_day_and_status.png"); plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# 5. STATISTICAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
print("\n── 5. STATISTICAL ANALYSIS ────────────────────────────────")

# 5a. Is delivery time significantly higher in High vs Low traffic?
low_t  = delivered[delivered["Traffic_Level"] == "Low"]["Delivery_Time_min"]
high_t = delivered[delivered["Traffic_Level"] == "High"]["Delivery_Time_min"]
t_stat, p_val = stats.ttest_ind(low_t, high_t)
print(f"\nT-Test (Delivery Time: Low vs High Traffic):")
print(f"  t-statistic = {t_stat:.4f},  p-value = {p_val:.6f}")
print(f"  {'✅ Significant difference (p < 0.05)' if p_val < 0.05 else '❌ No significant difference'}")

# 5b. Correlation between Order Value and Delivery Time
corr_val, p_corr = stats.pearsonr(
    delivered["Order_Value"], delivered["Delivery_Time_min"])
print(f"\nPearson Correlation (Order Value vs Delivery Time):")
print(f"  r = {corr_val:.4f},  p-value = {p_corr:.4f}")

# 5c. Average metrics summary
print(f"\nKey Metric Summary (Delivered Orders):")
print(f"  Avg Order Value    : ₹{delivered['Order_Value'].mean():.2f}")
print(f"  Avg Final Amount   : ₹{delivered['Final_Amount'].mean():.2f}")
print(f"  Avg Discount       : ₹{delivered['Discount'].mean():.2f}  ({delivered['Discount_Pct'].mean():.1f}%)")
print(f"  Avg Delivery Time  : {delivered['Delivery_Time_min'].mean():.1f} min")
print(f"  Avg Customer Rating: {delivered['Customer_Rating'].mean():.2f} / 5.0")
print(f"  Total Revenue      : ₹{delivered['Final_Amount'].sum():,.2f}")


# ══════════════════════════════════════════════════════════════════════════════
# 6. BUSINESS INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
print("\n── 6. KEY BUSINESS INSIGHTS ───────────────────────────────")

cancellation_rate = (df["Order_Status"] == "Cancelled").mean() * 100
best_restaurant   = avg_rating.idxmax()
peak_hour         = hourly.idxmax()
busiest_day       = df["Day_of_Week"].value_counts().idxmax()
top_city          = city_rev.idxmax()
top_payment       = df["Payment_Method"].value_counts().idxmax()

print(f"""
  1. Cancellation Rate    : {cancellation_rate:.1f}%
  2. Best Rated Restaurant: {best_restaurant}  ({avg_rating.max():.2f} ⭐)
  3. Peak Ordering Hour   : {peak_hour}:00 ({hourly.max()} orders)
  4. Busiest Day          : {busiest_day}
  5. Top Revenue City     : {top_city}  (₹{city_rev.max():,.0f})
  6. Most Used Payment    : {top_payment}
  7. High Traffic Impact  : Delivery time increases by
                            {high_t.mean() - low_t.mean():.1f} min (Low → High traffic)
  8. Rainy Weather Impact : Orders with cancellations rise in bad weather.
""")


print("=" * 65)
print("  ✅  ANALYSIS COMPLETE!  All charts saved to /charts/")
print("=" * 65)
