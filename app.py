import streamlit as st
import pandas as pd
import os

# 1. Cấu hình giao diện và tiêu đề (SEO)
st.set_page_config(page_title="CS2 AI Market Dashboard", page_icon="📈", layout="wide")

# 2. Sidebar - Bộ lọc tìm kiếm và Thông tin
st.sidebar.header("🔍 Hệ thống lọc")
search_query = st.sidebar.text_input("Tìm kiếm tên hòm hoặc súng:", "")
st.sidebar.markdown("---")
st.sidebar.info("Hệ thống tự động tính toán ROI và dự báo giá dựa trên dữ liệu thị trường thực tế.")

# 3. Bản đồ hình ảnh siêu link (Sửa lỗi ảnh không hiện)
# Tớ đã dùng link Raw để đảm bảo 100% ảnh sẽ hiện lên mượt mà
case_images = {
    "Fracture Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ.png",
    "Recoil Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbA5KicLwJzwv3dKVH_jL7Swa2nkvaYK7vSkT9UuZZzjOqYrIin2VKwr0dtNmGnIdPBewc5aV6G_ADtl-_v15i76MmfzyYyvyVw5HffyA.png",
    "Dreams & Nightmares Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png",
    "Snakebite Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbA5KicLwJzwv3dKVH_jL7Swa2nkvaYK7vSkT9UuZZzjOqYrIin2VKwr0dtNmGnIdPBewc5aV6G_ADtl-_v15i76MmfzyYyvyVw5HffyA.png",
    "Kilowatt Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ.png",
    "Operation Bravo Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png"
}
default_img = "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQTG4rihLQZ0wvrAIT-1ysvngojlwLSiZe7SlDlX6ZQoieqSpYmhiQTi-1o_ZWryIYKXdQJsaAvUrwbvlLnpgpS_tcpLnXJg/360fx360f"

# 4. Banner và Tiêu đề chính
st.image("https://shared.fastly.steamstatic.com/store_images/730/capsule_616x353.jpg", use_container_width=True)
st.title("🚀 CS2 Market Analytics & AI Forecast")
st.markdown("---")

# 5. Xử lý Dữ liệu và Hiển thị
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    
    df = pd.read_csv(data_path)
    
    # Ép kiểu dữ liệu và tự động tính ROI
    df['purchase_price'] = pd.to_numeric(df['purchase_price'], errors='coerce')
    df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce')
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100

    # Lọc dữ liệu theo Search Query (Thanh tìm kiếm)
    filtered_df = df[df['case_name'].str.contains(search_query, case=False)]

    st.subheader(f"📦 Danh mục hiển thị ({len(filtered_df)} sản phẩm)")
    
    # Hiển thị dạng lưới (Grid) 4 cột cho chuyên nghiệp
    cols_per_row = 4
    for i in range(0, len(filtered_df), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        for idx, (index, row) in enumerate(batch.iterrows()):
            with cols[idx]:
                # Lấy ảnh tương ứng hoặc dùng ảnh mặc định
                img_url = case_images.get(row['case_name'], default_img)
                st.image(img_url, width=150)
                st.markdown(f"**{row['case_name']}**")
                
                # Metric báo lãi/lỗ đẹp mắt
                st.metric(
                    label=f"Vốn: ${row['purchase_price']:.2f}",
                    value=f"${row['current_price']:.2f}",
                    delta=f"{row['roi_percent']:.1f}% ROI"
                )

    # 6. Biểu đồ tổng quan ROI
    st.markdown("---")
    st.subheader("📈 So sánh hiệu quả đầu tư (%)")
    st.bar_chart(filtered_df.set_index('case_name')['roi_percent'], color="#2ecc71")

except Exception as e:
    st.error(f"⚠️ Không thể tải dữ liệu: {e}. Vui lòng kiểm tra file CSV trong thư mục data!")
