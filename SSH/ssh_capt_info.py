import platform
import psutil
import subprocess

# Fonction pour obtenir les informations du système d'exploitation
def get_os_info():
    os_info = platform.uname()
    return {
        'Systeme': os_info.system,
        'Nom du PC': os_info.node,
        'Version du système': os_info.version,
        'Machine': os_info.machine,
        'Processeur': os_info.processor
    }

# Fonction pour obtenir les informations de la CPU
def get_cpu_info():
    cpu_info = {
        'Nombre de coeurs physiques': psutil.cpu_count(logical=False),
        'Nombre de coeurs logiques': psutil.cpu_count(logical=True),
        'Fréquence max (MHz)': psutil.cpu_freq().max,
        'Fréquence min (MHz)': psutil.cpu_freq().min,
        'Fréquence actuelle (MHz)': psutil.cpu_freq().current,
    }
    return cpu_info

# Fonction pour obtenir les informations de la mémoire
def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    memory_info = {
        'Mémoire totale (GB)': virtual_mem.total / (1024**3),
        'Mémoire disponible (GB)': virtual_mem.available / (1024**3),
        'Pourcentage utilisé (%)': virtual_mem.percent,
    }
    return memory_info

# Fonction pour obtenir les informations de stockage
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
            # Some partitions may not be accessible
            storage_info[partition.device] = "Accès refusé"
    return storage_info

# Fonction pour lister les périphériques
def get_devices_info():
    # Vérifier le système d'exploitation
    os_system = platform.system()

    if os_system == "Linux":
        # Utilisation de 'lsusb' pour Linux
        try:
            devices = subprocess.check_output("lsusb", shell=True).decode()
            return {'Périphériques USB': devices}
        except Exception as e:
            return {'Erreur': str(e)}

    elif os_system == "Windows":
        # Utilisation de 'wmic' pour Windows
        try:
            devices = subprocess.check_output("wmic path Win32_USBHub get DeviceID", shell=True).decode()
            return {'Périphériques USB': devices}
        except Exception as e:
            return {'Erreur': str(e)}

    else:
        return {'Erreur': "Système non supporté"}

# Fonction pour obtenir les informations de la batterie (optionnel pour un laptop)
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

# Fonction pour écrire les informations dans un fichier
def write_to_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Informations du Système d'exploitation :\n")
        for key, value in get_os_info().items():
            f.write(f"{key}: {value}\n")

        f.write("\nInformations CPU :\n")
        for key, value in get_cpu_info().items():
            f.write(f"{key}: {value}\n")

        f.write("\nInformations Mémoire :\n")
        for key, value in get_memory_info().items():
            f.write(f"{key}: {value}\n")

        f.write("\nInformations de Stockage :\n")
        storage_info = get_storage_info()
        for device, info in storage_info.items():
            f.write(f"Périphérique {device}:\n")
            if isinstance(info, dict):
                for key, value in info.items():
                    f.write(f"  {key}: {value}\n")
            else:
                f.write(f"  {info}\n")

        f.write("\nPériphériques connectés :\n")
        for key, value in get_devices_info().items():
            f.write(f"{key}: {value}\n")

        f.write("\nInformations Batterie (si applicable) :\n")
        for key, value in get_battery_info().items():
            f.write(f"{key}: {value}\n")

# Fonction principale pour démarrer l'écriture
def main():
    write_to_file("system_info.txt")

if __name__ == "__main__":
    main()
