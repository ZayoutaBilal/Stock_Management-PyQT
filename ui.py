import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QAbstractItemView,
    QSizePolicy, QHeaderView
)
from models import (
    init_db, ajouter_client, lire_clients, modifier_client, supprimer_client,
    ajouter_produit, lire_produits, modifier_produit, supprimer_produit,
    ajouter_commande, lire_commandes, modifier_commande, supprimer_commande, get_produit_quantite, set_produit_quantite
)
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Stock")
        self.setGeometry(500, 200, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()

        self.tabs = QTabWidget()


        self.tabs.addTab(self.create_client_tab(), "Client")
        self.tabs.addTab(self.create_product_tab(), "Produit")
        self.tabs.addTab(self.create_order_tab(), "Commande")

        main_layout.addWidget(self.tabs)

        self.central_widget.setLayout(main_layout)

    # ==================== Onglet Client ====================
    def create_client_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.client_name_input = QLineEdit()
        self.client_name_input.setPlaceholderText("Nom")
        self.client_email_input = QLineEdit()
        self.client_email_input.setPlaceholderText("Email")

        add_button = QPushButton("Ajouter Client")
        add_button.clicked.connect(self.add_client)

        update_button = QPushButton("Modifier Client")
        update_button.clicked.connect(self.update_client)

        layout.addWidget(self.client_name_input)
        layout.addWidget(self.client_email_input)
        layout.addWidget(add_button)
        layout.addWidget(update_button)

        self.client_table = QTableWidget()
        self.client_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.client_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.client_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.client_table.setColumnCount(3)
        self.client_table.setHorizontalHeaderLabels(["ID", "Nom", "Email"])
        self.client_table.cellClicked.connect(self.fill_client_form)
        layout.addWidget(self.client_table)
        self.load_clients()

        delete_button = QPushButton("Supprimer Client Sélectionné")
        delete_button.clicked.connect(self.delete_client)
        layout.addWidget(delete_button)

        tab.setLayout(layout)
        return tab

    def load_clients(self):
        clients = lire_clients()
        self.client_table.setRowCount(0)
        for row, client in enumerate(clients):
            self.client_table.insertRow(row)
            for col, data in enumerate(client):
                self.client_table.setItem(row, col, QTableWidgetItem(str(data)))

    def add_client(self):
        name = self.client_name_input.text()
        email = self.client_email_input.text()
        if name and email:
            ajouter_client(name, email)
            self.load_clients()
            self.clear_client_form()
            self.populate_dropdown_clients()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def update_client(self):
        client_id = self.client_table.item(self.client_table.currentRow(), 0).text()
        name = self.client_name_input.text()
        email = self.client_email_input.text()
        if client_id and name and email:
            modifier_client(int(client_id), name, email)
            self.load_clients()
            self.clear_client_form()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs pour la modification.")

    def delete_client(self):
        selected_row = self.client_table.currentRow()
        if selected_row >= 0:
            client_id = int(self.client_table.item(selected_row, 0).text())
            supprimer_client(client_id)
            self.load_clients()
            self.clear_client_form()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un client à supprimer.")

    def fill_client_form(self, row):
        self.client_name_input.setText(self.client_table.item(row, 1).text())
        self.client_email_input.setText(self.client_table.item(row, 2).text())

    def clear_client_form(self):
        self.client_name_input.clear()
        self.client_email_input.clear()

    # ==================== Onglet Produit ====================
    def create_product_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Nom du Produit")
        self.product_price_input = QLineEdit()
        self.product_price_input.setPlaceholderText("Prix")
        self.product_Quantity_input = QLineEdit()
        self.product_Quantity_input.setPlaceholderText("Quantite")

        add_button = QPushButton("Ajouter Produit")
        add_button.clicked.connect(self.add_product)

        update_button = QPushButton("Modifier Produit")
        update_button.clicked.connect(self.update_product)

        layout.addWidget(self.product_name_input)
        layout.addWidget(self.product_price_input)
        layout.addWidget(self.product_Quantity_input)
        layout.addWidget(add_button)
        layout.addWidget(update_button)

        self.product_table = QTableWidget()
        self.product_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.product_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(["ID", "Nom", "Prix","Quantite"])
        self.product_table.cellClicked.connect(self.fill_product_form)
        layout.addWidget(self.product_table)
        self.load_products()

        delete_button = QPushButton("Supprimer Produit Sélectionné")
        delete_button.clicked.connect(self.delete_product)
        layout.addWidget(delete_button)

        tab.setLayout(layout)
        return tab

    def load_products(self):
        products = lire_produits()
        self.product_table.setRowCount(0)
        for row, product in enumerate(products):
            self.product_table.insertRow(row)
            for col, data in enumerate(product):
                self.product_table.setItem(row, col, QTableWidgetItem(str(data)))

    def add_product(self):
        name = self.product_name_input.text()
        price = self.product_price_input.text()
        quantity = self.product_Quantity_input.text()
        if name and price and quantity:
            try:
                ajouter_produit(name, float(price),int(quantity))
                self.load_products()
                self.clear_product_form()
                self.populate_dropdown_produits()
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Le prix doit être un nombre valide.")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")

    def update_product(self):
        product_id = self.product_table.item(self.product_table.currentRow(), 0).text()
        name = self.product_name_input.text()
        price = self.product_price_input.text()
        quantity = self.product_Quantity_input.text()
        if product_id and name and price and quantity:
            try:
                modifier_produit(int(product_id), name, float(price),int(quantity))
                self.load_products()
                self.clear_product_form()
            except ValueError:
                QMessageBox.warning(self, "Erreur", "Le prix doit être un nombre valide.")
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs pour la modification.")

    def delete_product(self):
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            product_id = int(self.product_table.item(selected_row, 0).text())
            supprimer_produit(product_id)
            self.load_products()
            self.clear_product_form()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un produit à supprimer.")

    def fill_product_form(self, row):
        self.product_name_input.setText(self.product_table.item(row, 1).text())
        self.product_price_input.setText(self.product_table.item(row, 2).text())
        self.product_Quantity_input.setText(self.product_table.item(row, 3).text())

    def clear_product_form(self):
        self.product_name_input.clear()
        self.product_price_input.clear()
        self.product_Quantity_input.clear()

    # ==================== Onglet Commande ====================
    def create_order_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.client_dropdown = QComboBox()
        self.product_dropdown = QComboBox()

        self.populate_dropdown_clients()
        self.populate_dropdown_produits()

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")

        add_button = QPushButton("Ajouter Commande")
        add_button.clicked.connect(self.add_command)

        update_button = QPushButton("Modifier Commande")
        update_button.clicked.connect(self.update_command)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.client_dropdown)
        input_layout.addWidget(self.product_dropdown)
        input_layout.addWidget(self.quantity_input)
        input_layout.addWidget(add_button)
        input_layout.addWidget(update_button)

        layout.addLayout(input_layout)

        self.order_table = QTableWidget()
        self.order_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.order_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["ID", "Client", "Product", "Quantity","Date"])
        self.order_table.cellClicked.connect(self.fill_order_form)
        layout.addWidget(self.order_table)

        self.load_orders()

        delete_button = QPushButton("Supprimer Commande Sélectionné")
        delete_button.clicked.connect(self.delete_order)
        layout.addWidget(delete_button)

        tab.setLayout(layout)
        return tab

    def load_orders(self):
        orders = lire_commandes()
        self.order_table.setRowCount(0)
        for row, order in enumerate(orders):
            self.order_table.insertRow(row)
            for col, data in enumerate(order):
                self.order_table.setItem(row, col, QTableWidgetItem(str(data)))
        pass

    def add_command(self):
        client_id = self.client_dropdown.currentData()
        product_id = self.product_dropdown.currentData()
        quantity = self.quantity_input.text()
        if not client_id or not product_id or not quantity:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return
        if int(quantity) > get_produit_quantite(int(product_id)):
            QMessageBox.warning(self, "Erreur", "cette quantite n'est pas disponible !")
            return

        try:
            ajouter_commande(client_id, product_id, int(quantity),datetime.now())
            set_produit_quantite(int(product_id),int(quantity))
            self.load_orders()

        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le quantity doit être un nombre valide.")

    def update_command(self):
        selected_row = self.order_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une commande à modifier.")
            return
        order_id = self.order_table.item(selected_row, 0).text()

        client_id = self.client_dropdown.currentData()
        product_id = self.product_dropdown.currentData()
        quantity = self.quantity_input.text()

        if not client_id or not product_id or not quantity:
            QMessageBox.warning(self, "Erreur", "Veuillez remplir tous les champs.")
            return
        try:
            modifier_commande(order_id, client_id, product_id, int(quantity))
            self.load_orders()
            QMessageBox.information(self, "Succès", "Commande mise à jour avec succès.")
        except ValueError:
            QMessageBox.warning(self, "Erreur", "La quantité doit être un nombre valide.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur s'est produite: {str(e)}")

    def delete_order(self):
        selected_row = self.order_table.currentRow()
        if selected_row >= 0:
            order_id = int(self.order_table.item(selected_row, 0).text())
            supprimer_commande(order_id)
            self.load_orders()
        else:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une commande à supprimer.")

    def fill_order_form(self, row):
        order_id = self.order_table.item(row, 0).text()
        client_name = self.order_table.item(row, 1).text()
        product_name = self.order_table.item(row, 2).text()
        quantity = self.order_table.item(row, 3).text()

        client_index = self.client_dropdown.findText(client_name)
        if client_index != -1:
            self.client_dropdown.setCurrentIndex(client_index)

        product_index = self.product_dropdown.findText(product_name)
        if product_index != -1:
            self.product_dropdown.setCurrentIndex(product_index)

        self.quantity_input.setText(quantity)

    def populate_dropdown_clients(self):
        clients = lire_clients()
        self.client_dropdown.clear()
        self.client_dropdown.addItem("Select Client", "")
        for client in clients:
            client_id, client_name = client[0], client[1]
            self.client_dropdown.addItem(client_name, client_id)

    def populate_dropdown_produits(self):
        produits = lire_produits()
        self.product_dropdown.clear()
        self.product_dropdown.addItem("Select Product", "")
        for produit in produits:
            product_id, product_name = produit[0], produit[1]
            self.product_dropdown.addItem(product_name, product_id)
