#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime, date
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''   SELECT l.*, v.prix_velo AS prix, v.libelle_velo AS nom, v.stock, v.id_velo AS id_article
                FROM ligne_panier l
                INNER JOIN velo v on l.id_velo = v.id_velo
                WHERE id_utilisateur=%s '''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()
    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(quantite*v.prix_velo) as PRIX_TOTAL FROM ligne_panier LEFT JOIN velo v on v.id_velo = ligne_panier.id_velo WHERE id_utilisateur=%s GROUP BY id_utilisateur'''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()['PRIX_TOTAL']
    else:
        prix_total = None
    # etape 2 : selection des adresses
    sql = '''SELECT * FROM adresse WHERE id_utilisateur=%s'''
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()
    return render_template('client/boutique/panier_validation_adresses.html'
                           , adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           )

@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
    sql = ''' SELECT l.*, v.prix_velo AS prix, v.libelle_velo AS nom, v.stock, v.id_velo
                FROM ligne_panier l
                INNER JOIN velo v on l.id_velo = v.id_velo
                WHERE id_utilisateur=%s '''
    mycursor.execute(sql, id_client)
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
         flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
         return redirect(url_for('client_index'))
                                           # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    a = date.today()

    sql = ''' INSERT INTO commande(date_achat, id_utilisateur, etat_id, id_adresse_facture, id_adresse_livraison) VALUE (%s, %s, %s, %s, %s)'''

    livraison = request.form.get('id_adresse_livraison')
    if request.form.get('adresse_identique'):
        facturation = livraison
    else:
        facturation = request.form.get('id_adresse_facturation')

    mycursor.execute(sql, (a ,id_client, 1, facturation, livraison))

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    idCommande = int(mycursor.fetchone()['last_insert_id'])
    for item in items_ligne_panier:
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s '''
        mycursor.execute(sql, (id_client, item['id_velo']))
        sql = '''INSERT INTO ligne_commande(id_commande, id_velo, quantite, prix) VALUE (%s, %s, %s, %s)'''
        mycursor.execute(sql, (idCommande, item['id_velo'], int(item['quantite']), (int(item['quantite'])*int(item['prix']))))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''  SELECT *, SUM(lc.quantite*lc.prix) as prix_total, SUM(quantite) as nbr_articles
                FROM commande
                LEFT JOIN ligne_commande lc on commande.id_commande = lc.id_commande
                LEFT JOIN etat e on e.id_etat = commande.etat_id
                WHERE id_utilisateur=%s 
                GROUP BY commande.id_commande, commande.date_achat, commande.etat_id
                ORDER BY commande.date_achat, commande.etat_id
                '''
    mycursor.execute(sql, id_client)
    commandes = mycursor.fetchall()
    articles_commande = None
    commande_adresses = None    


    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        mycursor.execute('''SELECT lc.*, v.libelle_velo AS nom, (lc.quantite*lc.prix) AS prix_total FROM ligne_commande lc
        LEFT JOIN velo v on v.id_velo = lc.id_velo WHERE id_commande=%s''', id_commande)
        articles_commande = mycursor.fetchall()
        commande_adresses = None
        sql = ''' selection du détails d'une commande '''

        # partie 2 : selection de l'adresse de livraison et de facturation de la commande selectionnée
        sql = ''' selection des adressses '''

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )

