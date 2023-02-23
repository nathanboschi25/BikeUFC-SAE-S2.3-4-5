#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = '''
          select *, sum(quantite) as nbr_articles,sum(prix) as prix_total, libelle from commande cd
          inner join ligne_commande lc on cd.id_commande = lc.id_commande
          inner join etat on cd.etat_id = etat.id_etat
          group by lc.id_commande;      '''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    # print(id_commande)
    if id_commande != None:
        sql = '''
        select v.libelle_velo as nom, v.prix_velo as prix,lc.prix as prix_ligne, lc.quantite as quantite from commande cd
        inner join ligne_commande lc on cd.id_commande = lc.id_commande
        inner join velo v on lc.id_velo = v.id_velo
        where cd.id_commande = %s; 
        '''
        mycursor.execute(sql, id_commande)
        articles_commande = mycursor.fetchall()
        # print(articles_commande)
        sql = '''
            select ad.nom as nom_livraison, ad.rue as rue_livraison, ad.code_postal as code_postal_livraison, ville as ville_livraison from adresse ad
            inner join commande c on ad.id_adresse = c.id_adresse_livraison
            where c.id_commande = %s;
            select ad.nom as nom_facturation, ad.rue as rue_facturation, ad.code_postal as code_postal_facturation, ville as ville_facturation from adresse ad
            inner join commande c on ad.id_adresse = c.id_adresse_facture
            where c.id_commande = %s;
        '''
        mycursor.execute(sql, (id_commande,id_commande))
        commande_adresses = mycursor.fetchone()
        print(commande_adresses)
        # TODO : récup l'adreesse de facture sur la même commande et le même fetch avec les bon 'as' de la template admin/commande/show
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    if commande_id != None:
        print(commande_id)
        sql = '''           '''
        mycursor.execute(sql, commande_id)
        get_db().commit()
    return redirect('/admin/commande/show')