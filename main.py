import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ✅ Initialize Session State for Data Storage
if "machines_data" not in st.session_state:
    st.session_state["machines_data"] = pd.DataFrame(columns=["Machine Code", "Machine Name", "Country", "Customer", "Price", "Last Order No", "Supplier"])

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

# ✅ Home Page
if menu == "Home":
    st.markdown("""<h1 class='title'>Bonhoeffer Machine Tracker</h1>""", unsafe_allow_html=True)
    st.image("https://source.unsplash.com/1600x900/?factory,machine", use_container_width=True)

# ✅ Order Tab
elif menu == "Order":
    st.title("Upload Order Data")
    uploaded_order = st.file_uploader("Upload Order File (Excel/CSV)", type=["xlsx", "csv"], key="order_upload")
    if uploaded_order is not None:
        df_order = pd.read_excel(uploaded_order, engine="openpyxl") if uploaded_order.name.endswith(".xlsx") else pd.read_csv(uploaded_order)
        st.session_state["machines_data"] = pd.concat([st.session_state["machines_data"], df_order], ignore_index=True)
        st.success("Order Data Uploaded Successfully!")
        st.dataframe(st.session_state["machines_data"])

# ✅ Upload Data Tab
elif menu == "Upload Data":
    st.title("Upload Machine & Spare Part Prices")
    uploaded_price = st.file_uploader("Upload Price Data", type=["xlsx", "csv"], key="price_upload")
    if uploaded_price is not None:
        df_price = pd.read_excel(uploaded_price, engine="openpyxl") if uploaded_price.name.endswith(".xlsx") else pd.read_csv(uploaded_price)
        st.session_state["machines_data"] = pd.concat([st.session_state["machines_data"], df_price], ignore_index=True)
        st.success("Price Data Uploaded Successfully!")
        st.dataframe(st.session_state["machines_data"])

# ✅ View Data Tab
elif menu == "View Data":
    st.title("View Machine & Spare Part Data")
    st.write("### Total Machines & Codes")
    st.dataframe(st.session_state["machines_data"])

# ✅ Analytics Tab
elif menu == "Analytics":
    st.title("Analytics Dashboard")
    
    # ✅ Refresh Button for Live Updates
    st.button("Refresh Analytics", on_click=st.cache_data.clear)
    
    # ✅ Fetch Data from Session
    df_chart = st.session_state["machines_data"]
    
    if not df_chart.empty and "Country" in df_chart.columns and "Price" in df_chart.columns:
        df_grouped = df_chart.groupby("Country")["Price"].sum().reset_index()

        # ✅ Pie Chart with Values
        fig_pie = go.Figure(data=[
            go.Pie(labels=df_grouped["Country"], values=df_grouped["Price"], hole=0.3, textinfo='label+percent+value')
        ])
        fig_pie.update_layout(title_text="Shipment Distribution by Country")

        # ✅ Bar Chart
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_grouped["Country"],
            y=df_grouped["Price"],
            marker=dict(color="blue"),
            text=df_grouped["Price"],
            textposition="outside"
        ))
        fig_bar.update_layout(
            title="Total Shipment Value by Country",
            xaxis_title="Country",
            yaxis_title="Total Price (USD)",
            template="plotly_dark",
            font=dict(size=14),
            margin=dict(l=40, r=40, t=40, b=40),
            height=500
        )

        # ✅ Show Charts
        st.plotly_chart(fig_pie, use_container_width=True)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No valid data available for analytics. Please upload data first!")

# ✅ Filter Data Tab
elif menu == "Filter Data":
    st.title("Filter Machine Prices & Suppliers")
    uploaded_filter = st.file_uploader("Upload File (Code, Country, Client)", type=["xlsx", "csv"], key="filter_upload")
    if uploaded_filter is not None:
        df_filter = pd.read_excel(uploaded_filter, engine="openpyxl") if uploaded_filter.name.endswith(".xlsx") else pd.read_csv(uploaded_filter)
        st.success("Filter Data Uploaded Successfully!")
        st.dataframe(df_filter)
