DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS note;
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
    description VARCHAR(2048),
    stock INT,

    PRIMARY KEY (id_peinture),
    FOREIGN KEY (couleur_id) REFERENCES couleur (id_couleur),
    FOREIGN KEY (categorie_id) REFERENCES categorie (id_categorie)
);

CREATE TABLE IF NOT EXISTS utilisateur (
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(320),
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

CREATE TABLE IF NOT EXISTS commentaire (
    date_publication DATETIME,
    peinture_id      INT,
    utilisateur_id   INT,
    commentaire      VARCHAR(255),
    valider          INT,
    PRIMARY KEY (date_publication, peinture_id, utilisateur_id),
    FOREIGN KEY (peinture_id) REFERENCES peinture (id_peinture),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE IF NOT EXISTS note (
    peinture_id INT,
    utilisateur_id INT,
    note DECIMAL(2,1),
    PRIMARY KEY (peinture_id, utilisateur_id),
    FOREIGN KEY (peinture_id) REFERENCES peinture (id_peinture),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

#---------------------------------------------
#-----------Jeux de test----------------------
#---------------------------------------------

INSERT INTO etat (libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');

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

INSERT INTO peinture (nom_peinture, volume_pot, numero_melange, prix_peinture, couleur_id, categorie_id, fournisseur, marque, image, description, stock) VALUES
    ('Bouclier Bleu Extérieur', 1.0, 102, 15.50, 2, 1, 'Eclat d\'étoile', 'Eclat d\'étoile', 'bouclier_bleu_exterieur.png', 'Le Bouclier Bleu Extérieur est votre allié ultime contre les éléments. Sa teinte bleue profonde et riche ajoute une touche de sérénité à vos extérieurs, tandis que sa formule résistante aux intempéries offre une protection durable contre la pluie, le vent et le soleil. Que ce soit pour les portes, les fenêtres ou les clôtures, cette peinture assure une finition impeccable et une couleur éclatante qui dure.', 8),
    ('Vert Écologique', 3.0, 103, 30.75, 3, 2, 'Team Chartreuse', 'Team Chartreuse', 'vert_ecologique.png', 'Le Vert Écologique est un choix conscient pour les amoureux de la nature. Sa teinte verte rafraîchissante apporte une bouffée d\'air frais à votre environnement, tandis que sa formule respectueuse de l\'environnement garantit une empreinte écologique réduite. Que ce soit pour les murs intérieurs ou extérieurs, cette peinture offre une couverture exceptionnelle et une finition durable, pour des résultats durables et magnifiques.', 11),
    ('Apprêt Jaune Universel', 2.0, 104, 20.00, 4, 2, 'Eclat d\'étoile', 'Eclat d\'étoile', 'appret_jaune_universel.png', 'L\'Apprêt Jaune Universel est votre premier pas vers un résultat parfait. Sa teinte jaune lumineuse offre une base idéale pour une variété de couleurs, assurant une adhérence optimale et une finition uniforme. Que ce soit pour les murs intérieurs ou extérieurs, cette peinture préparatoire vous permet de créer une surface lisse et prête à accueillir votre couleur préférée.', 58),
    ('Harmonie Intérieure Rouge', 1.5, 105, 18.99, 1, 3, 'Bricodeco', 'Team Chartreuse', 'harmonie_interieure_rouge.png', 'L\'Harmonie Intérieure Rouge crée une atmosphère chaleureuse et accueillante dans votre maison. Sa teinte rouge vibrante évoque la passion et l\'énergie, tandis que sa formule de haute qualité offre une couverture exceptionnelle et une finition durable. Que ce soit pour un salon, une salle à manger ou une chambre à coucher, cette peinture ajoute une touche de glamour à votre décor intérieur.', 26),
    ('ProShield Bleu Extérieur', 2.5, 106, 25.50, 2, 3, 'Bricodeco', 'Team Chartreuse', 'proshield_bleu_exterieur.png', 'Le ProShield Bleu Extérieur est votre gardien contre les éléments. Sa teinte bleue profonde et riche ajoute une touche de calme à vos extérieurs, tandis que sa formule résistante aux intempéries offre une protection maximale contre la pluie, le vent et les rayons UV. Que ce soit pour les portes, les fenêtres ou les clôtures, cette peinture assure une finition impeccable et une couleur durable qui dure des années.', 3),
    ('Peinture Écologique GreenTech', 1.0, 107, 15.75, 3, 4, 'Eclat d\'étoile', 'Eclat d\'étoile', 'peinture_ecologique_greentech.png', 'La Peinture Écologique GreenTech est votre choix pour un intérieur sain et respectueux de l\'environnement. Sa formule à base d\'ingrédients naturels offre une alternative durable aux peintures traditionnelles, tout en offrant une couleur riche et une finition impeccable. Que ce soit pour les murs de votre salon, de votre chambre ou de votre bureau, cette peinture écologique crée un environnement sain et sûr pour votre famille.', 89),
    ('Premium Jaune Extérieur', 3.0, 108, 32.00, 4, 4, 'Team Chartreuse', 'Team Chartreuse', 'premium_jaune_exterieur.png', 'Le Premium Jaune Extérieur est le rayon de soleil dont vos extérieurs ont besoin. Sa teinte jaune lumineuse apporte de la joie et de la luminosité à n\'importe quel espace, tandis que sa formule résistante aux intempéries offre une protection durable contre les éléments. Que ce soit pour les murs, les portes ou les volets, cette peinture assure une finition impeccable et une couleur éclatante qui dure.', 7),
    ('Harmonie Intérieure Rouge', 2.0, 109, 21.99, 1, 5, 'Adam Peinture', 'Team Chartreuse', 'harmonie_interieure_rouge.png', 'L\'Harmonie Intérieure Rouge apporte une touche de passion à votre décor intérieur. Sa teinte rouge profonde et riche crée une ambiance chaleureuse et accueillante dans n\'importe quelle pièce, tandis que sa formule de haute qualité offre une couverture exceptionnelle et une finition durable. Que ce soit pour un salon, une salle à manger ou une chambre à coucher, cette peinture ajoute une touche de glamour à votre espace de vie.', 4),
    ('Ciel Étoilé Bleu', 1.5, 110, 17.50, 2, 5, 'Adam Peinture', 'Team Chartreuse', 'ciel_etoile_bleu.png', 'Le Ciel Étoilé Bleu capture la beauté et la tranquillité du ciel nocturne. Sa teinte bleue douce et paisible crée une atmosphère relaxante dans n\'importe quelle pièce. Que ce soit pour une chambre, un salon ou un bureau, cette peinture ajoute une touche de sérénité à votre espace. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable. Laissez-vous emporter par la magie des étoiles avec cette peinture magnifique.', 56),
    ('Éclat Vert Artistique', 2.5, 111, 28.75, 3, 6, 'Adam Peinture', 'Team Chartreuse', 'eclat_vert_artistique.png', 'L\'Éclat Vert Artistique apporte une touche de nature et de fraîcheur à votre espace. Sa teinte verte vibrante évoque la vie et la croissance, créant une ambiance dynamique et inspirante. Que ce soit pour un salon, une salle à manger ou un bureau, cette peinture ajoute une touche artistique à votre décoration intérieure. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable, pour des résultats époustouflants à chaque fois.', 23),
    ('Apprêt Gris Universel', 2.0, 112, 22.00, 4, 6, 'Team Chartreuse', 'Team Chartreuse', 'appret_gris_universel.png', 'L\'Apprêt Gris Universel est le choix idéal pour préparer vos surfaces avant de peindre. Sa teinte grise neutre offre une base parfaite pour une variété de couleurs, assurant une adhérence optimale et une finition uniforme. Que ce soit pour les murs intérieurs ou extérieurs, cette peinture préparatoire vous permet de créer une surface lisse et prête à accueillir votre couleur préférée.', 32),
    ('Lueur Écologique Vert Intérieur', 2.5, 115, 24.75, 3, 5, 'Adam Peinture', 'Team Chartreuse', 'lueur_ecologique_vert_interieur.png', 'La Lueur Écologique Vert Intérieur illumine votre intérieur avec sa couleur verte apaisante et sa formule respectueuse de l\'environnement. Conçue pour offrir une couverture exceptionnelle et une finition durable, cette peinture crée une ambiance calme et relaxante dans n\'importe quelle pièce. Que ce soit pour les murs de votre salon, de votre chambre ou de votre bureau, cette peinture écologique est le choix parfait pour un intérieur sain et beau.', 7),
    ('Ecru', 1.5, 117, 15.55, 4, 6, 'Adam Peinture', 'Team Chartreuse', 'ecru.png', 'L\'Ecru apporte une touche de douceur et d\'élégance à votre décor. Sa teinte crème neutre offre une toile de fond polyvalente pour une variété de styles et de palettes de couleurs. Que ce soit pour les murs, les meubles ou les accessoires, cette peinture ajoute une note subtile de sophistication à n\'importe quelle pièce. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable, pour des résultats impeccables.', 89),
    ('Chartreuse', 3.5, 127, 32.99, 1, 3, 'Team Chartreuse', 'Team Chartreuse', 'chartreuse.png', 'La Chartreuse est bien plus qu\'une simple couleur - c\'est une déclaration audacieuse. Sa teinte vert citron éclatante apporte une énergie vibrante à n\'importe quel espace, créant une ambiance dynamique et stimulante. Que ce soit pour les murs, les meubles ou les accents, cette peinture ajoute une touche d\'audace et de personnalité à votre décoration. Avec sa formule de haute qualité, elle offre une couverture exceptionnelle et une finition durable, pour des résultats éblouissants à chaque fois.', 10);

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

#INSERT INTO commentaire (date_publication, peinture_id, utilisateur_id, commentaire, valider) VALUES
#        ('2024-03-10', 1, 2, 'Très bonne peinture, je suis satisfait de mon achat.', 'Non'),
#        ('2024-03-11', 2, 3, 'La couleur est magnifique, mais la peinture est un peu épaisse.', 'Oui'),
#        ('2024-03-12', 3, 2, 'Je recommande vivement cette peinture écologique, elle est excellente !', 'Non');

#INSERT INTO note (peinture_id, utilisateur_id, note) VALUES
#        (1, 2, 4),
#        (2, 3, 3),
#        (3, 2, 5);

#INSERT INTO commande (id_commande, date_achat, utilisateur_id, etat_id) VALUES
#    (1, NOW(), 2, 2),
#    (2, '2024-02-07 10:00:00', 3, 1);


#INSERT INTO ligne_commande (commande_id, peinture_id, prix, quantite) VALUES
#    (2, 15, 32.99, 2),
#    (2, 5, 18.99, 3),
#    (1, 1, 25.99, 1),
#    (1, 5, 18.99, 5),
#    (1, 10, 17.50, 2);
