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

    mycursor.execute("DROP TABLE IF EXISTS ligne_panier;")
    mycursor.execute("DROP TABLE IF EXISTS ligne_commande;")
    mycursor.execute("DROP TABLE IF EXISTS commande;")
    mycursor.execute("DROP TABLE IF EXISTS etat;")
    mycursor.execute("DROP TABLE IF EXISTS coordonnees;")
    mycursor.execute("DROP TABLE IF EXISTS utilisateur;")
    mycursor.execute("DROP TABLE IF EXISTS peinture;")
    mycursor.execute("DROP TABLE IF EXISTS categorie;")
    mycursor.execute("DROP TABLE IF EXISTS couleur;")


    sql = '''CREATE TABLE IF NOT EXISTS categorie (
    id_categorie INT AUTO_INCREMENT NOT NULL,
    nom_categorie VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_categorie)
);
'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS couleur (
    id_couleur INT AUTO_INCREMENT NOT NULL,
    nom_couleur VARCHAR(128) NOT NULL,

    PRIMARY KEY (id_couleur)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS peinture (
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
    stock INT,

    PRIMARY KEY (id_peinture),
    FOREIGN KEY (couleur_id) REFERENCES couleur (id_couleur),
    FOREIGN KEY (categorie_id) REFERENCES categorie (id_categorie)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(320), # la taille maximal d'un mail est de 320 caractères, voir ci-dessous
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif CHAR(1),

    PRIMARY KEY (id_utilisateur)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS etat (
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);
'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS ligne_commande (
    commande_id INT,
    peinture_id INT,
    prix DECIMAL(15, 2),
    quantite INT,
    PRIMARY KEY (commande_id, peinture_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
);'''
    mycursor.execute(sql)

    sql = '''CREATE TABLE IF NOT EXISTS ligne_panier (
    utilisateur_id INT,
    peinture_id INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id, peinture_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
);'''
    mycursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS coordonnees (
    id_coordonne INT AUTO_INCREMENT,
    client_id INT REFERENCES utilisateur (id_utilisateur),
    num_rue_nom TEXT,
    ville VARCHAR(128),
    code_postal INT,
    nom_prenom VARCHAR(64),

    PRIMARY KEY (id_coordonne, client_id)
);"""
    mycursor.execute(sql)

    sql = '''INSERT INTO etat (libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');'''
    mycursor.execute(sql)

    sql = """INSERT INTO categorie (nom_categorie) VALUES
    ('Peintures d''Intérieur'),
    ('Peintures d''Extérieur'),
    ('Peintures Spécialisées'),
    ('Apprêt'),
    ('Peintures Artistiques'),
    ('Peintures Écologiques');"""
    mycursor.execute(sql)

    sql = '''INSERT INTO couleur (nom_couleur) VALUES
    ('Chartreuse'),
    ('Bleu'),
    ('Viva magenta'),
    ('Jaune');
'''
    mycursor.execute(sql)

    sql = '''INSERT INTO peinture (nom_peinture, volume_pot, numero_melange, prix_peinture, couleur_id, categorie_id, fournisseur, marque, image, stock) VALUES
    ('Peinture Premium Rouge Intérieur', 2.5, 101, 25.99, 1, 1, 'Team chartreuse', 'Team Chartreuse', 'peinture_premium_rouge_interieur.png', 5),
    ('Bouclier Bleu Extérieur', 1.0, 102, 15.50, 2, 1, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'bouclier_bleu_exterieur.png', 8),
    ('Vert Écologique', 3.0, 103, 30.75, 3, 2, 'Team Chartreuse', 'Team Chartreuse', 'vert_ecologique.png', 11),
    ('Apprêt Jaune Universel', 2.0, 104, 20.00, 4, 2, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'appret_jaune_universel.png', 58),
    ('Harmonie Intérieure Rouge', 1.5, 105, 18.99, 1, 3, 'Bricodeco', 'Team Chartreuse', 'harmonie_interieure_rouge.png', 26),
    ('ProShield Bleu Extérieur', 2.5, 106, 25.50, 2, 3, 'Bricodeco', 'Team Chartreuse', 'proshield_bleu_exterieur.png', 3),
    ('Peinture Écologique GreenTech', 1.0, 107, 15.75, 3, 4, 'Eclat d\\'étoile', 'Eclat d\\'étoile', 'peinture_ecologique_greentech.png', 89),
    ('Premium Jaune Extérieur', 3.0, 108, 32.00, 4, 4, 'Team Chartreuse', 'Team Chartreuse', 'premium_jaune_exterieur.png', 7),
    ('Harmonie Intérieure Rouge', 2.0, 109, 21.99, 1, 5, 'Adam Peinture', 'Team Chartreuse', 'harmonie_interieure_rouge.png', 4),
    ('Ciel Étoilé Bleu', 1.5, 110, 17.50, 2, 5, 'Adam Peinture', 'Team Chartreuse', 'ciel_etoile_bleu.png', 56),
    ('Éclat Vert Artistique', 2.5, 111, 28.75, 3, 6, 'Adam Peinture', 'Team Chartreuse', 'eclat_vert_artistique.png', 23),
    ('Apprêt Gris Universel', 2.0, 112, 22.00, 4, 6, 'Team Chartreuse', 'Team Chartreuse', 'appret_gris_universel.png', 32),
    ('Lueur Écologique Vert Intérieur', 2.5, 115, 24.75, 3, 5, 'Adam Peinture', 'Team Chartreuse', 'lueur_ecologique_vert_interieur.png',7),
    ('Ecru', 1.5, 117, 15.55, 4, 6, 'Adam Peinture', 'Team Chartreuse', 'ecru.png', 89),
    ('Chartreuse', 3.5, 127, 32.99, 1, 3, 'Team Chartreuse', 'Team Chartreuse', 'chartreuse.png', 10);'''
    mycursor.execute(sql)

    sql = '''INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
    (1,'admin','admin@admin.fr',
    'pbkdf2:sha256:600000$olNVM35LlMvBbE12$8e04be309fd45d72c684f5caa3804afbb77bfb3f6bec5fdd5a9a86165cd7092a',
    'ROLE_admin','admin'),
    (2,'client','client@client.fr',
    'pbkdf2:sha256:600000$dYjw0xxqdHAIA1GO$eaef95ecf21a51f50769bb3b45cbc59edebf575bbefe91a52c16b8525a6ed3c2',
    'ROLE_client','client'),
    (3,'client2','client2@client2.fr',
    'pbkdf2:sha256:600000$LLJIBGNbPjJ63uJM$b774cf95df80c722d09f957b1831d82689153544916b460410e2d0de73337db0',
    'ROLE_client','client2');
'''
    mycursor.execute(sql)

    mycursor.execute('''ALTER TABLE peinture ADD COLUMN description VARCHAR(1024);''')

    sql = '''INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
    (1, DATE('2024-02-08'), 2, 2),
    (2, DATE('2024-02-07'), 3, 1);'''
    mycursor.execute(sql)

    sql = '''INSERT INTO ligne_commande (commande_id, peinture_id, prix, quantite) VALUES
    (2, 15, 32.99, 2),
    (2, 5, 18.99, 3),
    (1, 1, 25.99, 1),
    (1, 5, 18.99, 5),
    (1, 10, 17.50, 2);'''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
