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


@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
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

        commande_adresses = []

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
