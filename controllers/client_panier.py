#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__, template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    # ---------
    id_declinaison_article = request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

    # ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    sql = '''SELECT
    *
FROM couleur
LEFT JOIN peinture p on couleur.id_couleur = p.couleur_id
WHERE
    id_peinture = %s;'''

    mycursor.execute(sql, id_article)
    declinaisons = mycursor.fetchall()
    print(declinaisons)
    print("id_article = " + str(id_article))
    if len(declinaisons) == 1:
        id_declinaison_article = declinaisons[0]['id_peinture']
    elif len(declinaisons) == 0:
        abort("pb nb de declinaison")
    else:
        sql = '''  INSERT INTO ligne_panier (utilisateur_id, peinture_id, quantite, date_ajout)
         VALUE ()''' # TODO demander quelle déclinaison choisir
        # tuple_insert_ligne = (declinaisons[])
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        return render_template('client/boutique/declinaison_article.html'
                                   , declinaisons=declinaisons
                                   , quantite=quantite
                                   , article=article)

    # ajout dans le panier d'un article
    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND peinture_id = %s;'''
    mycursor.execute(sql, (id_client, id_article))

    is_article_already_in = len(mycursor.fetchall()) > 0

    if is_article_already_in:
        sql = '''UPDATE ligne_panier SET quantite = quantite + 1 WHERE utilisateur_id = %s AND peinture_id = %s;'''
        mycursor.execute(sql, (id_client, id_article))

        # Retirer un article du stock
        sql = '''UPDATE peinture SET stock = stock - 1 WHERE id_peinture = %s;'''
        mycursor.execute(sql, id_article)
    else:
        sql = "INSERT INTO ligne_panier (utilisateur_id, peinture_id, quantite, date_ajout) VALUE  (%s, %s, %s, NOW());"
        mycursor.execute(sql, (id_client, id_article, quantite))

        # Retirer des articles du stock
        sql = '''UPDATE peinture SET stock = stock - %s WHERE id_peinture = %s;'''
        mycursor.execute(sql, (quantite, id_article))

    get_db().commit()

    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', '')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = '''SELECT
    l.*
FROM
    ligne_panier l
LEFT JOIN peinture p on l.peinture_id = p.id_peinture
WHERE
    l.utilisateur_id = %s
    AND l.peinture_id = %s;'''

    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()

    if not (article_panier is None) and int(article_panier['quantite']) > 1:
        sql = '''UPDATE ligne_panier SET quantite = quantite - 1 WHERE utilisateur_id = %s AND peinture_id = %s;'''
        mycursor.execute(sql, (id_client, id_article))
    else:
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND peinture_id = %s;'''
        mycursor.execute(sql, (id_client, id_article))

    # mise à jour du stock de l'article disponible
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = '''SELECT *
FROM
    ligne_panier
WHERE
    utilisateur_id = %s;'''

    mycursor.execute(sql, client_id)

    items_panier = mycursor.fetchall()
    for item in items_panier:
        print(item)
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND peinture_id = %s;'''
        mycursor.execute(sql, (client_id, item["peinture_id"]))
        sql2 = '''UPDATE peinture SET stock = stock + %s WHERE id_peinture = %s;'''
        mycursor.execute(sql2, (item["quantite"], item["peinture_id"]))
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get("id_article", "")
    # id_declinaison_article = request.form.get('id_declinaison_article')

    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND peinture_id = %s;'''
    mycursor.execute(sql, (id_client, id_article))
    lines = mycursor.fetchall()
    if len(lines) < 1:
        return redirect('/client/article/show')

    line = lines[0]

    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND peinture_id = %s;'''
    mycursor.execute(sql, (id_client, id_article))
    sql2 = '''UPDATE peinture SET stock = stock + %s WHERE id_peinture = %s;'''
    mycursor.execute(sql2, (line["quantite"], id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_couleur = request.form.getlist('filter_couleur')
    filter_categorie = request.form.getlist('filter_categorie')

    # test des variables puis
    # mise en session des variables
    if filter_word:
        session['filter_word'] = filter_word
    if filter_prix_min:
        session['filter_prix_min'] = filter_prix_min
    if filter_prix_max:
        session['filter_prix_max'] = filter_prix_max
    if len(filter_couleur) > 0:
        session['filter_couleur'] = filter_couleur
    if len(filter_categorie) > 0:
        session['filter_categorie'] = filter_categorie

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression des variables en session
    print("suppr filtre")
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_couleur', None)
    session.pop('filter_categorie', None)
    return redirect('/client/article/show')
