from pysnmp.hlapi import *
import argparse

# Fonction pour exécuter un SNMP GET
def snmp_get(oid, ip, community='public', port=161, version=2):
    """
    Effectue une requête SNMP GET pour récupérer une valeur à partir d'un OID.
    :param oid: L'OID à interroger.
    :param ip: L'adresse IP de l'appareil cible.
    :param community: La communauté SNMP (par défaut 'public').
    :param port: Le port SNMP (par défaut 161).
    :param version: La version SNMP (par défaut SNMPv2c).
    :return: Un dictionnaire contenant les résultats ou un message d'erreur.
    """
    # Préparer la requête SNMP GET
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=version - 1),  # Version 2 => mpModel=1
        UdpTransportTarget((ip, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    # Exécuter la requête et récupérer la réponse
    error_indication, error_status, error_index, var_binds = next(iterator)

    # Vérification des erreurs
    if error_indication:
        return {"error": f"Erreur d'indication SNMP : {error_indication}"}
    elif error_status:
        return {"error": f"Erreur SNMP {error_status} à l'index {error_index}"}
    else:
        # Renvoyer les résultats
        return {"results": [(str(var_bind[0]), str(var_bind[1])) for var_bind in var_binds]}

# Point d'entrée principal
if __name__ == "__main__":
    # Analyse des arguments de ligne de commande
    parser = argparse.ArgumentParser(description="Effectue une requête SNMP GET pour un OID spécifique.")
    parser.add_argument("ip", help="Adresse IP de l'appareil cible")
    parser.add_argument("oid", help="OID à interroger")
    parser.add_argument("-c", "--community", default="public", help="Communauté SNMP (par défaut : public)")
    parser.add_argument("-p", "--port", type=int, default=161, help="Port SNMP (par défaut : 161)")
    parser.add_argument("-v", "--version", type=int, choices=[1, 2, 3], default=2, help="Version SNMP (1, 2, 3)")

    args = parser.parse_args()

    # Appel de la fonction avec les arguments fournis
    result = snmp_get(args.oid, args.ip, community=args.community, port=args.port, version=args.version)

    # Affichage des résultats dans la console
    if "error" in result:
        print(result["error"])
    elif "results" in result:
        print("Résultats SNMP GET :")
        for oid, value in result["results"]:
            print(f"{oid} = {value}")
    else:
        print("Aucune donnée trouvée.")

