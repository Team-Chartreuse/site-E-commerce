#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db
from controllers.requetes import SELECT_LAST_ADDRESS_USED, SELECT_MOST_USED_ADDRESS

client_coordonnee = Blueprint('client_coordonnee', __name__,
                              template_folder='templates')


@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    mycursor.execute("""SELECT * FROM utilisateur WHERE id_utilisateur = %s""", (id_client,))
    utilisateur = mycursor.fetchone()

    mycursor.execute("""
    SELECT
    coordonnees.*,
    COUNT(c.id_commande) as nb_commandes
FROM coordonnees
LEFT JOIN commande c ON c.adresse_facturation = coordonnees.id_coordonne OR c.adresse_livraison = coordonnees.id_coordonne
WHERE client_id = %s
GROUP BY coordonnees.id_coordonne, c.date_achat, valide
ORDER BY valide DESC, c.date_achat DESC, COUNT(c.id_commande) DESC;""", (id_client,))
    adresses = mycursor.fetchall()

    sql = """SELECT * FROM adresse_favorite WHERE id_client = %s;"""
    mycursor.execute(sql, (id_client,))
    id_adresse_favorite = mycursor.fetchone()
    if id_adresse_favorite is None:
        mycursor.execute(SELECT_LAST_ADDRESS_USED, (id_client,))
        id_adresse_favorite = mycursor.fetchone()["id_coordonne"]
    else:
        id_adresse_favorite = id_adresse_favorite["id_adresse"]

    mycursor.execute("""SELECT COUNT(*) AS t FROM coordonnees WHERE client_id = %s AND valide;""", (id_client,))
    nb_adresses = mycursor.fetchone()["t"]

    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           , id_adresse_favorite=id_adresse_favorite
                           )


@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    mycursor.execute("""SELECT * FROM utilisateur WHERE id_utilisateur = %s;""", (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('client/coordonnee/edit_coordonnee.html'
                           , utilisateur=utilisateur
                           )


@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    mycursor.execute("""SELECT 1 FROM utilisateur WHERE (email = %s OR login = %s) AND id_utilisateur != %s;""",
                     (email, login, id_client))
    utilisateur = mycursor.fetchone()

    if utilisateur:
        flash(u'votre cet Email ou ce Login existe déjà pour un autre utilisateur', 'alert-warning')

        mycursor.execute("""SELECT * FROM utilisateur WHERE id_utilisateur = %s;""", (id_client,))
        utilisateur = mycursor.fetchone()
        return render_template('client/coordonnee/edit_coordonnee.html'
                               , utilisateur=utilisateur
                               )

    mycursor.execute(
        """UPDATE utilisateur SET nom = %s, login = %s, email = %s WHERE id_utilisateur = %s;""",
        (nom, login, email, id_client)
    )
    get_db().commit()

    # Edit session
    session['login'] = login

    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse', methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.form.get('id_adresse')

    mycursor.execute(
        """SELECT 1 FROM commande WHERE adresse_livraison = %s OR adresse_livraison = %s;""",
        (id_adresse, id_adresse)
    )
    commandes = mycursor.fetchall()

    if len(commandes) > 0:
        mycursor.execute(
            """UPDATE coordonnees SET valide=0 WHERE id_coordonne = %s AND client_id = %s;""",
            (id_adresse, id_client)
        )
    else:
        mycursor.execute("""DELETE FROM coordonnees WHERE id_coordonne = %s;""", (id_adresse,))

    mycursor.execute("""SELECT * FROM adresse_favorite WHERE id_client = %s;""", (id_client,))
    adresse_favorite = mycursor.fetchone()
    if adresse_favorite is not None and str(adresse_favorite["id_adresse"]) == str(id_adresse):
        mycursor.execute(SELECT_MOST_USED_ADDRESS, (id_client,))
        id_most_used_address = mycursor.fetchone()["id_coordonne"]
        mycursor.execute("UPDATE adresse_favorite SET id_adresse = %s WHERE id_client = %s;",
                         (id_most_used_address, id_client))
    elif adresse_favorite is None:
        mycursor.execute(SELECT_LAST_ADDRESS_USED, (id_client,))
        id_most_used_address = mycursor.fetchone()
        mycursor.execute("UPDATE adresse_favorite SET id_adresse = %s WHERE id_client = %s;",
                         (id_most_used_address, id_client))

    get_db().commit()

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

    mycursor.execute("""SELECT COUNT(*) AS c FROM coordonnees WHERE client_id = %s AND valide;""", (id_client,))
    nb_addresses = mycursor.fetchone()

    if nb_addresses is not None and int(nb_addresses["c"]) < 4:
        mycursor.execute(
            """INSERT INTO coordonnees (client_id, num_rue_nom, ville, code_postal, nom_prenom, valide)
        VALUE (%s, %s, %s, %s, %s, true);""",
            (
                id_client,
                rue,
                ville,
                code_postal,
                nom,
            )
        )
        get_db().commit()
    else:
        flash(u'Vous ne pouvez pas ajouter plus de 4 adresses', 'alert-warning')

    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')


    mycursor.execute("""SELECT * FROM coordonnees WHERE client_id = %s AND id_coordonne = %s;""",
                     (id_client, id_adresse))
    adresse = mycursor.fetchone()

    mycursor.execute("""SELECT * FROM utilisateur WHERE id_utilisateur = %s;""", (id_client,))
    utilisateur = mycursor.fetchone()

    return render_template('/client/coordonnee/edit_adresse.html'
                           , utilisateur=utilisateur
                           , adresse=adresse
                           )


@client_coordonnee.route('/client/coordonnee/edit_adresse', methods=['POST'])
def client_coordonnee_edit_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_coordonne')

    mycursor.execute(
        """SELECT 1 FROM commande WHERE adresse_livraison = %s OR adresse_livraison = %s;""",
        (id_adresse, id_adresse)
    )
    commandes = mycursor.fetchall()
    if len(commandes) < 1:
        mycursor.execute("""
            UPDATE coordonnees
            SET
                nom_prenom = %s,
                num_rue_nom = %s,
                code_postal = %s,
                ville = %s
            WHERE
                id_coordonne = %s;""", (nom, rue, code_postal, ville, id_adresse,))
    else:
        # On doit créer une nouvelle adresse et invalider l'ancienne
        mycursor.execute("UPDATE coordonnees SET valide = false WHERE id_coordonne = %s;", (id_adresse,))
        mycursor.execute(
            """INSERT INTO coordonnees (client_id, num_rue_nom, ville, code_postal, nom_prenom, valide)
        VALUE (%s, %s, %s, %s, %s, true);""",
            (id_client, rue, ville, code_postal, nom)
        )
        get_db().commit()

    get_db().commit()

    return redirect('/client/coordonnee/show')
