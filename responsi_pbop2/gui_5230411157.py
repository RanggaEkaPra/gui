import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from responsi_5230411157 import Database
import openpyxl

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Produk dan Transaksi")
        self.db = Database()

        self.setup_gui()

    def setup_gui(self):
        # Frame Produk
        product_frame = ttk.LabelFrame(self.root, text="Manajemen Produk", padding="10")
        product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(product_frame, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.product_name_entry = ttk.Entry(product_frame)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(product_frame, text="Harga Produk:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.product_price_entry = ttk.Entry(product_frame)
        self.product_price_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(product_frame, text="Tambah Produk", command=self.add_product).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(product_frame, text="Hapus Produk", command=self.delete_product).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(product_frame, text="Edit Produk", command=self.edit_product).grid(row=2, column=2, padx=5, pady=5)

        self.product_listbox = tk.Listbox(product_frame, height=10)
        self.product_listbox.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        # Frame Transaksi
        transaction_frame = ttk.LabelFrame(self.root, text="Proses Transaksi", padding="10")
        transaction_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(transaction_frame, text="Pilih Produk:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.product_combobox = ttk.Combobox(transaction_frame, state="readonly")
        self.product_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(transaction_frame, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(transaction_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(transaction_frame, text="Tambah Transaksi", command=self.add_transaction).grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.transaction_tree = ttk.Treeview(transaction_frame, columns=("Nama Produk", "Harga", "Jumlah", "Total Harga", "Tanggal"), show="headings")
        self.transaction_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.transaction_tree.heading("Nama Produk", text="Nama Produk")
        self.transaction_tree.heading("Harga", text="Harga")
        self.transaction_tree.heading("Jumlah", text="Jumlah")
        self.transaction_tree.heading("Total Harga", text="Total Harga")
        self.transaction_tree.heading("Tanggal", text="Tanggal")

        ttk.Button(self.root, text="Export ke Excel", command=self.export_to_excel).grid(row=1, column=0, columnspan=2, pady=10)

        self.update_product_list()

    def add_product(self):
        name = self.product_name_entry.get()
        price = self.product_price_entry.get()

        if not name or not price:
            messagebox.showerror("Error", "Nama dan harga produk harus diisi!")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Harga harus berupa angka!")
            return

        self.db.add_product_to_db(name, price)
        self.update_product_list()

    def edit_product(self):
        selected = self.product_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Pilih produk yang ingin diedit!")
            return

        index = selected[0]
        product_name = self.product_listbox.get(index).split(" - ")[0]
        product_price = self.product_listbox.get(index).split(" - ")[1].strip()[3:]  # Strip "Rp "

        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.insert(0, product_name)
        self.product_price_entry.delete(0, tk.END)
        self.product_price_entry.insert(0, product_price)

        # Modify the update function directly
        def update_product():
            name = self.product_name_entry.get()
            price = self.product_price_entry.get()

            if not name or not price:
                messagebox.showerror("Error", "Nama dan harga produk harus diisi!")
                return

            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Harga harus berupa angka!")
                return

            product_id = self.products[index]['id']
            self.db.update_product_in_db(product_id, name, price)
            self.update_product_list()
            messagebox.showinfo("Sukses", f"Produk '{name}' berhasil diperbarui!")

        # Reuse the existing button for update functionality
        self.update_product_button = ttk.Button(self.root, text="Update Produk", command=update_product)
        self.update_product_button.grid(row=3, column=2, padx=5, pady=5)

    def delete_product(self):
        selected = self.product_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Pilih produk yang ingin dihapus!")
            return

        index = selected[0]
        product_name = self.product_listbox.get(index).split(" - ")[0]
        self.db.delete_product_from_db(product_name)
        self.update_product_list()

    def update_product_list(self):
        self.product_listbox.delete(0, tk.END)
        self.products = self.db.get_products_from_db()
        for product in self.products:
            self.product_listbox.insert(tk.END, f"{product['nama_produk']} - Rp {product['harga']:.2f}")
        
        # Update the combobox as well
        self.update_product_combobox()

    def update_product_combobox(self):
        # Ensure the combobox gets the updated product names
        self.product_combobox['values'] = [product['nama_produk'] for product in self.products]
        if self.products:  # If there are products, select the first one by default
            self.product_combobox.current(0)

    def add_transaction(self):
        product_name = self.product_combobox.get()
        quantity = self.quantity_entry.get()

        if not product_name or not quantity:
            messagebox.showerror("Error", "Pilih produk dan masukkan jumlah!")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return

        if quantity <= 0:  # Check if quantity is 0 or negative
            messagebox.showerror("Error", "Jumlah tidak boleh 0 atau negatif!")
            return

        # Find the product based on the selected name
        product = next((p for p in self.products if p['nama_produk'] == product_name), None)
        if not product:
            messagebox.showerror("Error", "Produk tidak ditemukan!")
            return

        # Calculate the total price of the transaction
        total_price = product['harga'] * quantity
        transaction_date = date.today().strftime('%Y-%m-%d')

        # Add the transaction to the database
        self.db.add_transaction_to_db(product['id'], quantity, total_price, transaction_date)

        # Insert the transaction into the Treeview
        self.transaction_tree.insert("", tk.END, values=(product_name, f"Rp {product['harga']:.2f}", quantity, f"Rp {total_price:.2f}", transaction_date))
        self.quantity_entry.delete(0, tk.END)

    def export_to_excel(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Data Transaksi"

        sheet.append(["Nama Produk", "Harga", "Jumlah", "Total Harga", "Tanggal"])

        for child in self.transaction_tree.get_children():
            sheet.append(self.transaction_tree.item(child)['values'])

        file_name = "data_transaksi.xlsx"
        workbook.save(file_name)
        messagebox.showinfo("Sukses", f"Data transaksi berhasil diexport ke {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
