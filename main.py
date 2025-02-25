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

