import tkinter as tk
from tkinter.ttk import Treeview
from tkinter import messagebox, Label, Entry, Button, Toplevel, Frame, Listbox, StringVar, BOTH, LEFT, END
from managers.shelfManager import ShelfManager
from managers.bookManager import BookManager
from models.shelf import Shelf


class ShelfApp:
    """
    GUI Application for managing shelves.

    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        shelf_manager (ShelfManager): Manager for handling shelves.
        book_manager (BookManager): Manager for handling books.
    """
    def __init__(self, root):
        """
        Initializes the ShelfApp with the given root window.

        Args:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Gestion des Étagères")

        self.shelf_manager = ShelfManager()
        self.book_manager = BookManager()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        search_frame = Frame(self.root)
        search_frame.pack(pady=10)

        self.number_search_frame = Frame(search_frame)
        self.number_search_frame.grid(row=0, column=0, padx=10)
        self.search_label_number = Label(self.number_search_frame, font=('Verdana', 12, 'bold'), text="Recherche par Allée")
        self.search_label_number.pack(side=LEFT)
        self.search_entry_number = Entry(self.number_search_frame)
        self.search_entry_number.pack(side=LEFT)
        self.search_button_number = Button(self.number_search_frame, text="Recherche", font=('Verdana', 12, 'bold'), command=self.search_by_number)
        self.search_button_number.pack(side=LEFT)

        self.letter_search_frame = Frame(search_frame)
        self.letter_search_frame.grid(row=0, column=1, padx=10)
        self.search_label_letter = Label(self.letter_search_frame, font=('Verdana', 12, 'bold'), text="Recherche par Rayon")
        self.search_label_letter.pack(side=LEFT)
        self.search_entry_letter = Entry(self.letter_search_frame)
        self.search_entry_letter.pack(side=LEFT)
        self.search_button_letter = Button(self.letter_search_frame, text="Recherche", font=('Verdana', 12, 'bold'), command=self.search_by_letter)
        self.search_button_letter.pack(side=LEFT)

        self.refresh_list_button = Button(self.root, text="Actualiser la liste", font=('Verdana', 12, 'bold'), command = self.refresh_list)
        self.refresh_list_button.pack(pady=10)

        self.tree = Treeview(self.root, columns=('ID', 'Allée', 'Rayon', 'Livres'), show='headings')
        self.tree.pack(pady=10, fill=BOTH, expand=True)

        self.tree.heading('ID', text='ID')
        self.tree.heading('Allée', text='Allée')
        self.tree.heading('Rayon', text='Rayon')
        self.tree.heading('Livres', text='Livres')

        self.tree.column('ID', width=50)
        self.tree.column('Allée', width=100)
        self.tree.column('Rayon', width=150)
        self.tree.column('Livres', width=250)

        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        self.add_button = Button(button_frame, text="Ajouter une étagère", font=('Verdana', 12, 'bold'), command=self.add_shelf)
        self.add_button.pack(side=LEFT, padx=10)

        self.edit_button = Button(button_frame, text="Modifier une étagère", font=('Verdana', 12, 'bold'), command=self.edit_shelf)
        self.edit_button.pack(side=LEFT, padx=10)

        self.remove_button = Button(button_frame, text="Supprimer une étagère", font=('Verdana', 12, 'bold'), command=self.remove_shelf)
        self.remove_button.pack(side=LEFT, padx=10)

        self.add_book_button = Button(button_frame, text="Ajouter un livre à une étagère", font=('Verdana', 12, 'bold'), command=self.add_book_to_shelf)
        self.add_book_button.pack(side=LEFT, padx=10)

        self.remove_book_button = Button(button_frame, text="Enlever un livre d'une étagère", font=('Verdana', 12, 'bold'), command=self.remove_book_from_shelf)
        self.remove_book_button.pack(side=LEFT, padx=10)

        self.update_treeview()

    def search_by_number(self):
        """
        Searches for shelves by aisle number.
        """
        search_number = self.search_entry_number.get().strip().lower()
        filtered_shelves = [s for s in self.shelf_manager.shelves if search_number in str(s.number).lower()]
        if not filtered_shelves :
            messagebox.showwarning("Ce numéro d'allée n'existe pas.")
        self.update_treeview(filtered_shelves)

    def search_by_letter(self):
        """
        Searches for shelves by shelf letter.
        """
        search_letter = self.search_entry_letter.get().strip().lower()
        filtered_shelves = [s for s in self.shelf_manager.shelves if search_letter in str(s.letter).lower()]
        if not filtered_shelves :
            messagebox.showwarning("Cette lettre de rayon n'existe pas.")
        self.update_treeview(filtered_shelves)

    def update_treeview(self, shelves=None):
        """
        Updates the treeview with the current list of shelves.

        Args:
            shelves (list, optional): List of shelves to display. Defaults to None.
        """
        self.tree.delete(*self.tree.get_children())
        shelves = shelves or self.shelf_manager.shelves
        for shelf in shelves :
            book_titles = ", ".join([book.title for book in shelf.books])
            self.tree.insert('', 'end', values=
                             (
                                 shelf.shelf_id,
                                 shelf.number,
                                 shelf.letter,
                                 book_titles
                             ))
        
    def refresh_list(self):
        """
        Refreshes the shelf list in the treeview.
        """
        self.update_treeview()
            
    def edit_shelf(self):
        """
        Refreshes the shelf list in the treeview.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Veuillez sélectionner une étagère à modifier.")
            return

        selected_shelf_id = self.tree.item(selected_item[0])['values'][0]
        shelf = next((s for s in self.shelf_manager.shelves if s.shelf_id == selected_shelf_id), None)

        self.add_shelf(shelf)

    def remove_shelf(self):
        """
        Removes the selected shelf.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Veuillez sélectionner une étagère à modifier.")
            return

        selected_shelf_id = self.tree.item(selected_item[0])['values'][0]
        self.shelf_manager.remove_shelf(selected_shelf_id)

        self.update_treeview()

    def add_shelf(self, shelf=None):
        """
        Opens the form to add or edit a shelf.

        Args:
            shelf (Shelf, optional): The shelf to edit. Defaults to None.
        """
        self.shelf_wind = tk.Toplevel(self.root)
        self.shelf_wind.title("Formulaire Étagère")

        wind_width = 500
        wind_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (wind_width // 2)
        position_y = (screen_height // 2) - (wind_height // 2)
        self.shelf_wind.geometry(f"{wind_width}x{wind_height}+{position_x}+{position_y}")

        self.shelf_id_label = Label(self.shelf_wind, text="ID : ")
        self.shelf_id_label.grid(row=0, column=0, sticky='E')
        self.shelf_id_entry = Entry(self.shelf_wind, state="readonly", textvariable=StringVar(self.shelf_wind, value=str(shelf.shelf_id if shelf else Shelf.shelf_number)))
        self.shelf_id_entry.grid(row=0, column=1)

        self.number_label = Label(self.shelf_wind, text="Allée : ")
        self.number_label.grid(row=1, column=0, sticky='E')
        self.number_entry = Entry(self.shelf_wind)
        self.number_entry.grid(row=1, column=1)
        self.number_entry.insert(0, shelf.number if shelf else "")
        self.number_entry.focus_set()

        self.letter_label = Label(self.shelf_wind, text="Rayon : ")
        self.letter_label.grid(row=2, column=0, sticky='E')
        self.letter_entry = Entry(self.shelf_wind)
        self.letter_entry.grid(row=2, column=1)
        self.letter_entry.insert(0, shelf.letter if shelf else "")

        self.submit_button = Button(self.shelf_wind, text="Valider", command=lambda: self.save_shelf(shelf))
        self.submit_button.grid(row=3, column=0, columnspan=2)

    def save_shelf(self, shelf=None):
        """
        Saves the shelf information entered in the form.

        Args:
            shelf (Shelf, optional): The shelf to save. Defaults to None.
        """
        shelf_id = int(self.shelf_id_entry.get())
        try:
            number = int(self.number_entry.get())
        except ValueError:
            messagebox.showwarning("L'allée doit être un nombre")
            return

        letter = self.letter_entry.get().strip().upper()
        if not letter.isalpha() or len(letter) != 1:
            messagebox.showwarning("Le rayon doit être une lettre")
            return

        if not number or not letter:
            messagebox.showwarning("Veuillez remplir tous les champs !")
            return
        
        new_shelf = Shelf(shelf_id, number, letter)
        try:
            if shelf:
                self.shelf_manager.update_shelf(shelf.number, new_shelf)
            else:
                self.shelf_manager.add_shelf(new_shelf)
        except ValueError as e:
            messagebox.showwarning("Erreur", str(e))
            return

        self.update_treeview()
        self.shelf_wind.destroy()

    def add_book_to_shelf(self) :
        """
        Adds a book to the selected shelf.
        """
        selected_item = self.tree.selection()
        if not selected_item :
            messagebox.showwarning("Veuillez sélectionner une étagère.")
            return
        
        selected_shelf_id = self.tree.item(selected_item[0])['values'][0]
        shelf = next((s for s in self.shelf_manager.shelves if s.shelf_id == selected_shelf_id), None)

        self.book_wind = Toplevel(self.root)
        self.book_wind.title("Ajouter un livre à l'étagère")

        wind_width = 500
        wind_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (wind_width // 2)
        position_y = (screen_height // 2) - (wind_height // 2)
        self.book_wind.geometry(f"{wind_width}x{wind_height}+{position_x}+{position_y}")

        self.book_list = Listbox(self.book_wind, selectmode='single')
        self.book_list.pack(pady=10, fill=BOTH, expand=True)

        for book in self.book_manager.books :
            self.book_list.insert(END, f"{book.book_id}: {book.title} by {', '.join(book.authors)}")

        self.book_submit_button = Button(self.book_wind, text="Ajouter", command=lambda : self.save_book_to_shelf(shelf))
        self.book_submit_button.pack(pady=10)

    def save_book_to_shelf(self, shelf):
        """
        Saves the selected book to the shelf.

        Args:
            shelf (Shelf): The shelf to add the book to.
        """
        selected_book_index = self.book_list.curselection()
        if not selected_book_index :
            messagebox.showwarning("Veuillez sélectionner un livre.")
            return
    
        book_id = int(self.book_list.get(selected_book_index[0]).split(":")[0].strip())
        book = next((b for b in self.book_manager.books if b.book_id == book_id), None)

        if not book :
            messagebox.showwarning("Livre introuvable")
            return
        
        try :
            self.shelf_manager.add_book_to_shelf(shelf.number, book)
        except ValueError as e :
            messagebox.showwarning("Erreur", str(e))
            return
        
        self.update_treeview()
        self.book_wind.destroy()

    def remove_book_from_shelf(self):
        """
        Removes a book from the selected shelf.
        """
        selected_item = self.tree.selection()
        if not selected_item :
            messagebox.showwarning("Veuillez sélectionner une étagère.")
            return
    
        selected_shelf_id = self.tree.item(selected_item[0])['values'][0]
        shelf = next((s for s in self.shelf_manager.shelves if s.shelf_id == selected_shelf_id), None)

        self.remove_book_wind = Toplevel(self.root)
        self.remove_book_wind.title("Supprimer un livre de l'étagère")

        wind_width = 500
        wind_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width // 2) - (wind_width // 2)
        position_y = (screen_height // 2) - (wind_height // 2)
        self.remove_book_wind.geometry(f"{wind_width}x{wind_height}+{position_x}+{position_y}")

        self.book_list = Listbox(self.remove_book_wind, selectmode='single')
        self.book_list.pack(pady=10, fill=BOTH, expand=True)

        for book in shelf.books :
            self.book_list.insert(END, f"{book.book_id}: {book.title} by {', '.join(book.authors)}")

        self.book_remove_button = Button(self.remove_book_wind, text="Supprimer", command=lambda : self.comfirm_remove_book(shelf))
        self.book_remove_button.pack(pady=10)

    def comfirm_remove_book(self, shelf): 
        """
        Removes a book from the selected shelf.
        """
        selected_book_index = self.book_list.curselection()
        if not selected_book_index :
            messagebox.showwarning("Veuillez sélectionner un livre.")
            return
        
        book_id = int(self.book_list.get(selected_book_index[0]).split(":")[0].strip())

        try :
            self.shelf_manager.remove_book_from_shelf(shelf.number, book_id)
        except ValueError as e :
            messagebox.showwarning("Erreur", str(e))
            return
        
        self.update_treeview()
        self.remove_book_wind.destroy()