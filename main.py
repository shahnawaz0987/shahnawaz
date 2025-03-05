import streamlit as st
import sqlite3

# Display Background Image (Ensure the image exists in your directory)

# Database Connection
def connect_db():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT NOT NULL,
                        price REAL NOT NULL,
                        available TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        items TEXT NOT NULL,
                        total_price REAL NOT NULL,
                        status TEXT NOT NULL DEFAULT 'Pending'
                    )''')
    conn.commit()
    return conn, cursor

# Function to get menu items
def get_menu_items():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM menu")
    data = cursor.fetchall()
    conn.close()
    return data

# Function to place an order
def place_order(items, total_price):
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO orders (items, total_price) VALUES (?, ?)", (items, total_price))
    conn.commit()
    conn.close()

# Function to add a menu item
def add_menu_item(name, category, price, available):
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO menu (name, category, price, available) VALUES (?, ?, ?, ?)", (name, category, price, available))
    conn.commit()
    conn.close()

# Function to delete a menu item
def delete_menu_item(item_id):
    conn, cursor = connect_db()
    cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# Function to update a menu item
def update_menu_item(item_id, name, category, price, available):
    conn, cursor = connect_db()
    cursor.execute("UPDATE menu SET name=?, category=?, price=?, available=? WHERE id=?", (name, category, price, available, item_id))
    conn.commit()
    conn.close()

# Streamlit Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Menu", "Place Order", "Order Status"])

def update_order_status(order_id, status):
    conn, cursor = connect_db()
    cursor.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()
    conn.close()


if page == "Home":
    st.title("🏠 Welcome to Sukkur Delight")
    st.write("### 🍽️ Sukkur Delight - Restaurant & Cafe")
    st.write("Manage your restaurant efficiently with our easy-to-use system.")
    st.image("background.jpg")

elif page == "Menu":
    st.title("🍽️ Restaurant Menu")
    menu_items = get_menu_items()
    if menu_items:
        for item in menu_items:
            st.write(f"**{item[1]}** ({item[2]}) - ${item[3]:.2f} [{item[4]}]")
    else:
        st.write("No menu items available.")

    st.subheader("Manage Menu")
    with st.form("menu_form"):
        name = st.text_input("Item Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0, format="%.2f")
        available = st.selectbox("Availability", ["Yes", "No"])
        submitted = st.form_submit_button("Add Item")
        if submitted:
            add_menu_item(name, category, price, available)
            st.success("Menu item added successfully!")

    item_id = st.number_input("Enter Item ID to Delete", min_value=1, format="%d")
    if st.button("Delete Item"):
        delete_menu_item(item_id)
        st.success("Menu item deleted!")

    st.subheader("Update Menu Item")
    update_id = st.number_input("Enter Item ID to Update", min_value=1, max_value=5000, format="%d")
    new_name = st.text_input("New Name")
    new_category = st.text_input("New Category")
    new_price = st.number_input("New Price", min_value=0.0, format="%.2f")
    new_available = st.selectbox("New Availability", ["Yes", "No"])
    if st.button("Update Item"):
        update_menu_item(update_id, new_name, new_category, new_price, new_available)
        st.success("Menu item updated!")

elif page == "Place Order":
    st.title("🛒 Place an Order")
    menu_items = get_menu_items()
    order_items = st.multiselect("Select Items", [item[1] for item in menu_items])
    total_price = sum([item[3] for item in menu_items if item[1] in order_items])
    if st.button("Place Order"):
        if order_items:
            place_order(", ".join(order_items), total_price)
            st.success("Order placed successfully!")
        else:
            st.warning("Please select at least one item.")

elif page == "Order Status":
    st.title("📌 Update Order Status")
    order_id = st.number_input("Enter Order ID", min_value=1, format="%d")
    status = st.selectbox("Update Status", ["Pending", "Completed"])
    if st.button("Update Status"):
        update_order_status(order_id, status)
        st.success("Order status updated!")



# Initialize Database
connect_db()
