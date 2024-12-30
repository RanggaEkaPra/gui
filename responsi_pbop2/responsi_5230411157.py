# database.py
import mysql.connector

class Database:
    def __init__(self):
        """Initialize the database connection."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="responsi_5230411157"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database connected successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.conn = None
            self.cursor = None

    def execute_query(self, query, params=None):
        """Helper function to execute a query and handle exceptions."""
        if self.conn is None:
            print("Connection is not established.")
            return None
        
        try:
            self.cursor.execute(query, params or ())

            # Ensure to fetch all results before executing another query
            if query.lower().startswith("select"):
                return self.cursor.fetchall()  # Immediately fetch results for SELECT queries
            else:
                self.conn.commit()  # Commit changes for non-SELECT queries
                return self.cursor  # Return cursor for non-SELECT queries
        except mysql.connector.Error as err:
            print(f"Query failed: {err}")
            return None

    def add_product_to_db(self, name, price):
        """Add a product to the database."""
        query = "INSERT INTO produk (nama_produk, harga) VALUES (%s, %s)"
        result = self.execute_query(query, (name, price))
        if result:
            return self.cursor.lastrowid

    def update_product_in_db(self, product_id, name, price):
        """Update an existing product's details."""
        query = "UPDATE produk SET nama_produk = %s, harga = %s WHERE id = %s"
        self.execute_query(query, (name, price, product_id))

    def delete_product_from_db(self, product_name):
        """Delete a product from the database."""
        query = "DELETE FROM produk WHERE nama_produk = %s"
        self.execute_query(query, (product_name,))

    def get_products_from_db(self):
        """Fetch all products from the database."""
        query = "SELECT id, nama_produk, harga FROM produk"  # Correct column names
        result = self.execute_query(query)
        if result:
            return result  # Already fetched by execute_query
        return []  # Return an empty list if result is None

    def add_transaction_to_db(self, product_id, quantity, total_price, transaction_date):
        """Add a transaction to the database."""
        query = """INSERT INTO transaksi (id_produk, jumlah, total_harga, tanggal_transaksi)
                   VALUES (%s, %s, %s, %s)"""
        self.execute_query(query, (product_id, quantity, total_price, transaction_date))

    def close_connection(self):
        """Close the database connection."""
        if self.cursor and self.conn:
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")
        else:
            print("No connection to close.")
