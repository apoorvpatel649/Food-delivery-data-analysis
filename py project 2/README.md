# 🍕 Food Delivery Data Analysis
### College Project | Python | Data Analysis & Visualization

---

## 📁 Project Structure

```
food_delivery_analysis/
│
├── data/                          ← Auto-created on first run
│   └── food_delivery_data.csv     ← Generated dataset (1000 rows)
│
├── charts/                        ← Auto-created, all PNG charts saved here
│
├── generate_dataset.py            ← Script to create the dataset
├── food_delivery_analysis.py      ← Main analysis script (run in VS Code)
├── Food_Delivery_Analysis.ipynb   ← Jupyter Notebook version (recommended)
├── requirements.txt               ← Python dependencies
└── README.md                      ← This file
```

---

## 🚀 How to Run (VS Code)

### Step 1 – Install Dependencies
Open VS Code terminal (`Ctrl + ~`) and run:
```bash
pip install -r requirements.txt
```

### Step 2 – Run the Analysis (Option A: Python Script)
```bash
python food_delivery_analysis.py
```
Charts will be saved automatically to the `charts/` folder.

### Step 3 – Run the Analysis (Option B: Jupyter Notebook ⭐ Recommended)
```bash
jupyter notebook Food_Delivery_Analysis.ipynb
```
Or install the **Jupyter** VS Code extension and open the `.ipynb` file directly.

---

## 📊 What's Included

| # | Analysis | Type |
|---|----------|------|
| 1 | Order Status Distribution | Pie Chart |
| 2 | Orders per Restaurant | Bar Chart |
| 3 | Revenue by Cuisine | Horizontal Bar |
| 4 | Monthly Order Trend | Line Chart |
| 5 | Orders by Hour of Day | Bar Chart |
| 6 | Delivery Time Distribution | Histogram + KDE |
| 7 | Delivery Time vs Traffic | Box Plot |
| 8 | Payment Method Usage | Donut Chart |
| 9 | Average Rating by Restaurant | Bar Chart |
| 10 | Correlation Heatmap | Heatmap |
| 11 | Revenue by City | Bar Chart |
| 12 | Orders by Day & Status | Grouped Bar Chart |

---

## 🔬 Statistical Analysis
- **T-Test** – Delivery time comparison: Low vs High traffic
- **Pearson Correlation** – Order value vs delivery time
- **Descriptive Statistics** – Mean, std, min, max, quartiles

---

## 📦 Dataset Features (19 Columns)

| Column | Description |
|--------|-------------|
| Order_ID | Unique order identifier |
| Order_Date | Date of order |
| Order_Time | Time of order |
| Restaurant_Name | Name of restaurant |
| Cuisine_Type | Type of cuisine |
| City | City of order |
| Order_Value | Original order amount (₹) |
| Discount | Discount applied (₹) |
| Delivery_Fee | Delivery charge (₹) |
| Final_Amount | Amount paid after discount (₹) |
| Payment_Method | Mode of payment |
| Delivery_Time_min | Delivery time in minutes |
| Order_Status | Delivered / Cancelled / Pending |
| Customer_Rating | Rating out of 5.0 |
| Weather | Weather condition |
| Traffic_Level | Low / Medium / High |
| Day_of_Week | Day of the order |
| Month | Month of the order |
| Hour | Hour of the order (24h) |

---

## 🛠 Technologies Used
- **Python 3.x**
- **Pandas** – Data manipulation
- **NumPy** – Numerical operations
- **Matplotlib** – Plotting
- **Seaborn** – Statistical visualization
- **SciPy** – Statistical tests
- **Jupyter Notebook** – Interactive analysis

---

*Project generated for college data analysis coursework.*
