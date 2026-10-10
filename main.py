import pandas as pd
import numpy as np

def main():
    print("--- Retail Sales Intelligence Booting ---\n")
    
    # 1. Load Data
    df = pd.read_csv('data/sales.csv')
    print(f"[SYSTEM] Initial raw data loaded. Shape: {df.shape}")
    
    # 2. Data Cleaning & Null Handling
    df = df.drop_duplicates(subset=['order_id'])
    
    # Force columns to numeric, replacing strings like 'abc' with NaN
    df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce')
    df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
    
    df = df.dropna(subset=['units_sold'])
    
    median_price = df['unit_price'].median()
    df['unit_price'] = df['unit_price'].fillna(median_price)
    
    print(f"[SYSTEM] Data cleaning complete. Final shape: {df.shape}\n")
    
    # 3. NumPy Revenue Calculations
    df['revenue'] = df['units_sold'] * df['unit_price']
    
    # Convert to NumPy arrays for explicit numerical operations as requested
    revenue_array = df['revenue'].to_numpy()
    units_array = df['units_sold'].to_numpy()
    
    total_revenue = np.sum(revenue_array)
    total_orders = len(df)
    aov = total_revenue / total_orders if total_orders > 0 else 0
    total_units = np.sum(units_array)
    
    # 4. Console Report - Global Metrics
    print("        BUSINESS METRICS SUMMARY        ")
    print(f"Total Revenue:         ${total_revenue:,.2f}")
    print(f"Average Order Value:   ${aov:,.2f}")
    print(f"Total Units Sold:      {total_units:,.0f}\n")
    
    # 5. Groupby & Business Insights
    print("--- Revenue by Category ---")
    cat_rev = df.groupby('category')['revenue'].sum().sort_values(ascending=False)
    for cat, rev in cat_rev.items():
        print(f"{cat:15} : ${rev:,.2f}")
        
    print("\n--- Top 3 Products by Revenue ---")
    prod_rev = df.groupby('product_name')['revenue'].sum().sort_values(ascending=False).head(3)
    for prod, rev in prod_rev.items():
        print(f"{prod:25} : ${rev:,.2f}")
        
    print("\n--- Regional Sales Performance ---")
    reg_rev = df.groupby('region')['revenue'].sum().sort_values(ascending=False)
    for reg, rev in reg_rev.items():
        print(f"{reg:10} : ${rev:,.2f}")

if __name__ == "__main__":
    main()