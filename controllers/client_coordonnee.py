#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                              template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    mycursor.execute("""SELECT * FROM utilisateur WHERE id_utilisateur = %s""", (id_client,))
    utilisateur = mycursor.fetchone()

    mycursor.execute("""SELECT * FROM coordonnees WHERE client_id = %s""", (id_client,))
    adresses = mycursor.fetchall()

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=len(adresses)
                           )


# TODO
@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    return render_template('client/coordonnee/edit_coordonnee.html'
                           # ,utilisateur=utilisateur
                           )


# TODO
@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    utilisateur = None
    if utilisateur:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')
        return render_template('client/coordonnee/edit_coordonnee.html'
                               # , user=user
                               )

    get_db().commit()
    return redirect('/client/coordonnee/show')


# TODO
@client_coordonnee.route('/client/coordonnee/delete_adresse', methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.form.get('id_adresse')

    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    mycursor.execute("""SELECT * FROM utilisateur WHERE id_utilisateur = %s;""", (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/add_adresse.html', utilisateur=utilisateur)


@client_coordonnee.route('/client/coordonnee/add_adresse', methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    mycursor.execute("""SELECT COUNT(*) AS c FROM coordonnees WHERE client_id = %s;""", (id_client,))
    nb_addresses = mycursor.fetchone()

    if nb_addresses is not None and int(nb_addresses["c"]) < 4:
        mycursor.execute(
            """INSERT INTO coordonnees (client_id, num_rue_nom, ville, code_postal, nom_prenom)
        VALUE (%s, %s, %s, %s, %s);""",
            (
                id_client,
                rue,
                ville,
                code_postal,
                nom
            )
        )
        get_db().commit()
    else:
        flash(u'Vous ne pouvez pas ajouter plus de 4 adresses', 'alert-warning')

    return redirect('/client/coordonnee/show')


# TODO
@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    return render_template('/client/coordonnee/edit_adresse.html'
                           # ,utilisateur=utilisateur
                           # ,adresse=adresse
                           )


# TODO
@client_coordonnee.route('/client/coordonnee/edit_adresse', methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    return redirect('/client/coordonnee/show')
