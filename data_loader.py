import pandas as pd

def load_raw_data():
    orders = pd.read_csv(r"C:\Users\agogo\Desktop\Business dashboard\E-commerce_sales_dashboard\data\raw\archive (6)\olist_orders_dataset.csv")
    order_items = pd.read_csv(r"C:\Users\agogo\Desktop\Business dashboard\E-commerce_sales_dashboard\data\raw\archive (6)\olist_order_items_dataset.csv")
    products = pd.read_csv(r"C:\Users\agogo\Desktop\Business dashboard\E-commerce_sales_dashboard\data\raw\archive (6)\olist_products_dataset.csv")
    customers = pd.read_csv(r"C:\Users\agogo\Desktop\Business dashboard\E-commerce_sales_dashboard\data\raw\archive (6)\olist_customers_dataset.csv")
    product_category_name_translation = pd.read_csv(r"C:\Users\agogo\Desktop\Business dashboard\E-commerce_sales_dashboard\data\raw\archive (6)\product_category_name_translation.csv")

    return orders, order_items, products, customers, product_category_name_translation


