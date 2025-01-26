import socket
import platform
import psutil
import subprocess
import json

# Fonctions de récupération d'informations système
def get_os_info():
    os_info = platform.uname()
    return {
        'Systeme': os_info.system,
        'Nom du PC': os_info.node,
        'Version du système': os_info.version,
        'Machine': os_info.machine,
        'Processeur': os_info.processor
    }

def get_cpu_info():
    return {
        'Nombre de coeurs physiques': psutil.cpu_count(logical=False),
        'Nombre de coeurs logiques': psutil.cpu_count(logical=True),
        'Fréquence max (MHz)': psutil.cpu_freq().max,
        'Fréquence min (MHz)': psutil.cpu_freq().min,
        'Fréquence actuelle (MHz)': psutil.cpu_freq().current
    }

def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    return {
        'Mémoire totale (GB)': virtual_mem.total / (1024**3),
        'Mémoire disponible (GB)': virtual_mem.available / (1024**3),
        'Pourcentage utilisé (%)': virtual_mem.percent
    }

def get_storage_info():
    storage_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            storage_info[partition.device] = {
                'Total (GB)': usage.total / (1024**3),
                'Utilisé (GB)': usage.used / (1024**3),
                'Libre (GB)': usage.free / (1024**3),
                'Pourcentage utilisé (%)': usage.percent,
            }
        except PermissionError:
            storage_info[partition.device] = "Accès refusé"
    return storage_info

def get_devices_info():
    os_system = platform.system()
    if os_system == "Linux":
        try:
            devices = subprocess.check_output("lsusb", shell=True).decode()
            return {'Périphériques USB': devices}
        except Exception as e:
            return {'Erreur': str(e)}
    elif os_system == "Windows":
        try:
            devices = subprocess.check_output("wmic path Win32_USBHub get DeviceID", shell=True).decode()
            return {'Périphériques USB': devices}
        except Exception as e:
            return {'Erreur': str(e)}
    else:
        return {'Erreur': "Système non supporté"}

def get_battery_info():
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery is not None:
            return {
                'Pourcentage de la batterie': battery.percent,
                'Temps restant (s)': battery.secsleft if battery.secsleft != -2 else "N/A",
                'Branché sur secteur': battery.power_plugged
            }
        else:
            return {'Batterie': "Aucune batterie détectée"}
    return {'Batterie': "Fonctionnalité non supportée"}

# Fonction principale du serveur
def main():
    # Configurer le serveur
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(1)
    print("Serveur en attente de connexion...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")

        # Collecte des informations système
        data = {
            'OS': get_os_info(),
            'CPU': get_cpu_info(),
            'Mémoire': get_memory_info(),
            'Stockage': get_storage_info(),
            'Périphériques': get_devices_info(),
            'Batterie': get_battery_info()
        }

        # Envoi des données au client
        client_socket.sendall(json.dumps(data).encode('utf-8'))
        client_socket.close()

if __name__ == "__main__":
    main()
