import platform
import psutil
import requests
import json

# Function to get OS information
def get_os_info():
    os_info = platform.uname()
    return {
        'Systeme': os_info.system,
        'Nom du PC': os_info.node,
        'Version du système': os_info.version,
        'Machine': os_info.machine,
        'Processeur': os_info.processor
    }

# Function to get CPU information
def get_cpu_info():
    cpu_info = {
        'Nombre de coeurs physiques': psutil.cpu_count(logical=False),
        'Nombre de coeurs logiques': psutil.cpu_count(logical=True),
        'Fréquence max (MHz)': psutil.cpu_freq().max,
        'Fréquence min (MHz)': psutil.cpu_freq().min,
        'Fréquence actuelle (MHz)': psutil.cpu_freq().current,
    }
    return cpu_info

# Function to get memory information
def get_memory_info():
    virtual_mem = psutil.virtual_memory()
    memory_info = {
        'Mémoire totale (GB)': virtual_mem.total / (1024**3),
        'Mémoire disponible (GB)': virtual_mem.available / (1024**3),
        'Pourcentage utilisé (%)': virtual_mem.percent,
    }
    return memory_info

# Function to get storage information
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

# Function to list connected devices
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

# Function to get battery info (optional)
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

# Function to send data to server
def send_data_to_server(data, url="https://33df-129-45-112-48.ngrok-free.app/api/system_info"):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Data sent successfully!")
    except requests.exceptions.RequestException as e:
        print("Failed to send data:", e)

# Main function to gather data and send to server
def main():
    data = {
        "OS_Info": get_os_info(),
        "CPU_Info": get_cpu_info(),
        "Memory_Info": get_memory_info(),
        "Storage_Info": get_storage_info(),
        "Devices_Info": get_devices_info(),
        "Battery_Info": get_battery_info(),
    }
    send_data_to_server(data)

if __name__ == "__main__":
    main()
