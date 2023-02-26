#! /usr/bin/python
# -*- coding:utf-8 -*-
import numpy
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''SELECT id_velo AS id_article,
       libelle_velo AS nom,
       prix_velo AS prix,
       stock AS stock,
       image_velo as `image`

        FROM velo'''
        # ORDER BY libelle_velo;'''
    list_param = []
    condition_and = ""
    print(session)
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if "filter_word" in session:
        sql = sql + " libelle_velo LIKE %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session and "filter_prix_max" not in session :
        sql = sql + condition_and + " prix_velo > %s "
        list_param.append(session["filter_prix_min"])
        condition_and = " AND "
    elif "filter_prix_max" in session and "filter_prix_min" not in session :
        sql = sql + condition_and + " prix_velo < %s "
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    elif "filter_prix_min" in session and "filter_prix_max" in session:
        sql = sql + condition_and + " prix_velo BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1] # FIXME : INUTILE ?!
        for item in session['filter_types']:
            sql = sql + " id_type = %s "
            # FIXME
            if item != last_item:
                sql = sql + " or "
            list_param.append(item)
        sql = sql + ")"
    tuple_sql = tuple(list_param)

    sql += " ORDER BY libelle_velo; "

    
    # print(sql, tuple_sql)
    mycursor.execute(sql,tuple_sql)
    velos = mycursor.fetchall()
    # list_param = []
    # condition_and = ""
    # # utilisation du filtre
    # sql3=''' prise en compte des commentaires et des notes dans le SQL    '''
    # articles =[]


    # pour le filtre
    sql = "SELECT * FROM type_velo;"
    mycursor.execute(sql)
    types_velo = mycursor.fetchall()

    sql = '''SELECT
                l.quantite,
                 v.prix_velo as prix,
                 v.libelle_velo as nom ,
                  v.id_velo as id_article,
                  v.stock
            FROM ligne_panier l 
            LEFT JOIN velo v on v.id_velo = l.id_velo 
            WHERE id_utilisateur=%s'''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        sql = '''   SELECT SUM(quantite*v.prix_velo) AS prix_total
                    FROM ligne_panier
                    LEFT JOIN velo v on v.id_velo = ligne_panier.id_velo
                    WHERE id_utilisateur=%s
                    GROUP BY id_utilisateur
                '''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()
        prix_total = prix_total['prix_total']
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html'
                           , articles=velos
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=types_velo
                           )
