#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                        template_folder='templates')

@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()

    labels=[]
    values=[]

    sql_nb_type_peinture = '''
    SELECT 
    COUNT(DISTINCT id_categorie) AS types_articles_nb 
    FROM categorie;
    '''
    mycursor.execute(sql_nb_type_peinture)
    types_articles_nb = mycursor.fetchone()

    lignes = '''
    SELECT
    t.nom_categorie AS libelle,
    t.id_categorie AS id_type_article,
    COUNT(DISTINCT p.id_peinture) AS nbr_articles
    FROM
    categorie t
    INNER JOIN
    peinture p ON t.id_categorie = p.categorie_id
    GROUP BY
    t.id_categorie
    ORDER BY t.nom_categorie ASC;'''
    mycursor.execute(lignes)
    lignes = mycursor.fetchall()

    sql_nb_peinture = '''
    SELECT COUNT(DISTINCT id_peinture) AS nbr_articles
    FROM peinture;'''
    mycursor.execute(sql_nb_peinture)
    nbr_articles = mycursor.fetchone()

#    lignes = '''
#        SELECT
#        t.nom_categorie AS libelle,
#        t.id_categorie AS id_type_article,
#        AVG(n.note) AS nbr_articles
#    FROM
#        note n
#    INNER JOIN
#        peinture p ON t.id_categorie = p.categorie_id
#    GROUP BY
#        t.id_categorie, t.nom_categorie
#    ORDER BY t.nom_categorie ASC;'''
#    mycursor.execute(lignes)
#    lignes = mycursor.fetchall()
#
#    for ligne in lignes:
#        if ligne['nbr_articles'] is None:
#            ligne['nbr_articles'] = 0

    if nbr_articles is None:
        nbr_articles = 0

    # Remplir les libellés et les valeurs à partir des résultats de la requête SQL
    for ligne in lignes:
        labels.append(ligne['libelle'])  # Ajouter le libellé à la liste des libellés
        values.append(ligne['nbr_articles'])  # Ajouter la valeur à la liste des valeurs

    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , labels=labels
                           , values=values
                           , types_articles_nb=types_articles_nb
                           , nbr_articles=nbr_articles
                           , lignes=lignes)


# sujet 3 : adresses


@admin_dataviz.route('/admin/dataviz/etat2')
def show_dataviz_map():
    # mycursor = get_db().cursor()
    # sql = '''    '''
    # mycursor.execute(sql)
    # adresses = mycursor.fetchall()

    #exemples de tableau "résultat" de la requête
    adresses =  [{'dep': '25', 'nombre': 1}, {'dep': '83', 'nombre': 1}, {'dep': '90', 'nombre': 3}]

    # recherche de la valeur maxi "nombre" dans les départements
    # maxAddress = 0
    # for element in adresses:
    #     if element['nbr_dept'] > maxAddress:
    #         maxAddress = element['nbr_dept']
    # calcul d'un coefficient de 0 à 1 pour chaque département
    # if maxAddress != 0:
    #     for element in adresses:
    #         indice = element['nbr_dept'] / maxAddress
    #         element['indice'] = round(indice,2)

    print(adresses)

    return render_template('admin/dataviz/dataviz_etat_map.html'
                           , adresses=adresses
                          )


