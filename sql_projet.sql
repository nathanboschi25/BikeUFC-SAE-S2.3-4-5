use sae345;
drop table if exists
    ligne_panier,
    ligne_commande,
    commande,
    declinaison_velo,
    adresse,
    utilisateur,
    etat,
    taille,
    velo,
    fournisseur,
    type_velo,
    couleur;

CREATE TABLE couleur(
   id_couleur int not null auto_increment,
   libelle VARCHAR(255),
   code VARCHAR(255),
   PRIMARY KEY(id_couleur)
);

CREATE TABLE type_velo(
   id_type_velo int not null auto_increment,
   libelle VARCHAR(255),
   PRIMARY KEY(id_type_velo)
);

CREATE TABLE fournisseur(
   id_fournisseur int not null auto_increment,
   libelle VARCHAR(255),
   code_postal INT,
   ville VARCHAR(255),
   rue VARCHAR(255),
   PRIMARY KEY(id_fournisseur)
);


CREATE TABLE velo
(
    id_velo        int NOT NULL AUTO_INCREMENT,
    libelle        VARCHAR(255),
    disponible     BOOL,
    prix           DECIMAL(8, 2),
    description    VARCHAR(255),
    image          VARCHAR(255),
    id_type_velo   INT NOT NULL,
    id_fournisseur INT NOT NULL,
    PRIMARY KEY (id_velo),
    FOREIGN KEY (id_fournisseur) REFERENCES fournisseur (id_fournisseur),
#     CONSTRAINT
    FOREIGN KEY (id_type_velo) REFERENCES type_velo (id_type_velo) # ON DELETE SET NULL
);

CREATE TABLE taille(
   id_taille int not null auto_increment,
   libelle VARCHAR(255),
   PRIMARY KEY(id_taille)
);

CREATE TABLE etat(
   id_etat int not null auto_increment,
   libelle VARCHAR(255),
   PRIMARY KEY(id_etat)
);

CREATE TABLE utilisateur(
   id_utilisateur int not null auto_increment,
   login VARCHAR(255),
   email VARCHAR(255),
   libelle VARCHAR(255),
   password VARCHAR(255),
   role VARCHAR(255),
   PRIMARY KEY(id_utilisateur)
);

CREATE TABLE adresse(
   id_adresse int not null auto_increment,
   libelle VARCHAR(255),
   rue VARCHAR(255),
   code_postal INT,
   ville VARCHAR(255),
   date_utilisation VARCHAR(255),
   id_utilisateur INT NOT NULL,
   PRIMARY KEY(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE declinaison_velo(
   id_declinaison_velo int not null auto_increment,
   stock INT,
   prix_declinaison DECIMAL(8,2),
   image VARCHAR(255),
   id_velo INT NOT NULL,
   id_taille INT NOT NULL,
   id_couleur INT NOT NULL,
   PRIMARY KEY(id_declinaison_velo),
   FOREIGN KEY(id_velo) REFERENCES velo(id_velo),
   FOREIGN KEY(id_taille) REFERENCES taille(id_taille),
   FOREIGN KEY(id_couleur) REFERENCES couleur(id_couleur)
);

CREATE TABLE commande(
   id_commande int not null auto_increment,
   date_achat DATE,
   id_adresse_facturation INT NOT NULL,
   id_adresse_livraison INT NOT NULL,
   id_utilisateur INT NOT NULL,
   id_etat INT NOT NULL,
   PRIMARY KEY(id_commande),
   FOREIGN KEY(id_adresse_facturation) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_adresse_livraison) REFERENCES adresse(id_adresse),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
   FOREIGN KEY(id_etat) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_commande(
   id_declinaison_velo INT,
   id_commande INT,
   quantite INT,
   prix DECIMAL(8,2),
   PRIMARY KEY(id_declinaison_velo, id_commande),
   FOREIGN KEY(id_declinaison_velo) REFERENCES declinaison_velo(id_declinaison_velo),
   FOREIGN KEY(id_commande) REFERENCES commande(id_commande)
);

CREATE TABLE ligne_panier(
   id_declinaison_velo INT,
   id_utilisateur INT,
   quantite INT,
   date_ajout DATE,
   PRIMARY KEY(id_declinaison_velo, id_utilisateur),
   FOREIGN KEY(id_declinaison_velo) REFERENCES declinaison_velo(id_declinaison_velo),
   FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

insert into couleur(id_couleur, libelle, code)
VALUES
    (NULL, 'original', ''),
    (null,'rouge', '#ff0000'),
    (null,'green','#00ff00'),
    (null,'bleu','#0000ff');
insert into type_velo( libelle)
VALUES
    ('VTT'), ('ROUTE'), ('VILLE'), ('ELECTRIQUE'), ('ENFANTS')
insert into fournisseur (libelle)
values ('TREK'),
       ('LAPIERRE'),
       ('PEUGEOT'),
       ('SPECIALIZED'),
       ('CUBE');
insert into velo(libelle, disponible, prix, image, id_type_velo, id_fournisseur)
values ('Slash 8 GX',1, 4499.00, 'Slash8GX.jpeg',  1, 1),
       ('Madone SLR 9 7eG',1, 14699.00, 'MadoneSLR9.jpeg',  2, 1),
       ('Dual Sport 3 Equipped',1, 1249.00,'DualSport3EQ.webp',  3, 1),
       ('Powerfly FS 9 Equipped 2eG',1, 7299.00,'PowerflyFS9EQ.webp',  4, 1),
       ('Domane+ LT 7 2eG',1, 7999.00,'DomanePlusLT7.jpeg',  4, 1),
       ('Spicy CF 6.9 2022',1, 4599.00, 'SpicyCF6.9MY22.png',  1, 2),
       ('Aircode DRS 9.0 2022',1, 8399.00, 'AircodeDRS9.0MY22.png',  2, 2),
       ('e-Urban 3.4 2023',1, 2599.00, 'E-Urban3.4MY22.png',  4, 2),
       ('R02 CARBONE ULTEGRA - 2019',1, 2999.00, 'peugeot-r02-carbone-ultegra.jpg',  2, 3),
       ('Epic Comp',1, 5200.00, 'EPIC-COMP.webp',  1, 4),
       ('Sirrus 2.0 - Équipé',1, 1100.00, '90921-82_SIRRUS-20-EQ-FSTGRN-BLKREFL_HERO.webp',  3, 4),
       ('Aethos Expert',1, 7000.00, '97222-30_AETHOS-EXPERT-OIL-FLKSIL_HERO1.webp',  2, 4),
       ('TRAVEL SLX',1, 2199.00, 'travel.jpg',  3, 5);
insert into taille(libelle)
values ('XS'),
       ('S'),
       ('M'),
       ('L'),
       ('XL');
insert into etat(libelle)
values ('En attente'),
       ('Expédié');
insert into utilisateur(login, email, libelle, password, role)
values ('client', 'client@clients.com', 'Jean','sha256$p0G37N7TRA0rCdB2$e16136a121e9c3e1965e7823b9d9f9bc348c6104fd607fcce5e6ef47702dcb99', 'ROLE_client'),
       ('client2', 'client2@clients.com', 'Marque','sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422', 'ROLE_client'),
       ('admin', 'admin@admin.com', 'Dieu','sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf', 'ROLE_admin');
insert into adresse( id_utilisateur,libelle, rue, code_postal, ville, date_utilisation )
values ( 1, 'IUT', '19 Av. du Maréchal Juin', 90016, 'Belfort', '2022-02-22'),
       ( 1, 'Mairie Belfort', 'Pl. d''Armes', 90000, 'Belfort', '2022-02-22'),
       ( 2, 'IUT', '19 Av. du Maréchal Juin', 90016, 'Belfort', '2022-02-22');

INSERT INTO declinaison_velo (id_velo, id_taille, id_couleur, image, prix_declinaison, stock)
SELECT v.id_velo, t.id_taille, c.id_couleur, '', FLOOR(RAND() * 2000), FLOOR(RAND() * 100)
FROM velo v, taille t, couleur c
WHERE (SELECT COUNT(*) FROM declinaison_velo dv WHERE dv.id_velo = v.id_velo) < 4
  AND RAND() < 4 / (SELECT COUNT(*) FROM velo)
  AND RAND() < 0.5
ORDER BY RAND();
# insert into commande( date_achat, id_adresse_facturation, id_adresse_livraison, id_utilisateur, id_etat)
# values ('2022-02-23',1,1,1,1),
#        ('2022-02-23',2,1,2,1),
#        ('2022-02-23',2,1,1,1);
# insert into ligne_commande(id_declinaison_velo, id_commande, quantite, prix)
# values (1,1,1,4599.00),
#        (1,2,2,9198.00);
# insert into ligne_panier(id_declinaison_velo, id_utilisateur, quantite, date_ajout)
# values (2,1,2,'2022-02-23'),
#        (3,2,1,'2022-02-23');

