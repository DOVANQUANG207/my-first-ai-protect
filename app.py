import streamlit as st
import pandas as pd
import os

# 1. Cấu hình trang & SEO
st.set_page_config(page_title="CS2 AI Analytics", page_icon="📈", layout="wide")

# 2. Sidebar - Bộ lọc tìm kiếm
st.sidebar.header("🔍 Bộ Lọc Tìm Kiếm")
search_query = st.sidebar.text_input("Nhập tên hòm muốn tìm:", "")

# 3. Dữ liệu hình ảnh (Cập nhật thêm link ảnh)
case_images = {
    "Fracture Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ.png",
    "Recoil Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbA5KicLwJzwv3dKVH_jL7Swa2nkvaYK7vSkT9UuZZzjOqYrIin2VKwr0dtNmGnIdPBewc5aV6G_ADtl-_v15i76MmfzyYyvyVw5HffyA.png",
    "Dreams & Nightmares Case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png",
    "Snakebite Case": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbA5KicLwJzwv3dKVH_jL7Swa2nkvaYK7vSkT9UuZZzjOqYrIin2VKwr0dtNmGnIdPBewc5aV6G_ADtl-_v15i76MmfzyYyvyVw5HffyA/360fx360f",
    "Kilowatt Case": "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ/360fx360f"
}
default_img = "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQTG4rihLQZ0wvrAIT-1ysvngojlwLSiZe7SlDlX6ZQoieqSpYmhiQTi-1o_ZWryIYKXdQJsaAvUrwbvlLnpgpS_tcpLnXJg/360fx360f"

# 4. Giao diện chính
st.image("https://shared.fastly.steamstatic.com/store_images/730/capsule_616x353.jpg", use_container_width=True)
st.title("📊 CS2 Premium Dashboard & AI Forecast")

# 5. Xử lý dữ liệu
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(current_dir, 'data', 'cs2_cases_market.csv'))
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    
    # Tính năng tìm kiếm
    filtered_df = df[df['case_name'].str.contains(search_query, case=False)]

    # Hiển thị số lượng hòm đang tìm thấy
    st.write(f"Đang hiển thị {len(filtered_df)} hòm phù hợp.")

    # Hiển thị dạng lưới (Grid) - 4 hòm mỗi dòng
    cols_per_row = 4
    for i in range(0, len(filtered_df), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        for idx, (index, row) in enumerate(batch.iterrows()):
            with cols[idx]:
                img_url = case_images.get(row['case_name'], default_img)
                st.image(img_url, use_container_width=True)
                st.subheader(row['case_name'])
                st.metric("Giá hiện tại", f"${row['current_price']:.2f}", f"{row['roi_percent']:.1f}% ROI")

    # Biểu đồ tổng quan
    st.markdown("---")
    st.subheader("📈 Phân tích lợi nhuận tổng quát")
    st.bar_chart(filtered_df.set_index('case_name')['roi_percent'])

except Exception as e:
    st.error(f"Lỗi tải dữ liệu: {e}")
