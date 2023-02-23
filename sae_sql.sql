DROP TABLE IF EXISTS
    ligne_panier,
    ligne_commande,
    type_velo,
    velo,
    fournisseur,
    commande,
    adresse,
    etat,
    utilisateur;

CREATE TABLE utilisateur(
                            id_utilisateur INT NOT NULL AUTO_INCREMENT,
                            login VARCHAR(255),
                            email VARCHAR(255),
                            nom VARCHAR(255),
                            password VARCHAR(255),
                            role VARCHAR(255),
                            est_actif TINYINT(1),
    -- token_email VARCHAR(255,
    -- token_email_date DATE(),

    -- go_auth_token VARCHAR(255),
    -- go_username_token VARCHAR(255)
                            PRIMARY KEY (id_utilisateur)
)ENGINE=InnoDB DEFAULT CHARSET utf8mb4;

CREATE TABLE etat(
                     id_etat INT NOT NULL AUTO_INCREMENT,
                     libelle VARCHAR(255),
                     PRIMARY KEY(id_etat)
);

create table if not exists adresse(
                        id_adresse int not null auto_increment,
                        id_utilisateur int not null,
                        nom varchar(255),
                        rue varchar(255),
                        code_postal int,
                        ville varchar(255),
                        date_utilisation date,
                        primary key (id_adresse),
                        foreign key (id_utilisateur) references utilisateur(id_utilisateur)
);

CREATE TABLE commande(
                         id_commande INT NOT NULL AUTO_INCREMENT,
                         date_achat DATE,
                         id_utilisateur INT NOT NULL,
                         etat_id INT NOT NULL,
                         id_adresse_facture int not null ,
                         id_adresse_livraison int not null ,
                         PRIMARY KEY (id_commande),
                         FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
                         FOREIGN KEY (etat_id) REFERENCES etat(id_etat),
                         foreign key (id_adresse_facture) references adresse(id_adresse),
                         foreign key (id_adresse_livraison) references adresse(id_adresse)
);

CREATE TABLE fournisseur(
                            id_fournisseur INT NOT NULL AUTO_INCREMENT,
                            libelle_fournisseur VARCHAR(50),
                            PRIMARY KEY(id_fournisseur)
);

CREATE TABLE type_velo(
                          id_type INT NOT NULL AUTO_INCREMENT,
                          libelle_type VARCHAR(255),
                          PRIMARY KEY(id_type)
);

CREATE TABLE velo(
                     id_velo INT NOT NULL AUTO_INCREMENT,
                     libelle_velo VARCHAR(255),
                     prix_velo DECIMAL(10,2),
                     image_velo VARCHAR(255),
                     stock INT,
                     id_type INT NOT NULL,
                     id_fournisseur INT NOT NULL,
                     PRIMARY KEY(id_velo),
                     FOREIGN KEY(id_type) REFERENCES type_velo(id_type),
                     FOREIGN KEY(id_fournisseur) REFERENCES fournisseur(id_fournisseur)
);

CREATE TABLE ligne_commande(
                               id_commande INT NOT NULL,
                               id_velo INT,
                               quantite INT,
                               prix DECIMAL(10,2),
                               PRIMARY KEY(id_commande, id_velo),
                               FOREIGN KEY(id_commande) REFERENCES commande(id_commande),
                               FOREIGN KEY(id_velo) REFERENCES velo(id_velo)
);

CREATE TABLE ligne_panier(
                             id_utilisateur INT NOT NULL,
                             id_velo INT,
                             quantite INT,
                             PRIMARY KEY(id_utilisateur, id_velo),
                             FOREIGN KEY(id_utilisateur) REFERENCES utilisateur(id_utilisateur),
                             FOREIGN KEY(id_velo) REFERENCES velo(id_velo)
);

INSERT INTO etat(libelle) VALUES ('En attente'), ('Expédié'), ('Validé'), ('Confirmé'), ('Annulé');
INSERT INTO type_velo(libelle_type) VALUES ('VTT'), ('ROUTE'), ('VILLE'), ('ELECTRIQUE'), ('ENFANTS');
INSERT INTO fournisseur(libelle_fournisseur) VALUES ('TREK'), ('LAPIERRE'), ('PEUGEOT'), ('SPECIALIZED'), ('CUBE');
INSERT INTO utilisateur(login, email, password, role) VALUES
                                                          ('client', 'client@clients.com', 'sha256$p0G37N7TRA0rCdB2$e16136a121e9c3e1965e7823b9d9f9bc348c6104fd607fcce5e6ef47702dcb99', 'ROLE_client'),
                                                          ('client2', 'client2@clients.com', 'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422', 'ROLE_client'),
                                                          ('admin', 'admin@admin.com', 'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf', 'ROLE_admin');
INSERT INTO velo(libelle_velo, prix_velo, image_velo, stock, id_type, id_fournisseur) VALUES
                                                                                          ('Slash 8 GX', 4499.00, 'Slash8GX.jpeg', 100, 1, 1),
                                                                                          ('Madone SLR 9 7eG', 14699.00, 'MadoneSLR9.jpeg', 100, 2, 1),
                                                                                          ('Dual Sport 3 Equipped', 1249.00,'DualSport3EQ.webp', 100, 3, 1),
                                                                                          ('Powerfly FS 9 Equipped 2eG', 7299.00,'PowerflyFS9EQ.webp', 100, 4, 1),
                                                                                          ('Domane+ LT 7 2eG', 7999.00,'DomanePlusLT7.jpeg', 100, 4, 1),
                                                                                          ('Spicy CF 6.9 2022', 4599.00, 'SpicyCF6.9MY22.png', 100, 1, 2),
                                                                                          ('Aircode DRS 9.0 2022', 8399.00, 'AircodeDRS9.0MY22.png', 100, 2, 2),
                                                                                          ('e-Urban 3.4 2023', 2599.00, 'E-Urban3.4MY22.png', 100, 4, 2),
                                                                                          ('R02 CARBONE ULTEGRA - 2019', 2999.00, 'peugeot-r02-carbone-ultegra.jpg', 100, 2, 3),
                                                                                          ('Epic Comp', 5200.00, 'EPIC-COMP.webp', 100, 1, 4),
                                                                                          ('Sirrus 2.0 - Équipé', 1100.00, '90921-82_SIRRUS-20-EQ-FSTGRN-BLKREFL_HERO.webp', 100, 3, 4),
                                                                                          ('Aethos Expert', 7000.00, '97222-30_AETHOS-EXPERT-OIL-FLKSIL_HERO1.webp', 100, 2, 4),
                                                                                          ('TRAVEL SLX', 2199.00, 'travel.jpg', 100, 3, 5);
INSERT INTO ligne_panier VALUES
                             (1, 1, 1),
                             (1, 2, 3),
                             (1, 5, 12),
                             (2, 8, 1),
                             (2, 4, 2);

insert into adresse(id_adresse, id_utilisateur, nom, rue, code_postal, ville, date_utilisation) values
                            (
                                null, 1, 'IUT', '19 Av. du Maréchal Juin', 90016, 'Belfort', '2022-02-22'
                            ),
                            (
                                null, 1, 'Mairie Belfort', 'Pl. d''Armes', 90000, 'Belfort', '2022-02-22'
                            ),
                            (
                                null, 2, 'IUT', '19 Av. du Maréchal Juin', 90016, 'Belfort', '2022-02-22'
                            );


INSERT INTO commande(id_commande, date_achat, id_utilisateur, etat_id, id_adresse_facture, id_adresse_livraison) VALUES
                            (NULL, '2021-07-04', 1, 2,1,1),
                            (null, '2022-02-22', 2,2,1,2),
                            (null,'2022-02-22',2,1,2,1),
                            (null,'2022-02-22',2,1,2,1);
INSERT INTO ligne_commande(id_commande, id_velo, quantite, prix) VALUES (1, 3, 2, 12599.00),
                                  (1, 7, 1, 7993.25),
                                  (2,3,2,13456),
                                  (2,4,3,12232),
                                  (3,2,3,123867),
                                  (4,1,2,12323);