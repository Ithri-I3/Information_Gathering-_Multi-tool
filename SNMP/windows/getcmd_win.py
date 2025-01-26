import argparse
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# Fonction asynchrone pour exécuter une commande SNMP GET
async def snmp_get(target, port, community, oid):
    # Exécution de la commande GET
    transport_target = await UdpTransportTarget.create((target, port))  # Utilisation de .create()
    iterator = get_cmd(
        SnmpEngine(),
        CommunityData(community),
        transport_target,
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    error_indication, error_status, error_index, var_binds = await iterator
    if error_indication:
        # Ignorer l'erreur noSuchName, qui indique que l'OID n'est pas disponible
        if "noSuchName" in str(error_indication):
            return None
        # Autres erreurs, les afficher
        print(f"Erreur SNMP: {error_indication}")
        return None
    elif error_status:
        if "noSuchName" in str(error_status):
            return None
        print(f"Erreur SNMP: {error_status.prettyPrint()}")
        return None
    else:
        for var_bind in var_binds:
            print(f"{var_bind[0]} = {var_bind[1]}")

# Fonction principale pour récupérer les paramètres depuis la ligne de commande
def main():
    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(description="Exécuter une requête SNMP GET")
    parser.add_argument("ip", help="Adresse IP de la cible SNMP")
    parser.add_argument("oid", help="OID SNMP à interroger")
    parser.add_argument("-c", "--community", default="public", help="Nom de la communauté SNMP (par défaut: public)")

    # Récupération des arguments
    args = parser.parse_args()

    # Exécution de la fonction dans une boucle événementielle
    asyncio.run(snmp_get(args.ip, 161, args.community, args.oid))

if __name__ == "__main__":
    main()
