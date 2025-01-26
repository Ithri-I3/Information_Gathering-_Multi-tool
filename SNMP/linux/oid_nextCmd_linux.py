from pysnmp.hlapi import *
import argparse

# Fonction pour récupérer les descriptions des dispositifs
def get_hrDeviceDescriptions(ip, community, base_oid, port=161):
    """
    Récupère les descriptions des dispositifs (comme les processeurs) sous l'OID spécifié.

    :param ip: Adresse IP de la machine cible
    :param community: Communauté SNMP
    :param base_oid: OID de base pour les descriptions de dispositifs
    :param port: Port SNMP (par défaut 161)
    :return: Liste des tuples (OID, valeur)
    """
    results = []

    # Utilisation de nextCmd pour parcourir toutes les entrées sous l'OID
    for (errorIndication, errorStatus, errorIndex, varBinds) in nextCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((ip, port)),
        ContextData(),
        ObjectType(ObjectIdentity(base_oid)),
        lexicographicMode=False,  # Arrête la recherche au-delà de l'OID de base
    ):
        if errorIndication:
            print(f"Erreur d'indication : {errorIndication}")
            break
        elif errorStatus:
            print(f"Erreur d'état : {errorStatus.prettyPrint()}")
            break
        else:
            for varBind in varBinds:
                # Ajout des résultats
                results.append((str(varBind[0]), str(varBind[1])))

    return results

# Point d'entrée principal
if __name__ == "__main__":
    # Analyse des arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Récupère les descriptions SNMP des dispositifs.")
    parser.add_argument("ip", help="Adresse IP de la machine cible")
    parser.add_argument("base_oid", help="OID de base pour les descriptions de dispositifs")
    parser.add_argument("-c", "--community", default="public", help="Communauté SNMP (par défaut : public)")
    parser.add_argument("-p", "--port", type=int, default=161, help="Port SNMP (par défaut : 161)")

    args = parser.parse_args()

    # Appel de la fonction avec les arguments fournis
    descriptions = get_hrDeviceDescriptions(args.ip, args.community, args.base_oid, args.port)

    # Affichage des résultats dans la console
    if descriptions:
        print("Descriptions des dispositifs :")
        for oid, description in descriptions:
            print(f"{oid} : {description}")
    else:
        print("Aucune information trouvée.")

