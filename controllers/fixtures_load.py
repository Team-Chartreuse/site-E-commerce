#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql = '''DROP TABLE IF EXISTS 
    peinture, 
    ligne_panier,
    ligne_commande,
    commande,
    etat,
    utilisateur,
    categorie,
    couleur;
    '''
    mycursor.execute(sql)

    sql = '''
        CREATE TABLE IF NOT EXISTS utilisateur (
        id_utilisateur INT AUTO_INCREMENT,
        login VARCHAR(255),
        email VARCHAR(320), # la taille maximal d\'un mail est de 320 caractères, voir ci-dessous
        nom VARCHAR(255),
        password VARCHAR(255),
        role VARCHAR(255),
    
        PRIMARY KEY (id_utilisateur)
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO utilisateur (login, email, nom, password, role) VALUES
        ('meyer', 'tim@jmail.com', 'timothée', 'test', 'admin'),
        ('dulieux', 'dulieuxdit@arrowbase.dot', 'dudu', 'monsuperpassword', 'admin')
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS categorie (
        id_categorie INT AUTO_INCREMENT NOT NULL,
        nom_categorie VARCHAR(64) NOT NULL,
    
        PRIMARY KEY (id_categorie)
    );
    '''
    mycursor.execute(sql)

    sql = ''' 
    INSERT INTO categorie (nom_categorie) VALUES
        ('Peintures d''Intérieur'),
        ('Peintures d''Extérieur'),
        ('Peintures Spécialisées'),
        ('Apprêt'),
        ('Peintures Artistiques'),
        ('Peintures Écologiques');
    '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS etat (
        id_etat INT AUTO_INCREMENT,
        libelle VARCHAR(50),
        PRIMARY KEY (id_etat)
    );
    '''
    mycursor.execute(sql)

    sql = ''' 
        INSERT INTO etat (libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS peinture (
    id_peinture INT AUTO_INCREMENT,
    nom_peinture VARCHAR(50),
    volume_pot DECIMAL(5, 2),
    numero_melange INT,
    prix_peinture DECIMAL(15, 2),
    couleur_id INT,
    categorie_id INT,
    fournisseur VARCHAR(50),
    marque VARCHAR(50),
    image VARCHAR(128),

    PRIMARY KEY (id_peinture),
    FOREIGN KEY (couleur_id) REFERENCES couleur (id_couleur),
    FOREIGN KEY (categorie_id) REFERENCES categorie (id_categorie)
    );
     '''
    mycursor.execute(sql)
    sql = """
    INSERT INTO peinture 
    (nom_peinture, volume_pot, numero_melange, prix_peinture, couleur_id, categorie_id, fournisseur, marque, image)
    VALUES
        ('Peinture Premium Rouge Intérieur', 2.5, 101, 25.99, 1, 1, 'Team chartreuse', 'Team Chartreuse', 'paint_image1.jpg'),
        ('Bouclier Bleu Extérieur', 1.0, 102, 15.50, 2, 1, 'Eclat etoile', 'Eclat d\\'étoile', 'paint_image2.jpg'),
        ('Vert Écologique', 3.0, 103, 30.75, 3, 2, 'Team Chartreuse', 'Team Chartreuse', 'paint_image3.jpg'),
        ('Apprêt Jaune Universel', 2.0, 104, 20.00, 4, 2, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'paint_image4.jpg'),
        ('Harmonie Intérieure Rouge', 1.5, 105, 18.99, 1, 3, 'Bricodeco', 'Team Chartreuse', 'paint_image5.jpg'),
        ('ProShield Bleu Extérieur', 2.5, 106, 25.50, 2, 3, 'Bricodeco', 'Team Chartreuse', 'paint_image6.jpg'),
        ('Peinture Écologique GreenTech', 1.0, 107, 15.75, 3, 4, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'paint_image7.jpg'),
        ('Premium Jaune Extérieur', 3.0, 108, 32.00, 4, 4, 'Team Chartreuse', 'Team Chartreuse', 'paint_image8.jpg'),
        ('Harmonie Intérieure Rouge', 2.0, 109, 21.99, 1, 5, 'Adam Peinture', 'Team Chartreuse', 'paint_image9.jpg'),
        ('Ciel Étoilé Bleu', 1.5, 110, 17.50, 2, 5, 'Adam Peinture', 'Team Chartreuse', 'paint_image10.jpg'),
        ('Éclat Vert Artistique', 2.5, 111, 28.75, 3, 6, 'Adam Peinture', 'Team Chartreuse', 'paint_image11.jpg'),
        ('Apprêt Gris Universel', 2.0, 112, 22.00, 4, 6, 'Team Chartreuse', 'Team Chartreuse', 'paint_image12.jpg'),
        ('Harmonie Intérieure Rouge', 1.0, 113, 16.99, 1, 5, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'paint_image13.jpg'),
        ('ProShield Bleu Extérieur Plus', 3.0, 114, 31.50, 2, 6, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'paint_image14.jpg'),
        ('Lueur Écologique Vert Intérieur', 2.5, 115, 24.75, 3, 5, 'Adam Peinture', 'Team Chartreuse', 'paint_image15.jpg');
    """
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
    );
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande 
                 '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE IF NOT EXISTS ligne_commande (
        commande_id INT,
        peinture_id INT,
        prix DECIMAL(15, 2),
        quantite INT,
        PRIMARY KEY (commande_id, peinture_id),
        FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
    );
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande 
    '''
    mycursor.execute(sql)

    sql = '''
    CREATE TABLE IF NOT EXISTS ligne_panier (
    utilisateur_id INT,
    peinture_id INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id, peinture_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
    ); 
'''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
