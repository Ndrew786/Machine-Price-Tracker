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
                last_order_no TEXT)''')
conn.commit()

# Streamlit Page Config
st.set_page_config(page_title="Machine Price Tracker", layout="wide")

# Sidebar Navigation with Icons
with st.sidebar:
    menu = option_menu("Main Menu", ["Home", "Upload Data", "View Data", "Analytics"],
                       icons=["house", "cloud-upload", "table", "bar-chart"],
                       menu_icon="cast", default_index=0)

# Home Page
if menu == "Home":
    st.markdown("""
    <h1 style='text-align: center;'>Welcome to Machine Price Tracker</h1>
    <p style='text-align: center;'>Easily manage and analyze machine pricing data.</p>
    """, unsafe_allow_html=True)
    st.image("https://source.unsplash.com/1600x900/?factory,machine", use_column_width=True)

# Upload Data Page
elif menu == "Upload Data":
    st.title("Upload Excel or CSV File")
    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=["xlsx", "csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file, engine="openpyxl") if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
            df.columns = df.columns.str.strip().str.lower()
            required_columns = ["machine code", "machine name en", "machine name es", "country", "customer", "price", "last order no"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing columns in file: {missing_columns}")
            else:
                st.success("File uploaded successfully!")
                st.dataframe(df.style.set_properties(**{'background-color': '#f0f2f6', 'border': '1px solid black'}))
                for _, row in df.iterrows():
                    c.execute("INSERT OR IGNORE INTO machines VALUES (?, ?, ?, ?, ?, ?, ?)", tuple(row))
                conn.commit()
                st.success("Data processed successfully!")
        except Exception as e:
            st.error(f"Error reading file: {e}")

# View Data Page
elif menu == "View Data":
    st.title("View Machines Data")
    country_filter = st.text_input("Enter country to fetch prices")
    customer_filter = st.text_input("Enter customer to fetch prices")
    if st.button("Fetch Prices"):
        query = "SELECT * FROM machines WHERE country = ? AND customer = ?"
        c.execute(query, (country_filter, customer_filter))
        result = c.fetchall()
        if result:
            df_result = pd.DataFrame(result, columns=["Machine Code", "Machine Name EN", "Machine Name ES", "Country", "Customer", "Price", "Last Order No"])
            st.dataframe(df_result.style.format({"Price": "${:,.2f}"}).set_properties(**{'border': '1px solid black'}))
        else:
            st.warning("No records found for the given filters.")

# Analytics Page
elif menu == "Analytics":
    st.title("Analytics Dashboard")
    c.execute("SELECT country, AVG(price) FROM machines GROUP BY country")
    data = c.fetchall()
    if data:
        df_chart = pd.DataFrame(data, columns=["Country", "Avg Price"])
        fig = px.bar(df_chart, x="Country", y="Avg Price", title="Average Machine Price by Country",
                     color="Avg Price", color_continuous_scale="blues")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for analytics.")

conn.close()

import streamlit as st
import pandas as pd
import sqlite3
import sqlite3
conn = sqlite3.connect(":memory:")  # In-memory database for Streamlit Cloud
import pandas as pd
import streamlit as st

# Excel file read karte waqt openpyxl ka use karo
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")  # 🔥 Fix applied
        else:
            df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:", df)
    except Exception as e:
        st.error(f"Error reading file: {e}")


# Database setup
conn = sqlite3.connect("machines.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS machines (
                machine_code TEXT PRIMARY KEY,
                machine_name_en TEXT,
                machine_name_es TEXT,
                country TEXT,
                customer TEXT,
                price REAL,
                last_order_no TEXT)''')
conn.commit()

# Streamlit UI
def main():
    st.title("Machine Price Tracker & Order Manager")

    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=["xlsx", "csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
            st.write("Uploaded Data:", df)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return

        for _, row in df.iterrows():
            try:
                machine_code, machine_name_en, machine_name_es, country, customer, price, last_order_no = (
                    row["Machine Code"], row["Machine Name EN"], row["Machine Name ES"],
                    row["Country"], row["Customer"], row["Price"], row["Last Order No"]
                )

                c.execute("SELECT * FROM machines WHERE machine_code = ?", (machine_code,))
                data = c.fetchone()

                if data is None:
                    if pd.isna(price):
                        price = st.number_input(f"Enter price for {machine_name_en} ({country}, {customer})", min_value=0.0)
                    c.execute("INSERT INTO machines VALUES (?, ?, ?, ?, ?, ?, ?)", 
                              (machine_code, machine_name_en, machine_name_es, country, customer, price, last_order_no))
                else:
                    st.write(f"Machine {machine_name_en} already exists.")
            except KeyError as e:
                st.error(f"Missing column in file: {e}")
                return

        conn.commit()
        st.success("Data processed successfully!")

    country_filter = st.text_input("Enter country to fetch prices")
    customer_filter = st.text_input("Enter customer to fetch prices")

    if st.button("Fetch Prices"):
        query = "SELECT * FROM machines WHERE country = ? AND customer = ?"
        c.execute(query, (country_filter, customer_filter))
        result = c.fetchall()
        if result:
            st.write(pd.DataFrame(result, columns=["Machine Code", "Machine Name EN", "Machine Name ES", "Country", "Customer", "Price", "Last Order No"]))
        else:
            st.warning("No records found for the given filters.")

if __name__ == "__main__":
    main()
    conn.close()

