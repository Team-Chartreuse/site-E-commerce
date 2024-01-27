#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

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
        nom_categorie
    FROM peinture
    JOIN couleur
    ON peinture.couleur_id = couleur.id_couleur
    JOIN categorie
    ON peinture.categorie_id = categorie.id_categorie;
    '''
    list_param = []
    condition_and = ""
    # utilisation du filtre
    sql3 = ''' prise en compte des commentaires et des notes dans le SQL    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    print(articles)

    # pour le filtre
    types_article = []

    articles_panier = []

    if len(articles_panier) >= 1:
        sql = ''' calcul du prix total du panier '''
        prix_total = None
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           #, prix_total=prix_total
                           , items_filtre=types_article
                           )
