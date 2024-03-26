DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS declinaison;
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

CREATE TABLE IF NOT EXISTS taille(
    id_taille INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    code_taille INT,
    PRIMARY KEY (id_taille)
);

CREATE TABLE IF NOT EXISTS declinaison(
    id_declinaison_peinture INT AUTO_INCREMENT,
    stock INT,
    prix_declinaison DECIMAL(15, 2),
    peinture_id INT,
    taille_id INT,
    PRIMARY KEY (id_declinaison_peinture),
    FOREIGN KEY (peinture_id) REFERENCES peinture(id_peinture),
    FOREIGN KEY (taille_id) REFERENCES taille(id_taille)
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
    declinaison_peinture_id INT,
    prix DECIMAL(15, 2),
    quantite INT,
    PRIMARY KEY (commande_id, declinaison_peinture_id),
    FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    FOREIGN KEY (declinaison_peinture_id) REFERENCES declinaison(id_declinaison_peinture)
);

CREATE TABLE IF NOT EXISTS ligne_panier (
    utilisateur_id INT,
    declinaison_peinture_id INT,
    quantite INT,
    date_ajout DATE,
    PRIMARY KEY (utilisateur_id, declinaison_peinture_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (declinaison_peinture_id) REFERENCES declinaison(id_declinaison_peinture)
);

ALTER TABLE peinture ADD COLUMN description VARCHAR(1024);

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

INSERT INTO taille (libelle, code_taille) VALUES
  ('1L', 1),
  ('2.5L', 2),
  ('5L', 3);

INSERT INTO peinture (nom_peinture, volume_pot, numero_melange, prix_peinture, couleur_id, categorie_id, fournisseur, marque, image) VALUES
    ('Peinture Premium Rouge Intérieur', 2.5, 101, 25.99, 1, 1, 'Team chartreuse', 'Team Chartreuse', 'peinture_premium_rouge_interieur.png'),
    ('Bouclier Bleu Extérieur', 1.0, 102, 15.50, 2, 1, 'Eclat d\'étoile', 'Eclat d\'étoile', 'bouclier_bleu_exterieur.png'),
    ('Vert Écologique', 3.0, 103, 30.75, 3, 2, 'Team Chartreuse', 'Team Chartreuse', 'vert_ecologique.png'),
    ('Apprêt Jaune Universel', 2.0, 104, 20.00, 4, 2, 'Eclat d\'étoile', 'Eclat d\'étoile', 'appret_jaune_universel.png'),
    ('Harmonie Intérieure Rouge', 1.5, 105, 18.99, 1, 3, 'Bricodeco', 'Team Chartreuse', 'harmonie_interieure_rouge.png'),
    ('ProShield Bleu Extérieur', 2.5, 106, 25.50, 2, 3, 'Bricodeco', 'Team Chartreuse', 'proshield_bleu_exterieur.png'),
    ('Peinture Écologique GreenTech', 1.0, 107, 15.75, 3, 4, 'Eclat d\'étoile', 'Eclat d\'étoile', 'peinture_ecologique_greentech.png'),
    ('Premium Jaune Extérieur', 3.0, 108, 32.00, 4, 4, 'Team Chartreuse', 'Team Chartreuse', 'premium_jaune_exterieur.png'),
    ('Harmonie Intérieure Rouge', 2.0, 109, 21.99, 1, 5, 'Adam Peinture', 'Team Chartreuse', 'harmonie_interieure_rouge.png'),
    ('Ciel Étoilé Bleu', 1.5, 110, 17.50, 2, 5, 'Adam Peinture', 'Team Chartreuse', 'ciel_etoile_bleu.png'),
    ('Éclat Vert Artistique', 2.5, 111, 28.75, 3, 6, 'Adam Peinture', 'Team Chartreuse', 'eclat_vert_artistique.png'),
    ('Apprêt Gris Universel', 2.0, 112, 22.00, 4, 6, 'Team Chartreuse', 'Team Chartreuse', 'appret_gris_universel.png'),
    ('Lueur Écologique Vert Intérieur', 2.5, 115, 24.75, 3, 5, 'Adam Peinture', 'Team Chartreuse', 'lueur_ecologique_vert_interieur.png'),
    ('Ecru', 1.5, 117, 15.55, 4, 6, 'Adam Peinture', 'Team Chartreuse', 'ecru.png'),
    ('Chartreuse', 3.5, 127, 32.99, 1, 3, 'Team Chartreuse', 'Team Chartreuse', 'chartreuse.png'    );


# ---------------------------------------------
# Déclinaisons pour les peintures sélectionnées
# ---------------------------------------------


-- 1. Peinture Premium Rouge Intérieur
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(10, 25.99, 1, 1), -- 1L
(5, 32.99, 1, 2), -- 2.5L
(2, 40.99, 1, 3); -- 5L

-- 2. Bouclier Bleu Extérieur
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(8, 15.50, 2, 1), -- 1L
(4, 20.50, 2, 2), -- 2.5L
(2, 25.50, 2, 3); -- 5L

-- 3. Vert Écologique
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(11, 30.75, 3, 1), -- 1L
(6, 37.75, 3, 2), -- 2.5L
(3, 44.75, 3, 3); -- 5L

-- 4. Apprêt Jaune Universel
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(58, 20.00, 4, 1), -- 1L
(29, 25.00, 4, 2), -- 2.5L
(15, 30.00, 4, 3); -- 5L

-- 5. Harmonie Intérieure Rouge
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(26, 18.99, 5, 1), -- 1L
(13, 23.99, 5, 2), -- 2.5L
(7, 28.99, 5, 3); -- 5L

-- 6. ProShield Bleu Extérieur
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(3, 25.50, 6, 1), -- 1L
(2, 30.50, 6, 2), -- 2.5L
(1, 35.50, 6, 3); -- 5L

-- 7. Peinture Écologique GreenTech
INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(89, 15.75, 7, 1), -- 1L
(45, 20.75, 7, 2), -- 2.5L
(23, 25.75, 7, 3); -- 5L

-- Déclinaisons par défaut pour les peintures restantes

INSERT INTO declinaison (stock, prix_declinaison, peinture_id, taille_id) VALUES
(10, 19.99, 8, 2), -- Harmonie Intérieure Rouge
(12, 22.99, 9, 2), -- Ciel Étoilé Bleu
(15, 27.99, 10, 2), -- Éclat Vert Artistique
(20, 23.99, 11, 2), -- Apprêt Gris Universel
(18, 25.99, 12, 2), -- Lueur Écologique Vert Intérieur
(25, 16.99, 13, 2), -- Ecru
(30, 33.99, 14, 2); -- Chartreuse



INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom) VALUES
    (1,'admin','admin@admin.fr',
    'pbkdf2:sha256:600000$olNVM35LlMvBbE12$8e04be309fd45d72c684f5caa3804afbb77bfb3f6bec5fdd5a9a86165cd7092a',
    'ROLE_admin','admin'),
    (2,'client','client@client.fr',
    'pbkdf2:sha256:600000$dYjw0xxqdHAIA1GO$eaef95ecf21a51f50769bb3b45cbc59edebf575bbefe91a52c16b8525a6ed3c2',
    'ROLE_client','client'),
    (3,'client2','client2@client2.fr',
    'pbkdf2:sha256:600000$LLJIBGNbPjJ63uJM$b774cf95df80c722d09f957b1831d82689153544916b460410e2d0de73337db0',
    'ROLE_client','client2');
