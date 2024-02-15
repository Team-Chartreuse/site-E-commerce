#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
# from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''SELECT
    p.nom_peinture AS nom,
    p.id_peinture AS id_article,
    c.nom_categorie AS libelle,
    c.id_categorie AS type_article_id,
    p.prix_peinture AS prix,
    p.stock AS stock,
    p.image AS image
FROM peinture p
INNER JOIN categorie c ON c.id_categorie = p.categorie_id;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()

    return render_template('admin/article/add_article.html'
                           # ,types_article=type_article,
                           # ,couleurs=colors
                           # ,tailles=tailles
                           )


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()

    nom = request.form.get('nom', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    if image:
        filename = 'img_upload' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
    else:
        print("erreur")
        filename = None

    sql = '''  requête admin_article_2 '''

    tuple_add = (nom, filename, prix, type_article_id, description)
    print(tuple_add)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    print(u'article ajouté , nom: ', nom, ' - type_article:', type_article_id, ' - prix:', prix,
          ' - description:', description, ' - image:', image)
    message = u'article ajouté , nom:' + nom + '- type_article:' + type_article_id + ' - prix:' + prix + ' - description:' + description + ' - image:' + str(
        image)
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = ''' requête admin_article_3 '''
    mycursor.execute(sql, id_article)
    nb_declinaison = mycursor.fetchone()
    if nb_declinaison['nb_declinaison'] > 0:
        message = u'il y a des declinaisons dans cet article : vous ne pouvez pas le supprimer'
        flash(message, 'alert-warning')
    else:
        sql = ''' requête admin_article_4 '''
        mycursor.execute(sql, id_article)
        article = mycursor.fetchone()
        print(article)
        image = article['image']

        sql = ''' requête admin_article_5  '''
        mycursor.execute(sql, id_article)
        get_db().commit()
        if image != None:
            os.remove('static/images/' + image)

        print("un article supprimé, id :", id_article)
        message = u'un article supprimé, id : ' + id_article
        flash(message, 'alert-success')

    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()

    sql = '''SELECT
    p.image AS image,
    p.id_peinture AS id_article,
    p.nom_peinture AS nom,
    p.prix_peinture AS prix,
    p.stock AS stock,
    IFNULL(p.description, 'No description')
FROM peinture p
WHERE p.id_peinture = %s
LIMIT 1;'''

    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    print(article)

    sql = '''SELECT c.id_categorie AS id_type_article, c.nom_categorie AS libelle FROM categorie c;'''

    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # sql = '''
    # requête admin_article_6
    # '''
    # mycursor.execute(sql, id_article)
    # declinaisons_article = mycursor.fetchall()

    return render_template('admin/article/edit_article.html'
                           , article=article
                           , types_article=types_article
                           #  ,declinaisons_article=declinaisons_article
                           )


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom')
    id_article = request.form.get('id_article')
    image = request.files.get('image', '')
    stock = request.form.get('stock', '')
    type_article_id = request.form.get('type_article_id', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description')

    sql = '''SELECT image FROm peinture WHERE id_peinture = %s;'''

    mycursor.execute(sql, id_article)
    image_nom = mycursor.fetchone()
    image_nom = image_nom['image']
    if image:
        if image_nom != "" and image_nom is not None and os.path.exists(
                os.path.join(os.getcwd() + "/static/images/", image_nom)):
            os.remove(os.path.join(os.getcwd() + "/static/images/", image_nom))
        # filename = secure_filename(image.filename)
        if image:
            filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
            image.save(os.path.join('static/images/', filename))
            image_nom = filename

    sql = '''UPDATE peinture
SET
    nom_peinture = %s,
    image = %s,
    prix_peinture = %s,
    categorie_id = %s,
    description = %s,
    stock = %s
WHERE
    peinture.id_peinture = %s;
'''
    mycursor.execute(sql, (nom, image_nom, prix, type_article_id, description, stock, id_article))

    get_db().commit()
    if image_nom is None:
        image_nom = ''
    message = u'article modifié , nom:' + nom + '- type_article :' + type_article_id + ' - prix:' + prix + ' - image:' + image_nom + ' - description: ' + description
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    article = []
    commentaires = {}
    return render_template('admin/article/show_avis.html'
                           , article=article
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
