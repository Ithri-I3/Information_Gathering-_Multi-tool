import argparse
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# Fonction asynchrone pour effectuer un SNMP WALK
async def snmp_walk(target, port, community, oid):
    """Effectuer un SNMP WALK en utilisant next_cmd."""
    try:
        # Configurer la cible SNMP
        transport_target = await UdpTransportTarget.create((target, port))

        # Initialisation des variables pour le WALK
        base_oid = ObjectIdentity(oid)  # L'OID de base
        current_oid = ObjectType(base_oid)

        while True:
            # Appeler `next_cmd` pour récupérer le prochain ensemble de données
            error_indication, error_status, error_index, var_binds = await next_cmd(
                SnmpEngine(),
                CommunityData(community),
                transport_target,
                ContextData(),
                current_oid
            )

            if error_indication:
                print(f"Erreur SNMP : {error_indication}")
                break
            elif error_status:
                print(f"Erreur SNMP : {error_status.prettyPrint()} à l'index {error_index}")
                break
            else:
                # Vérifier et afficher les résultats
                for var_bind in var_binds:
                    oid_str = str(var_bind[0])
                    if oid_str.startswith(str(base_oid)) and oid_str != str(base_oid):
                        print(f"{var_bind[0]} = {var_bind[1]}")

                    # Vérifier si l'OID récupéré commence exactement par l'OID de base
                        # Préparer le prochain OID pour continuer le WALK
                        current_oid = ObjectType(ObjectIdentity(oid_str))
                    else:
                        # Si l'OID ne commence plus exactement par l'OID de base, arrêter le processus
                        print("L'OID ne correspond plus exactement à l'OID de base. Arrêt du processus.")
                        return

            # Arrêter si aucun nouveau résultat n'est disponible
            if not var_binds:
                break

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

# Fonction principale pour récupérer les paramètres depuis la ligne de commande
def main():
    # Création du parseur d'arguments
    parser = argparse.ArgumentParser(description="Effectuer un SNMP WALK")
    parser.add_argument("ip", help="Adresse IP de la cible SNMP")
    parser.add_argument("oid", help="OID SNMP pour commencer le WALK")
    parser.add_argument("-c", "--community", default="public", help="Nom de la communauté SNMP (par défaut: public)")

    # Récupération des arguments
    args = parser.parse_args()

    # Exécution de la fonction dans une boucle événementielle
    asyncio.run(snmp_walk(args.ip, 161, args.community, args.oid))

if __name__ == "__main__":
    main()
