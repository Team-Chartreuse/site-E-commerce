#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                           template_folder='templates')


@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['GET', 'POST'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']

    sql = '''SELECT
    u.login,
    commande.date_achat AS date_achat,
    SUM(lc.quantite) AS nbr_articles,
    SUM(lc.prix * lc.quantite) AS prix_total,
    e.libelle AS libelle,
    e.id_etat AS etat_id,
    commande.id_commande AS id_commande
FROM
    commande
INNER JOIN ligne_commande lc ON lc.commande_id = commande.id_commande
INNER JOIN etat e ON e.id_etat = commande.etat_id
INNER JOIN utilisateur u ON u.id_utilisateur = commande.utilisateur_id
GROUP BY commande.id_commande, e.id_etat
ORDER BY e.id_etat, prix_total;'''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    client = None
    id_commande = request.args.get('id_commande', None)
    print("id_commande: ", id_commande)
    if id_commande:  # != None est inutile (d'après PyCharm)

        sql = '''SELECT
    lc.quantite AS quantite,
    lc.prix AS prix,
    lc.quantite,
    lc.prix * lc.quantite AS prix_ligne,
    p.nom_peinture AS nom
FROM ligne_commande lc
INNER JOIN peinture p ON p.id_peinture = lc.peinture_id
WHERE lc.commande_id = %s
ORDER BY lc.prix * lc.quantite;'''

        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        sql = '''SELECT u.*
FROM ligne_commande lc
INNER JOIN commande c ON lc.commande_id = c.id_commande
INNER JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
WHERE lc.commande_id = %s;'''
        mycursor.execute(sql, (id_commande,))
        client = mycursor.fetchone()

        sql = '''SELECT
                                    id_coordonne as id_adresse_livraison,
                                    nom_prenom as nom_livraison,
                                    num_rue_nom as rue_livraison,
                                    code_postal as code_postal_livraison,
                                    ville as ville_livraison
                                FROM coordonnees
                                INNER JOIN commande c ON c.adresse_livraison = coordonnees.id_coordonne
                                WHERE c.id_commande = %s;'''
        mycursor.execute(sql, (id_commande,))
        commande_livraison = mycursor.fetchone()
        print(commande_livraison)
        if commande_livraison is None:
            flash("Vous n'avez pas d'adresse de livraison pour cette commande", 'alert-warning')
            return redirect('/client/commande/show')
        commande_adresses = commande_livraison

        sql = '''SELECT
                            id_coordonne as id_adresse_facturation,
                            nom_prenom as nom_facturation,
                            num_rue_nom as rue_facturation,
                            code_postal as code_postal_facturation,
                            ville as ville_facturation
                        FROM coordonnees
                        INNER JOIN commande c ON c.adresse_facturation = coordonnees.id_coordonne
                        WHERE c.id_commande = %s;'''
        mycursor.execute(sql, (id_commande,))
        commande_facturation: dict = mycursor.fetchone()
        if commande_facturation is None:
            flash("Vous n'avez pas d'adresse de facturation pour cette commande", 'alert-warning')
            return redirect('/client/commande/show')

        if commande_facturation["id_adresse_facturation"] == commande_livraison["id_adresse_livraison"]:
            commande_adresses["adresse_identique"] = True
        else:
            for (k, v) in commande_facturation.items():
                commande_adresses[k] = v

    print(articles_commande)
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           , client=client
                           )


@admin_commande.route('/admin/commande/valider', methods=['get', 'post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id:  # != None est inutile (d'après PyCharm)
        print(commande_id)
        sql = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s;'''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')
