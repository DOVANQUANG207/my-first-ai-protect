import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from sklearn.linear_model import LinearRegression

def analyze_and_predict():
    print("--- STARTING AI DATA PIPELINE ---")
    
    # 1. Đường dẫn file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    
    try:
        # 2. Xử lý dữ liệu với Pandas
        df = pd.read_csv(file_path)
        df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
        df_sorted = df.sort_values(by='roi_percent', ascending=False)
        
        # 3. Machine Learning: Dự báo giá 6 tháng tới
        print("\n[AI Insights]: Predicting future prices using Linear Regression...")
        # Giả định thời gian từ lúc mua đến nay là 30 ngày (điểm 0 đến điểm 30)
        X_train = np.array([[0], [30]]) 
        future_time = np.array([[180]]) # 6 tháng sau
        
        predictions = []
        for index, row in df_sorted.iterrows():
            y_train = np.array([row['purchase_price'], row['current_price']])
            model = LinearRegression().fit(X_train, y_train)
            pred = model.predict(future_time)[0]
            predictions.append(max(0, pred)) # Đảm bảo giá không âm
        
        df_sorted['predicted_price_6m'] = predictions
        print(df_sorted[['case_name', 'current_price', 'predicted_price_6m']])

        # 4. Vẽ biểu đồ ROI hiện tại
        plt.figure(figsize=(10, 6))
        plt.bar(df_sorted['case_name'], df_sorted['roi_percent'], color='skyblue')
        plt.title('CS2 Investment ROI & AI Forecast Ready')
        plt.ylabel('ROI (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Lưu và hiển thị
        plt.savefig(os.path.join(current_dir, 'cs2_final_report.png'))
        print(f"\n=> Report image saved as 'cs2_final_report.png'")
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    analyze_and_predict()
