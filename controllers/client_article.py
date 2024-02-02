#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():             # remplace client_index
    mycursor = get_db().cursor()
    id_client = session.get('id_user', '')

    sql = '''
    SELECT
        id_peinture AS id_article,
        nom_peinture AS nom,
        volume_pot,
        numero_melange,
        prix_peinture AS prix,
        couleur_id,
        categorie_id,
        fournisseur,
        marque,
        image,
        nom_couleur,
        nom_categorie,
        stock
    FROM peinture
    JOIN couleur
    ON peinture.couleur_id = couleur.id_couleur
    JOIN categorie
    ON peinture.categorie_id = categorie.id_categorie
    '''

    list_param = []
    condition = []

    if session.get('filter_word', None):
        condition.append("nom_peinture LIKE %s")
        list_param.append(f"%{session['filter_word']}%")
    if session.get('filter_prix_min', None) and session.get('filter_prix_max', None):
        condition.append("prix_peinture BETWEEN %s AND %s")
        list_param.extend([float(session['filter_prix_min']), float(session['filter_prix_max'])])
    if session.get('filter_couleur', None):
        condition.append("couleur_id IN ({})".format(','.join(['%s'] * len(session['filter_couleur']))))
        list_param.extend([int(x) for x in session['filter_couleur']])
    if session.get('filter_categorie', None):
        condition.append("categorie_id IN ({})".format(','.join(['%s'] * len(session['filter_categorie']))))
        list_param.extend([int(x) for x in session['filter_categorie']])

    condition_and = ""
    if len(condition) > 0:
        condition_and = " WHERE " + " AND ".join(condition)
    # utilisation du filtre
    sql3 = ''' prise en compte des commentaires et des notes dans le SQL    '''  # TODO
    print(sql+condition_and, list_param)
    mycursor.execute(sql+condition_and, tuple(list_param))
    articles = mycursor.fetchall()

    # pour le filtre
    sql2 = '''
    SELECT 
        id_couleur,
        nom_couleur AS libelle
    FROM couleur;
    '''
    mycursor.execute(sql2)
    types_couleur = mycursor.fetchall()
    sql2 = '''
    SELECT 
        id_categorie,
        nom_categorie AS libelle
    FROM categorie;
    '''
    mycursor.execute(sql2)
    categorie = mycursor.fetchall()

    # Fetch des articles du panier
    sql = '''SELECT
    l.*,
    p.prix_peinture AS prix,
    p.stock AS stock,
    p.nom_peinture AS nom
FROM
    ligne_panier l
LEFT JOIN peinture p on l.peinture_id = p.id_peinture
WHERE
    l.utilisateur_id = %s;'''

    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:

        sql = '''SELECT
    SUM(p.prix_peinture * l.quantite) as total
FROM
    ligne_panier l
LEFT JOIN peinture p on l.peinture_id = p.id_peinture
WHERE
    l.utilisateur_id = %s;'''

        mycursor.execute(sql, id_client)
        res = mycursor.fetchall()
        if res and len(res) > 0:
            prix_total = res[0]['total']
    else:
        prix_total = None  # FIXME wtf?
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           # , prix_total=prix_total
                           , filtre_couleur=types_couleur
                           , filtre_categorie=categorie
                           )
