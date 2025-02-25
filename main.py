import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_option_menu import option_menu

# Database setup
conn = sqlite3.connect("machines.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS machines (
                machine_code TEXT PRIMARY KEY,
                machine_name_en TEXT,
                machine_name_es TEXT,
                country TEXT,
                customer TEXT,
                price REAL,
                last_order_no TEXT,
                supplier TEXT)''')
conn.commit()

# Streamlit Page Config with Background
st.set_page_config(page_title="Bonhoeffer Machine Tracker", layout="wide")
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #ffffff;
        background: -webkit-linear-gradient(left, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation with Icons
with st.sidebar:
    menu = option_menu("Main Menu", ["Home", "Order", "Upload Data", "View Data", "Analytics", "Filter Data"],
                       icons=["house", "file-earmark-spreadsheet", "cloud-upload", "table", "bar-chart", "filter"],
                       menu_icon="cast", default_index=0)

# Home Page
if menu == "Home":
    st.markdown("""<h1 class='title'>Bonhoeffer Machine Tracker</h1>""", unsafe_allow_html=True)
    st.image("https://source.unsplash.com/1600x900/?factory,machine", use_container_width=True)

# Order Tab
elif menu == "Order":
    st.title("Upload Order Data")
    uploaded_order = st.file_uploader("Upload Order File (Excel/CSV)", type=["xlsx", "csv"], key="order_upload")
    if uploaded_order is not None:
        df_order = pd.read_excel(uploaded_order, engine="openpyxl") if uploaded_order.name.endswith(".xlsx") else pd.read_csv(uploaded_order)
        st.success("Order Data Uploaded Successfully!")
        st.dataframe(df_order)

# Upload Data Tab
elif menu == "Upload Data":
    st.title("Upload Machine & Spare Part Prices")
    uploaded_price = st.file_uploader("Upload Price Data", type=["xlsx", "csv"], key="price_upload")
    if uploaded_price is not None:
        df_price = pd.read_excel(uploaded_price, engine="openpyxl") if uploaded_price.name.endswith(".xlsx") else pd.read_csv(uploaded_price)
        st.success("Price Data Uploaded Successfully!")
        st.dataframe(df_price)

# View Data Tab
elif menu == "View Data":
    st.title("View Machine & Spare Part Data")
    st.write("### Total Machines & Codes")
    c.execute("SELECT machine_code, machine_name_en FROM machines")
    machines = c.fetchall()
    st.dataframe(pd.DataFrame(machines, columns=["Machine Code", "Machine Name"]))

# Analytics Tab
elif menu == "Analytics":
    st.title("Analytics Dashboard")
    st.write("### Current Month Shipments vs Planned")
    c.execute("SELECT country, SUM(price) FROM machines GROUP BY country")
    data = c.fetchall()
    if data:
        df_chart = pd.DataFrame(data, columns=["Country", "Total Value"])
        fig = px.bar(df_chart, x="Country", y="Total Value", title="Total Shipment Value by Country", color="Total Value", color_continuous_scale="blues")
        st.plotly_chart(fig, use_container_width=True)

# Filter Data Tab
elif menu == "Filter Data":
    st.title("Filter Machine Prices & Suppliers")
    uploaded_filter = st.file_uploader("Upload File (Code, Country, Client)", type=["xlsx", "csv"], key="filter_upload")
    if uploaded_filter is not None:
        df_filter = pd.read_excel(uploaded_filter, engine="openpyxl") if uploaded_filter.name.endswith(".xlsx") else pd.read_csv(uploaded_filter)
        st.success("Filter Data Uploaded Successfully!")
        st.dataframe(df_filter)

conn.close()
