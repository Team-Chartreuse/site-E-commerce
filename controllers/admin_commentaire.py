#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__, template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article = request.args.get('id_article', None)
    sql_commentaires = '''
    SELECT U.id_utilisateur,
    C.peinture_id AS id_article,
    C.date_publication,
    C.valider,
    U.nom,
    C.commentaire
    FROM commentaire C
    INNER JOIN utilisateur U ON C.utilisateur_id = U.id_utilisateur
    WHERE C.peinture_id = %s
    ORDER BY C.date_publication ASC, U.id_utilisateur DESC;'''
    mycursor.execute(sql_commentaires, id_article)
    commentaires = mycursor.fetchall()
    sql_article = '''
    SELECT nom_peinture AS nom,
        id_peinture AS id_article
    FROM peinture
    WHERE id_peinture = %s;'''
    mycursor.execute(sql_article, id_article)
    article = mycursor.fetchone()
    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , article=article
                           )

@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    sql_check_response = '''SELECT COUNT(*) AS verif FROM commentaire WHERE peinture_id = %s AND date_publication = %s;'''
    tuple_verif = (id_article, date_publication)
    mycursor.execute(sql_check_response, tuple_verif)
    response_count = mycursor.fetchone()
    if response_count['verif'] == 1:
        sql1 = '''DELETE FROM commentaire
        WHERE peinture_id = %s
        AND date_publication = %s
        AND utilisateur_id = %s;
        '''
        tuple_delete1=(id_article, date_publication, id_utilisateur)
        mycursor.execute(sql1, tuple_delete1)
    elif response_count['verif'] > 1 and id_utilisateur == '1':
        sql2 = '''DELETE FROM commentaire
        WHERE peinture_id = %s
        AND date_publication = %s
        AND utilisateur_id = 1;
        '''
        tuple_delete2=(id_article, date_publication)
        mycursor.execute(sql2, tuple_delete2)
    elif response_count['verif'] > 1 and id_utilisateur != '1':
        sql3 = '''DELETE FROM commentaire
        WHERE peinture_id = %s
        AND date_publication = %s;
        '''
        tuple_delete3=(id_article, date_publication)
        mycursor.execute(sql3, tuple_delete3)

    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    mycursor = get_db().cursor()
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_article = request.args.get('id_article', None)
        date_publication = request.args.get('date_publication', None)
        sql_check_response = '''SELECT COUNT(*) AS verif FROM commentaire WHERE peinture_id = %s AND date_publication = %s;'''
        tuple_verif = (id_article, date_publication)
        mycursor.execute(sql_check_response, tuple_verif)
        response_count = mycursor.fetchone()
        if response_count['verif'] > 1:
            flash("Vous avez déjà répondu. Supprimer et recréer votre réponse.", "warning")
            return redirect('/admin/article/commentaires?id_article=' + id_article)
        return render_template('admin/article/add_commentaire.html', id_utilisateur=id_utilisateur, id_article=id_article, date_publication=date_publication)

    id_utilisateur = session['id_user']   #1 admin
    print(id_utilisateur)
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''INSERT INTO commentaire (date_publication, peinture_id, utilisateur_id, commentaire, valider)
             VALUES (%s, %s, %s, %s, 0)'''
    tuple_add=(date_publication, id_article, id_utilisateur, commentaire)
    mycursor.execute(sql, tuple_add)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_article = request.args.get('id_article', None)
    mycursor = get_db().cursor()
    sql = '''UPDATE commentaire SET valider=1 WHERE peinture_id=%s;'''
    mycursor.execute(sql, id_article)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)