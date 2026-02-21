import streamlit as st
import pandas as pd
import os

# 1. Cấu hình trang
st.set_page_config(page_title="CS2 AI Market Dashboard", page_icon="🚀", layout="wide")

# 2. Sidebar
st.sidebar.header("🔍 Hệ thống lọc")
search_query = st.sidebar.text_input("Tìm kiếm tên hòm hoặc súng:", "")
st.sidebar.info("Hệ thống tự động tính ROI và dự báo giá.")

# 3. KHO LINK ẢNH SIÊU ỔN ĐỊNH (Sửa lỗi ảnh không hiện)
case_images = {
    "fracture case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ.png",
    "recoil case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbA5KicLwJzwv3dKVH_jL7Swa2nkvaYK7vSkT9UuZZzjOqYrIin2VKwr0dtNmGnIdPBewc5aV6G_ADtl-_v15i76MmfzyYyvyVw5HffyA.png",
    "dreams & nightmares case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png",
    "snakebite case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png",
    "kilowatt case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1x1JgZk57TqLghpxlXwIytN_tHjl9KIlfD3J6jXxTgGvcZzi-2ZqI-njgTlqUdoMmvxcoTAdFRqZltLmXjQ.png",
    "operation bravo case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png",
    "clutch case": "https://raw.githubusercontent.com/SteamDatabase/SteamTracker/master/images/730/econ/item_images/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQbT5qirIgp1xgDIditH_tDigYmflfCIM7_UqXYDu5JxibCeqImijwTj-xY6Yjj1IYeWIQNpZF_X-AC2kOzo0MDv6p3AwXs3uSMqsyzE.png"
}
default_img = "https://community.cloudflare.steamstatic.com/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXU5A1PIYQNqhpOSV-fTPOo8zjVF1xwIQTG4rihLQZ0wvrAIT-1ysvngojlwLSiZe7SlDlX6ZQoieqSpYmhiQTi-1o_ZWryIYKXdQJsaAvUrwbvlLnpgpS_tcpLnXJg/360fx360f"

# 4. Giao diện chính
st.image("https://shared.fastly.steamstatic.com/store_images/730/capsule_616x353.jpg", use_container_width=True)
st.title("🚀 CS2 Market Analytics & AI Forecast")

# 5. Xử lý dữ liệu
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'cs2_cases_market.csv')
    df = pd.read_csv(data_path)
    
    # Tính ROI
    df['roi_percent'] = ((df['current_price'] - df['purchase_price']) / df['purchase_price']) * 100
    
    # Lọc theo tìm kiếm
    filtered_df = df[df['case_name'].str.contains(search_query, case=False)]
    st.subheader(f"📦 Danh mục hiển thị ({len(filtered_df)} sản phẩm)")

    # Hiển thị dạng lưới
    cols_per_row = 4
    for i in range(0, len(filtered_df), cols_per_row):
        cols = st.columns(cols_per_row)
        batch = filtered_df.iloc[i : i + cols_per_row]
        for idx, (index, row) in enumerate(batch.iterrows()):
            with cols[idx]:
                # CHỖ NÀY QUAN TRỌNG: Viết thường tên hòm để khớp với kho ảnh
                name_key = row['case_name'].lower().strip()
                img_url = case_images.get(name_key, default_img)
                
                st.image(img_url, width=150)
                st.markdown(f"**{row['case_name']}**")
                st.metric(f"Vốn: ${row['purchase_price']:.2f}", f"${row['current_price']:.2f}", f"{row['roi_percent']:.1f}% ROI")

except Exception as e:
    st.error(f"Lỗi: {e}")
