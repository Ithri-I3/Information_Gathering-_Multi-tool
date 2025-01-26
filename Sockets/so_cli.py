import socket
import json

# Fonction pour récupérer l'IP locale de la machine
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Se connecter à un serveur fictif pour obtenir l'IP locale
        s.connect(('10.254.254.254', 1))  # Utiliser une adresse IP quelconque
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '0.0.0.0'  # Si la connexion échoue, retourne une valeur par défaut
    finally:
        s.close()
    return local_ip

def main():
    # Ouvrir le fichier socket.txt en mode écriture
    with open('socket.txt', 'w') as file:
        # Récupérer l'adresse IP locale automatiquement
        local_ip = get_local_ip()
        file.write(f"L'adresse IP locale de la machine est : {local_ip}\n")

        # Configurer la connexion au serveur (si le serveur est sur la même machine)
        server_ip = local_ip  # Utilisation de l'IP locale
        server_port = 12345  # Le port du serveur
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))  # Connexion au serveur

        # Recevoir les données du serveur
        data = client_socket.recv(4096)  # Taille du buffer ajustable si nécessaire

        # Charger les données JSON
        system_info = json.loads(data.decode('utf-8'))

        # Écrire les informations du système d'exploitation dans le fichier
        file.write("Informations du Système d'exploitation :\n")
        for key, value in system_info['OS'].items():
            file.write(f"{key}: {value}\n")

        file.write("\nInformations CPU :\n")
        for key, value in system_info['CPU'].items():
            file.write(f"{key}: {value}\n")

        file.write("\nInformations Mémoire :\n")
        for key, value in system_info['Mémoire'].items():
            file.write(f"{key}: {value}\n")

        file.write("\nInformations de Stockage :\n")
        for device, info in system_info['Stockage'].items():
            file.write(f"Périphérique {device}:\n")
            if isinstance(info, dict):
                for key, value in info.items():
                    file.write(f"  {key}: {value}\n")
            else:
                file.write(f"  {info}\n")

        file.write("\nPériphériques connectés :\n")
        for key, value in system_info['Périphériques'].items():
            file.write(f"{key}: {value}\n")

        file.write("\nInformations Batterie (si applicable) :\n")
        for key, value in system_info['Batterie'].items():
            file.write(f"{key}: {value}\n")

        # Envoyer un message (correctement encodé en UTF-8)
        message = "Message reçu par le serveur."
        client_socket.sendall(message.encode('utf-8'))  # Encoder en UTF-8
        client_socket.close()

if __name__ == "__main__":
    main()
