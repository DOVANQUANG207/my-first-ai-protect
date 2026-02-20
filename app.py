import streamlit as st
import pandas as pd
import os

# ==========================================
# 1. CẤU HÌNH TRANG & BANNER
# ==========================================
st.set_page_config(page_title="CS2 AI Dashboard", page_icon="🚀", layout="wide")

# Banner ổn định từ Steam Store
st.image("https://shared.fastly.steamstatic.com/store_images/730/capsule_616x353.jpg", use_container_width=True)

st.title("🚀 CS2 Market Analytics & AI Forecast")
st.markdown("Hệ thống tự động theo dõi, tính toán lợi nhuận và dự báo giá hòm CS2 bằng Machine Learning.")
st.markdown("---")

# ==========================================
# 2. ĐƯỜNG DẪN DỮ LIỆU & HÌNH ẢNH
# ==========================================
current_dir = os.path.dirname(os.path.abspath(__file__))
market_data_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
history_data_path = os.path.join(current_dir, 'data', 'price_history.csv')

# Link ảnh ổn định từ kho dữ liệu SteamDatabase trên GitHub (Chống lỗi 0)
case_images = {
    "Fracture Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ.png",
    "Recoil Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbA5KicLwJzwv3dKVH_jL7Swa2nkvaYK7vSkT9UuZZzjOqYrIin2VKwr0dtNmGnIdPBewc5aV6G_ADtl-_v15i76MmfzyYyvyVw5HffyA.png",
    "Dreams & Nightmares Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png"
}
default_img = "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQTG4rihLQZ0wvrAIT-1ysvngojlwLSiZe7SlDlX6ZQoieqSpYmhiQTi-1o_ZWryIYKXdQJsaAvUrwbvlLnpgpS_tcpLnXJg/360fx360f"

# ==========================================
# 3. XỬ LÝ & HIỂN THỊ DỮ LIỆU CHÍNH
# ==========================================
try:
    # Đọc dữ liệu
    df = pd.read_csv(market_data_path)
    
    # Ép kiểu dữ liệu và tự động tính ROI (Tránh lỗi thiếu cột roi_percent)
    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    
    st.subheader("📦 Showcase Danh Mục Hòm Trực Tiếp")
    
    # Tạo các cột bằng đúng số lượng hòm có trong file CSV
    cols = st.columns(len(df))
    
    for index, row in df.iterrows():
        with cols[index]:
            # Hiển thị ảnh (Nền trong suốt chuẩn đẹp)
            img_url = case_images.get(row['case_name'], default_img)
            
            # Khung chứa ảnh và thông tin
            st.image(img_url, width=150)
            st.markdown(f"**{row['case_name']}**")
            
            # Thẻ Metric xịn xò báo lãi/lỗ
            st.metric(
                label=f"Giá vốn: ${row['purchase_price']:.2f}", 
                value=f"${row['current_price']:.2f}", 
                delta=f"{row['roi_percent']:.2f}% ROI"
            )

    st.markdown("---")
    
    # ==========================================
    # 4. KHU VỰC TABS (BẢNG, BIỂU ĐỒ, LỊCH SỬ)
    # ==========================================
    tab1, tab2, tab3 = st.tabs(["📊 Bảng Dữ Liệu Chi Tiết", "📈 Biểu Đồ So Sánh Tăng Trưởng", "📉 Lịch sử Biến Động (Live)"])
    
    with tab1:
        st.info("Bảng dữ liệu trích xuất từ file CSV, đã được AI xử lý lại tỷ lệ lợi nhuận.")
        # Định dạng lại bảng cho đẹp
        display_df = df[['case_name', 'purchase_price', 'current_price', 'roi_percent']].copy()
        display_df['roi_percent'] = display_df['roi_percent'].round(2).astype(str) + '%'
        st.dataframe(display_df, use_container_width=True)
        
    with tab2:
        st.info("So sánh mức độ hiệu quả đầu tư (ROI) giữa các loại hòm.")
        chart_data = df.set_index('case_name')[['roi_percent']]
        st.bar_chart(chart_data, color="#2ecc71") # Màu xanh lá tài chính
        
    with tab3:
        if os.path.exists(history_data_path):
            st.success("Dữ liệu chuỗi thời gian (Time-series) đang được thu thập tốt!")
            h_df = pd.read_csv(history_data_path)
            
            # Đảm bảo cột price là dạng số
            h_df['price'] = pd.to_numeric(h_df['price'], errors='coerce')
            
            # Vẽ biểu đồ đường qua các mốc thời gian
            pivot_df = h_df.pivot(index='timestamp', columns='case_name', values='price')
            st.line_chart(pivot_df)
        else:
            st.warning("Chưa có dữ liệu lịch sử. Hãy chạy file `cs2_analysis.py` định kỳ để hệ thống tự động lưu vết giá!")

except Exception as e:
    st.error(f"⚠️ Hệ thống đang gặp gián đoạn: {e}")
    st.info("Vui lòng đảm bảo bạn đã tạo thư mục `data` và có chứa file `cs2_cases_market.csv` bên trong.") 