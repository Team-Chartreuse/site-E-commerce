#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                            template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    SELECT 
        id_peinture, 
        utilisateur_id,
        couleur_id AS id_couleur,
        nom_peinture AS nom,
        prix_peinture AS prix,
        nom_couleur AS libelle_couleur,
        id_categorie,
        nom_categorie,
        quantite
    FROM ligne_panier
    JOIN peinture ON ligne_panier.peinture_id = peinture.id_peinture
    JOIN couleur ON peinture.couleur_id = couleur.id_couleur
    JOIN categorie ON peinture.categorie_id = categorie.id_categorie
    WHERE utilisateur_id = %s; 
    '''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        prix_total = 0
        for peinture in articles_panier:
            prix_total += peinture["prix"] * peinture["quantite"]
    else:
        prix_total = None

    # étape 2 : selection des adresses
    mycursor.execute("""SELECT * FROM coordonnees WHERE client_id = %s AND valide;""", (id_client,))
    adresses = mycursor.fetchall()

    return render_template('client/boutique/panier_validation_adresses.html'
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , validation=1
                           , adresses=adresses
                           # , id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    # None if not checked, a string elsewhere
    is_adresses_different = request.form.get("adresse_identique") is None

    id_adresse_facturation = request.form.get("id_adresse_facturation")

    id_adresse_livraison = id_adresse_facturation
    if is_adresses_different:
        id_adresse_livraison = request.form.get("id_adresse_livraison")

    id_client = session['id_user']
    sql = '''
    SELECT 
        peinture_id,
        utilisateur_id,
        quantite,
        date_ajout,
        prix_peinture AS prix
    FROM ligne_panier
    JOIN peinture ON ligne_panier.peinture_id = peinture.id_peinture
    WHERE utilisateur_id = %s;'''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()

    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')
    # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    str_date = str(datetime.now())
    a = datetime.strptime(str_date[:len(str_date) - 10], "%Y-%m-%d %H:%M")
    etat_id = '''
    SELECT id_etat
    FROM etat
    WHERE libelle LIKE '%en attente%'
    LIMIT 1
    '''
    mycursor.execute(etat_id)
    etat_id = mycursor.fetchone()
    print(etat_id)
    sql = '''INSERT INTO commande(date_achat, utilisateur_id, etat_id, adresse_facturation, adresse_livraison)
    VALUE (%s, %s, %s, %s, %s);'''
    mycursor.execute(sql, (a, id_client, etat_id['id_etat'], id_adresse_facturation, id_adresse_livraison))

    sql = '''SELECT LAST_INSERT_ID() AS last_insert_id FROM commande'''
    mycursor.execute(sql)
    last_insert_id = mycursor.fetchone()['last_insert_id']
    # numéro de la dernière commande
    for item in items_ligne_panier:
        print("hey !")
        sql = '''DELETE FROM ligne_panier WHERE peinture_id = %s;'''
        mycursor.execute(sql, item['peinture_id'])

        sql = '''
        INSERT INTO ligne_commande(commande_id, peinture_id, prix, quantite) 
        VALUE (%s, %s, %s, %s)
        '''
        mycursor.execute(sql, (last_insert_id, item['peinture_id'], item['prix'], item['quantite']))
    get_db().commit()
    flash(u'Commande ajoutée', 'alert-success')
    return redirect('/client/article/show')


@client_commande.route('/client/commande/show', methods=['get', 'post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    SELECT 
        date_achat,
        SUM(prix) AS prix_total,
        SUM(quantite) AS nbr_articles,
        libelle,
        id_commande
    FROM commande
    JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    JOIN etat ON commande.etat_id = etat.id_etat
    WHERE utilisateur_id = %s
    GROUP BY date_achat, libelle, etat_id, id_commande
    ORDER BY etat_id, date_achat DESC
    '''
    mycursor.execute(sql, id_client)

    sql = '''  selection des commandes ordonnées par état puis par date d'achat descendant '''
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande is not None:
        sql = '''
        SELECT
            peinture.nom_peinture AS nom,
            quantite,
            ligne_commande.prix,
            (peinture.prix_peinture * quantite) AS prix_ligne,
            categorie.id_categorie,
            categorie.nom_categorie,
            couleur.id_couleur,
            couleur.nom_couleur
        FROM ligne_commande
        JOIN peinture ON ligne_commande.peinture_id = peinture.id_peinture
        JOIN categorie ON peinture.categorie_id = categorie.id_categorie
        JOIN couleur ON peinture.couleur_id = couleur.id_couleur
        WHERE commande_id = %s
        '''
        mycursor.execute(sql, id_commande)
        articles_commande = mycursor.fetchall()
        for article in articles_commande:
            article['nb_declinaisons'] = 2

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )
