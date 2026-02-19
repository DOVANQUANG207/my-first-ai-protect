import pandas as pd

def analyze_cs2_market():
    print("Initializing CS2 Market Analysis...")
    try:
        # 1. Đọc dữ liệu từ thư mục data
        df = pd.read_csv('data/cs2_cases_market.csv')
        
        # 2. Tính toán Lợi nhuận (Profit) và Tỉ suất ROI
        df['profit_usd'] = df['current_price'] - df['purchase_price']
        df['roi_percent'] = (df['profit_usd'] / df['purchase_price']) * 100
        
        # 3. Sắp xếp danh sách từ lãi cao nhất đến thấp nhất
        df_sorted = df.sort_values(by='roi_percent', ascending=False)
        
        # 4. In ra báo cáo
        print("\n--- CS2 MARKET ANALYSIS REPORT ---")
        print(df_sorted[['case_name', 'purchase_price', 'current_price', 'roi_percent']])
        
        # Tìm hòm lãi nhất
        best_case = df_sorted.iloc[0]
        print(f"\n=> TOP RECOMMENDATION: Invest in '{best_case['case_name']}' with a massive ROI of {best_case['roi_percent']:.2f}%!")
        
    except FileNotFoundError:
        print("Error: Could not find 'data/cs2_cases_market.csv'. Please check the folder structure.")

if __name__ == "__main__":
    analyze_cs2_market()
