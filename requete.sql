select date_achat, sum(quantite) as nbr_articles,sum(prix) as prix_total, libelle from commande cd
inner join ligne_commande lc on cd.id_commande = lc.id_commande
inner join etat on cd.etat_id = etat.id_etat
group by lc.id_commande;

select v.libelle_velo as nom, v.prix_velo as prix,lc.prix as prix_ligne, lc.quantite as quantite from commande cd
inner join ligne_commande lc on cd.id_commande = lc.id_commande
inner join velo v on lc.id_velo = v.id_velo
where cd.id_commande = %s;

select ad.nom as nom_livraison, ad.rue as rue_livraison, ad.code_postal as code_postal_livraison, ville as ville_livraison from adresse ad
inner join commande c on ad.id_adresse = c.id_adresse_livraison
where c.id_commande = 1;
select ad.nom as nom_facturation, ad.rue as rue_facturation, ad.code_postal as code_postal_facturation, ville as ville_facturation from adresse ad
inner join commande c on ad.id_adresse = c.id_adresse_facture
where c.id_commande = 1;

select li.nom as nom_livraison, li.rue as rue_livraison, li.code_postal as code_postal_livraison, li.ville as ville_livraison from commande c
inner join adresse fa on c.id_adresse_facture = fa.id_adresse
inner join adresse li on c.id_adresse_livraison = li.id_adresse
where c.id_commande = %s;

select * from commande;
 