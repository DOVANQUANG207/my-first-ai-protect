import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_cs2_market():
    print("Initializing CS2 Market Analysis & Visualization...")
    
    # 1. Xử lý đường dẫn file thông minh
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    
    try:
        # 2. Đọc dữ liệu
        df = pd.read_csv(file_path)
        
        # 3. Tính toán ROI
        df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
        df_sorted = df.sort_values(by='roi_percent', ascending=False)
        
        # 4. In báo cáo ra Terminal
        print("\n--- CS2 MARKET REPORT ---")
        print(df_sorted[['case_name', 'purchase_price', 'current_price', 'roi_percent']])
        
        # 5. VẼ BIỂU ĐỒ
        plt.figure(figsize=(10, 6))
        plt.bar(df_sorted['case_name'], df_sorted['roi_percent'], color='skyblue')
        plt.xlabel('Case Name')
        plt.ylabel('ROI (%)')
        plt.title('CS2 Cases Investment Returns (ROI)')
        plt.xticks(rotation=45)
        
        # Lưu biểu đồ thành file ảnh
        plt.tight_layout()
        chart_path = os.path.join(current_dir, 'cs2_roi_chart.png')
        plt.savefig(chart_path)
        print(f"\n=> Success: Chart saved at {chart_path}")
        
        # Hiển thị biểu đồ
        plt.show()
        
    except FileNotFoundError:
        print(f"Error: Not found at {file_path}. Check your 'data' folder!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    analyze_cs2_market()
