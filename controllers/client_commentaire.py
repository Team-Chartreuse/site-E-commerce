#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article', None)
    id_client = session['id_user']
    ## partie 4
    # client_historique_add(id_article, id_client)

    sql = '''
    SELECT
        id_peinture AS id_article,
        nom_peinture AS nom,
        volume_pot,
        COUNT(note) AS nb_notes,
        CASE
            WHEN COUNT(note) > 0 THEN AVG(note)
            ELSE NULL
        END AS moyenne_notes,
        numero_melange,
        prix_peinture AS prix,
        couleur_id,
        categorie_id,
        fournisseur,
        marque,
        description,
        image,
        nom_couleur,
        nom_categorie
    FROM peinture
    JOIN couleur ON peinture.couleur_id = couleur.id_couleur
    JOIN categorie ON peinture.categorie_id = categorie.id_categorie
    LEFT JOIN note ON peinture.id_peinture = note.peinture_id
    WHERE id_peinture = %s;
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()

    nb_commentaires = {'nb_commentaires_total': 0, 'nb_commentaires_utilisateur': 0}
    commandes_articles = {'nb_commandes_article': 0}

    sql_commentaires = '''
        SELECT U.nom AS nom,
       C.peinture_id AS id_article,
       U.id_utilisateur,
       C.commentaire,
       C.date_publication,
       AVG(N.note) AS note_moyenne
FROM commentaire C
INNER JOIN utilisateur U ON U.id_utilisateur = C.utilisateur_id
LEFT JOIN note N ON N.utilisateur_id = U.id_utilisateur
WHERE C.peinture_id = %s
  AND (C.valider = 1 OR U.id_utilisateur = %s)
GROUP BY U.nom, C.peinture_id, U.id_utilisateur, C.commentaire, C.date_publication
ORDER BY C.date_publication ASC, U.id_utilisateur DESC;'''
    comm = (id_article, id_client)
    mycursor.execute(sql_commentaires, comm)
    commentaires = mycursor.fetchall()

    sql_commandes_articles = '''
    SELECT COUNT(*) AS commandes_articles
    FROM ligne_commande L
    INNER JOIN commande C ON C.id_commande = L.commande_id
    WHERE (L.peinture_id = %s AND C.id_commande = L.commande_id)
    AND C.utilisateur_id = %s;
    '''
    mycursor.execute(sql_commandes_articles, (id_article, id_client))
    commandes_articles['nb_commandes_article'] = mycursor.fetchone()['commandes_articles']

    sql_note = '''
    SELECT note,
    peinture_id AS id_article,
    utilisateur_id AS id_client
    FROM note
    WHERE peinture_id = %s AND utilisateur_id = %s;
    '''
    mycursor.execute(sql_note, (id_article, id_client))
    note = mycursor.fetchone()

    if note:
        note = note['note']

    sql_nb_commentaires = '''
    SELECT COUNT(*) AS nb_commentaires
    FROM commentaire
    WHERE peinture_id = %s;
    '''
    mycursor.execute(sql_nb_commentaires, id_article)
    nb_commentaires['nb_commentaires_total'] = mycursor.fetchone()['nb_commentaires']

    sql_nb_commentaires_individuel = '''
        SELECT COUNT(*) AS nb_commentaires
        FROM commentaire
        WHERE peinture_id = %s
        AND utilisateur_id = %s;
        '''
    mycursor.execute(sql_nb_commentaires_individuel, (id_article, id_client))
    nb_commentaires['nb_commentaires_utilisateur'] = mycursor.fetchone()['nb_commentaires']

    return render_template('client/article_info/article_details.html',
                           article=article,
                           commentaires=commentaires,
                           commandes_articles=commandes_articles,
                           note=note,
                           nb_commentaires=nb_commentaires)


@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    if commentaire == '':
        flash(u'Commentaire non pris en compte')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/article/details?id_article='+id_article)

    tuple_insert = (id_article, id_client, commentaire)
    sql = ''' INSERT INTO commentaire (date_publication, peinture_id, utilisateur_id, commentaire, valider)
VALUES (NOW(), %s, %s, %s, 0);
 '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    print(date_publication)
    sql = '''DELETE FROM commentaire
    WHERE peinture_id = %s
    AND date_publication = %s
    AND utilisateur_id = %s;'''
    tuple_delete=(id_article, date_publication, id_client)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    print(date_publication)

    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    print(note)
    print(type(note))
    if note is None:
        note = 0
    id_article = request.form.get('id_article', None)
    tuple_insert = (id_article, id_client, note)
    sql = ''' INSERT INTO note (peinture_id, utilisateur_id, note)
VALUES (%s, %s, %s); '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    if note is None or note == '':
        note = 0
    id_article = request.form.get('id_article', None)
    tuple_update = (note, id_article, id_client)
    sql = ''' UPDATE note
SET note = %s
WHERE peinture_id = %s
AND utilisateur_id = %s; '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    tuple_delete = (id_article, id_client)
    sql = ''' DELETE FROM note
WHERE peinture_id = %s
AND utilisateur_id = %s; '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)
