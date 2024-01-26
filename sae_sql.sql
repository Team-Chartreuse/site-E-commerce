DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS peinture;
DROP TABLE IF EXISTS categorie;
DROP TABLE IF EXISTS couleur;


CREATE TABLE IF NOT EXISTS categorie (
    id_categorie INT AUTO_INCREMENT NOT NULL,
    nom_categorie VARCHAR(64) NOT NULL,

    PRIMARY KEY (id_categorie)
);

CREATE TABLE IF NOT EXISTS couleur (
    id_couleur INT AUTO_INCREMENT NOT NULL,
    nom_couleur VARCHAR(128) NOT NULL,

    PRIMARY KEY (id_couleur)
);

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

CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(320), # la taille maximal d'un mail est de 320 caractères, voir ci-dessous
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif CHAR(1),

    PRIMARY KEY (id_utilisateur)
);
#        Emails limitations:
# Section 3 says: (from erratum 1003) In addition to restrictions on syntax, there is a length limit on email addresses.
# That limit is a maximum of 64 characters (octets) in the "local part" (before the "@") and a maximum of 255
# characters (octets) in the domain part (after the "@") for a total length of 320 characters.


#     Remplacer le nom de la table article par celui de votre sujet.
#     Créer la table qui permettra de définir la déclinaison de l’article
#     Remplacer l’attribut article_id par celui de votre sujet dans le schéma ci-dessus.
#     Créer une table type_article (en modifiant le nom par celui du sujet)
#     Ajouter des attributs dans la table principale
#     L’état de la commande peut être selon le sujet, “en attente”, “expédié”, “validé”, “confirmé”
#
#
#     Le système doit disposer d’un système de panier stocké dans une base de données avant la confirmation de la commande (et non en “session”)
#
#
#     Rechercher les clés primaires dans le schéma ci-dessus.
#     Modifier le schéma avec les éléments de votre sujet en vous inspirant d’exemples sur internet

# utilisateur (id_utilisateur, login, email, nom, password, role)
# commande (id_commande, date_achat, #utilisateur_id, #etat_id)
# ligne_commande ( #commande_id , #peinture_id , prix, quantite)
# ligne_panier (#utilisateur_id , #peinture_id, quantite, date_ajout)
# etat (id_etat, libelle )

CREATE TABLE IF NOT EXISTS etat (
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);

CREATE TABLE IF NOT EXISTS commande (
    id_commande INT AUTO_INCREMENT,
    date_achat DATE,
    utilisateur_id INT,
    etat_id INT,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
);


CREATE TABLE IF NOT EXISTS ligne_commande (
    commande_id INT,
    peinture_id INT,
    prix DECIMAL(15, 2),
    quantite INT,
    PRIMARY KEY (commande_id, peinture_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
);

CREATE TABLE IF NOT EXISTS ligne_panier (
    utilisateur_id INT,
    peinture_id INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id, peinture_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture)
);

# États possibles
INSERT INTO etat (libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');

#---------------------------------------------
#-----------Jeux de test----------------------
#---------------------------------------------

INSERT INTO categorie (nom_categorie) VALUES
    ('Peintures d''Intérieur'),
    ('Peintures d''Extérieur'),
    ('Peintures Spécialisées'),
    ('Apprêt'),
    ('Peintures Artistiques'),
    ('Peintures Écologiques');

INSERT INTO couleur (nom_couleur) VALUES
    ('Chartreuse'),
    ('Bleu'),
    ('Viva magenta'),
    ('Jaune');

INSERT INTO peinture (nom_peinture, volume_pot, numero_melange, prix_peinture, couleur_id, categorie_id, fournisseur, marque, image) VALUES
    ('Peinture Premium Rouge Intérieur', 2.5, 101, 25.99, 1, 1, 'Team chartreuse', 'Team Chartreuse', 'paint_image1.jpg'),
    ('Bouclier Bleu Extérieur', 1.0, 102, 15.50, 2, 1, 'Eclat d\'étoile', 'Eclat d\'étoile', 'paint_image2.jpg'),
    ('Vert Écologique', 3.0, 103, 30.75, 3, 2, 'Team Chartreuse', 'Team Chartreuse', 'paint_image3.jpg'),
    ('Apprêt Jaune Universel', 2.0, 104, 20.00, 4, 2, 'Eclat d\'étoile', 'Eclat d\'étoile', 'paint_image4.jpg'),
    ('Harmonie Intérieure Rouge', 1.5, 105, 18.99, 1, 3, 'Bricodeco', 'Team Chartreuse', 'paint_image5.jpg'),
    ('ProShield Bleu Extérieur', 2.5, 106, 25.50, 2, 3, 'Bricodeco', 'Team Chartreuse', 'paint_image6.jpg'),
    ('Peinture Écologique GreenTech', 1.0, 107, 15.75, 3, 4, 'Eclat d\'étoile', 'Eclat d\'étoile', 'paint_image7.jpg'),
    ('Premium Jaune Extérieur', 3.0, 108, 32.00, 4, 4, 'Team Chartreuse', 'Team Chartreuse', 'paint_image8.jpg'),
    ('Harmonie Intérieure Rouge', 2.0, 109, 21.99, 1, 5, 'Adam Peinture', 'Team Chartreuse', 'paint_image9.jpg'),
    ('Ciel Étoilé Bleu', 1.5, 110, 17.50, 2, 5, 'Adam Peinture', 'Team Chartreuse', 'paint_image10.jpg'),
    ('Éclat Vert Artistique', 2.5, 111, 28.75, 3, 6, 'Adam Peinture', 'Team Chartreuse', 'paint_image11.jpg'),
    ('Apprêt Gris Universel', 2.0, 112, 22.00, 4, 6, 'Team Chartreuse', 'Team Chartreuse', 'paint_image12.jpg'),
    ('Lueur Écologique Vert Intérieur', 2.5, 115, 24.75, 3, 5, 'Adam Peinture', 'Team Chartreuse', 'paint_image15.jpg');

INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
    (1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin'),
    (2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client'),
    (3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2');