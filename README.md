# E-commerce Sales & Operations Dashboard

>🔗 **✅ Live app:** https://olist-e-commerce-sales-dashboard.streamlit.app/

An interactive dashboard built on **99,000+ real orders** from Olist, a Brazilian e-commerce marketplace. It's built for a **head of sales** who needs to decide where to invest next quarter, and who also needs to know whether operations (delivery, cancellations) are holding the business back.

## Business questions

1. **Is revenue growing, and when does it peak?**
2. **Which product categories actually drive the business?**
3. **Which regions are underperforming, and is late delivery part of the reason?**

## What the dashboard will show

- **Headline KPIs:** total revenue, number of orders, average order value, unique customers
- **Sales:** monthly revenue trend, top categories, revenue by state
- **Fulfilment health:** orders by status, cancellation rate, late-delivery rate and median delivery time by state
- **Filters:** date range, state, category
- **Insights:** 3 data-backed recommendations

## Early findings

- **Median delivery time: 10 days.** The average is 12 days because a few extreme delays (up to 209 days) pull it up, so the median is the fairer "typical delivery" number.
- **7.9% of delivered orders arrived after the promised date.**

## Data

Source: [Brazilian E-Commerce Public Dataset by Olist (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The raw files are not stored in this repo; download them from Kaggle into `data/raw/`.

5 tables used: `orders`, `order_items`, `products`, `customers`, `product_category_name_translation`.

### Data notes & cleaning decisions

- **Grain:** the main table has one row per item sold (112,650 rows). Orders are counted with unique `order_id`, never by row count.
- **Merges:** all merges are left joins starting from `order_items`. The row count was checked after every step to make sure no rows were dropped or duplicated.
- **Revenue = item price, excluding freight.** Freight is a shipping cost, not product sales. Freight is kept separately for the operations analysis.
- **Missing categories (1.4% of items):** 1,603 items had no category at all and are labelled `unknown`; 24 items had a category missing from the translation table and were translated manually.
- **Undelivered orders:** about 2,450 items have no delivery date (cancelled, shipped or still processing). They are excluded from delivery-time and late-rate calculations, so rates are computed "out of delivered orders".

## Project structure

```
├── data/
│   ├── raw/                 # Kaggle files (not committed)
│   └── processed/           # clean files used by the dashboard
│       ├── sales.csv        # one row per item sold
│       └── orders_status.csv  # one row per order (all statuses)
├── data_loader.py           # loads the raw tables and parses dates
├── 01_explore.ipynb         # first look at each table
├── 02_clean_merge.ipynb     # merge, clean, new columns, save processed files
└── 03_kpis.ipynb            # KPI calculations
```

## Tech stack

Python · pandas · Plotly · Streamlit · Git/GitHub

## Run it locally

```bash
pip install pandas plotly streamlit
streamlit run app.py   # once the app is added
```

---

Built by **Maty Traoré** · Big Data, AI & Management (Audencia × Centrale Nantes)
