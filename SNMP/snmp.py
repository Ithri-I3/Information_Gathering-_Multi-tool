import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import platform
import subprocess

def validate_inputs(ip_address, oid):
    ip_regex = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    oid_regex = re.compile(r'^\d+\.\d+(\.\d+)*$')
    if not ip_regex.match(ip_address):
        return "Adresse IP invalide. Format attendu : x.x.x.x (ex: 192.168.0.1)."
    if not oid_regex.match(oid):
        return "OID invalide. Format attendu : au moins deux nombres séparés par un point (ex: 1.3)."
    return None

def check_os():
    current_os = platform.system()
    if current_os == "Windows":
        message = "Vous utilisez Windows."
    elif current_os == "Linux":
        message = "Vous utilisez Linux."
    else:
        message = f"Système inconnu : {current_os}"

    insert_line(message)

def run_command(ip_address, oid, community, operation):
    os_type = platform.system().lower()

    if os_type == "linux":
        if operation == "get":
            command = ["SNMP/linux/oid_getCmd_linux", ip_address, oid]
        elif operation == "next":
            command = ["SNMP/linux/oid_nextCmd_linux", ip_address, oid]
    elif os_type == "windows":
        if operation == "get":
            command = ["SNMP/windows/dist/getcmd_win.exe", ip_address, oid]
        elif operation == "next":
            command = ["SNMP/windows/dist/next_cmd_win.exe", ip_address, oid]

    # Ajouter l'option -c si la communauté n'est pas "public"
    if community and community != "public":
        command.append("-c")
        command.append(community)

    try:
        # Exécuter la commande et récupérer la sortie
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout  # Récupérer la sortie standard de la commande

        for line in output.splitlines():
            insert_line(line)

        insert_line("-" * 50)

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erreur d'exécution", f"Erreur lors de l'exécution de la commande: {e}")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

def insert_line(text):
    """
    Affiche une ligne de texte dans le canvas et fait défiler automatiquement vers le bas.
    """
    output_canvas.create_text(5, output_canvas.bbox("all")[3] + 15 if output_canvas.bbox("all") else 10,
                              text=text, anchor="nw", font=("Arial", 12), fill="black")
    
    output_canvas.update_idletasks()  # Met à jour l'affichage pour refléter les nouvelles lignes

    # Mettre à jour la zone de défilement pour inclure toutes les lignes ajoutées
    output_canvas.config(scrollregion=output_canvas.bbox("all"))

    # Faire défiler automatiquement vers le bas après l'ajout d'une ligne
    output_canvas.yview_moveto(1)  # Déplace la vue de la scrollbar tout en bas

def clear_canvas():
    """
    Supprime tout le contenu du canvas.
    """
    output_canvas.delete("all")

def submit():
    # Effacer le contenu précédent du canvas
    clear_canvas()

    ip_address = ip_entry.get().strip()
    oid = oid_entry.get().strip()
    community = community_entry.get().strip()
    operation = operation_combo.get().strip()

    # Remplace "placeholder" par une chaîne vide si l'utilisateur ne le modifie pas
    if community == "public":
        community = ""

    error_message = validate_inputs(ip_address, oid)
    if error_message:
        messagebox.showerror("Erreur de Validation", error_message)
        return

    # Insérer les informations de l'utilisateur dans la fenêtre de sortie
    insert_line(f"IP Address: {ip_address}")
    insert_line(f"OID: {oid}")
    insert_line(f"Community: {community if community else 'public'}")
    insert_line(f"Operation: {operation}")
    insert_line("-" * 50)

    run_command(ip_address, oid, community, operation)

def add_placeholder(event, entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.configure(foreground="grey")

def remove_placeholder(event, entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, tk.END)
        entry.configure(foreground="black")

# Création de la fenêtre principale
root = tk.Tk()
root.title("SNMP Interface")
root.geometry("1000x500")
root.configure(bg="#d1f5d3")

# Style global
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#d1f5d3", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TCombobox", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), background="#4caf50", foreground="white", padding=5)

# Conteneur principal centré
frame = tk.Frame(root, bg="#d1f5d3", padx=10, pady=10)
frame.pack(expand=True)

# Adresse IP
ttk.Label(frame, text="Adresse IP :").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ip_entry = ttk.Entry(frame, width=20)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

# OID
ttk.Label(frame, text="OID :").grid(row=0, column=2, padx=5, pady=5, sticky="e")
oid_entry = ttk.Entry(frame, width=20)
oid_entry.grid(row=0, column=3, padx=5, pady=5)

# Community avec placeholder
ttk.Label(frame, text="Community :").grid(row=0, column=4, padx=5, pady=5, sticky="e")
community_entry = ttk.Entry(frame, width=20, foreground="grey")
community_entry.grid(row=0, column=5, padx=5, pady=5)

# Ajout du placeholder "public"
placeholder_text = "public"
community_entry.insert(0, placeholder_text)
community_entry.bind("<FocusIn>", lambda event: remove_placeholder(event, community_entry, placeholder_text))
community_entry.bind("<FocusOut>", lambda event: add_placeholder(event, community_entry, placeholder_text))

# Dropdown pour choisir entre Get ou Next
ttk.Label(frame, text="Opération :").grid(row=0, column=6, padx=5, pady=5, sticky="e")
operation_combo = ttk.Combobox(frame, values=["get", "next"], state="readonly", width=15)
operation_combo.set("get")
operation_combo.grid(row=0, column=7, padx=5, pady=5)

# Bouton de soumission
submit_button = ttk.Button(frame, text="Soumettre", command=submit)
submit_button.grid(row=0, column=8, padx=10, pady=5)

# Canvas pour afficher les résultats avec Scrollbar
canvas_frame = tk.Frame(root, bg="white")
canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)

output_canvas = tk.Canvas(canvas_frame, bg="white", width=980)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=output_canvas.yview)
output_canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
output_canvas.pack(side="left", fill="both", expand=True)

# Lancement de l'interface graphique
root.mainloop()

