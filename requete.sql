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

select v.libelle_velo as nom, v.id_velo as id_article, v.prix_velo as prix, v.id_type as type_article_id,
       tv.libelle_type as libelle, v.stock as stock, v.image_velo as image from velo v
inner join type_velo tv on v.id_type = tv.id_type; # avis as nb_commentaires_nouveaux // faire aussi nb_declinaisons

select v.id_velo as id_article, v.libelle_velo as nom, v.id_type as type_article_id, v.prix_velo as prix, v.image_velo as image
from velo v
where v.id_velo = %s;

select ty.libelle_type as libelle, ty.id_type as id_type_article
from type_velo ty;

select tv.libelle_type as libelle_type, v.stock
from velo v
inner join type_velo tv on v.id_type = tv.id_type
where v.id_velo = %s
group by tv.id_type;

select v.image_velo as image
from velo v
where v.id_velo = %s;


update velo
set libelle_velo = %s, image_velo = %s, prix_velo = %s, id_type = %s, description_velo = ',', stock = %s
where id_velo = %s;


SELECT id_velo AS id_article,
       libelle_velo AS nom,
       prix_velo AS prix,
       stock AS stock,
       image_velo as `image`

        FROM velo

        WHERE (id_type = 1 or id_type = 2)
        ORDER BY libelle_velo;