SELECT_LAST_ADDRESS_USED = """SELECT
    coordonnees.id_coordonne
FROM coordonnees
LEFT JOIN commande c ON c.adresse_livraison = coordonnees.id_coordonne OR c.adresse_facturation = coordonnees.id_coordonne
WHERE client_id = %s AND valide
GROUP BY id_coordonne, c.date_achat
ORDER BY c.date_achat DESC, COUNT(c.id_commande) DESC LIMIT 1;"""

SELECT_MOST_USED_ADDRESS = """SELECT
    coordonnees.id_coordonne
FROM coordonnees
LEFT JOIN commande c ON c.adresse_livraison = coordonnees.id_coordonne OR c.adresse_facturation = coordonnees.id_coordonne
WHERE client_id = %s AND valide
GROUP BY id_coordonne, c.date_achat
ORDER BY COUNT(c.id_commande) DESC LIMIT 1;"""