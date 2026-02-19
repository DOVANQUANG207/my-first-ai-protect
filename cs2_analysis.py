import pandas as pd

try:
    df = pd.read_csv('data/cs2_cases_market.csv')
    
    df['profit_usd'] = df['current_price'] - df['purchase_price']
    df['roi_percent'] = (df['profit_usd'] / df['purchase_price']) * 100
    
    df_sorted = df.sort_values(by='roi_percent', ascending=False)
    
    print("--- BÁO CÁO PHÂN TÍCH ĐẦU TƯ CS2 ---")
    print(df_sorted[['case_name', 'purchase_price', 'current_price', 'roi_percent']])
    
    best_case = df_sorted.iloc[0]
    print(f"\n=> Hòm đáng đầu tư nhất: {best_case['case_name']} với mức lãi {best_case['roi_percent']:.2f}%")

except FileNotFoundError:
    print("Lỗi: Không tìm thấy file data/cs2_cases_market.csv. Hãy kiểm tra lại thư mục data!")
