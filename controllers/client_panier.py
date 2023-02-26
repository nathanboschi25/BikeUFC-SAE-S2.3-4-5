#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))
    # ---------
    #id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

    # ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

    # ajout dans le panier d'un article
    sql = 'SELECT * FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s'
    mycursor.execute(sql, (id_client, id_article))
    ligne_pannier = mycursor.fetchone()
    article_dans_pannier = True if ligne_pannier is not None else False
    if article_dans_pannier is True:
        sql = 'UPDATE ligne_panier SET quantite=quantite+%s WHERE id_utilisateur=%s AND id_velo=%s'
    else:
        sql = 'INSERT INTO ligne_panier(quantite, id_utilisateur, id_velo) VALUE (%s, %s, %s)'

    result = mycursor.execute(sql, (quantite, id_client, id_article))
    sql = '''SELECT stock FROM velo WHERE id_velo=%s;'''
    mycursor.execute(sql, id_article)
    stock_final = mycursor.fetchone()['stock'] - quantite

    if result == 1:
        sql = 'UPDATE velo SET stock=%s WHERE id_velo=%s'
        mycursor.execute(sql, (stock_final, id_article))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    sql = '''SELECT quantite FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s;'''
    mycursor.execute(sql, (id_client, id_article))

    if mycursor.fetchone()['quantite'] < 2:
        sql = '''DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s'''
    else:
        sql = '''UPDATE ligne_panier SET quantite=quantite-1 WHERE id_utilisateur=%s AND id_velo=%s'''
    mycursor.execute(sql, (id_client, id_article))

    sql = '''UPDATE velo SET stock=stock+1 WHERE id_velo=%s'''
    mycursor.execute(sql, id_article)

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier WHERE id_utilisateur=%s '''
    mycursor.execute(sql, client_id)
    items_panier = mycursor.fetchall()
    for item in items_panier:
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s '''
        mycursor.execute(sql, (client_id, item['id_velo']))

        sql=''' UPDATE velo SET stock=stock+%s WHERE id_velo=%s'''
        mycursor.execute(sql, (item['quantite'], item['id_velo']))

        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    #id_declinaison_article = request.form.get('id_declinaison_article')

    sql = ''' SELECT * FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s'''
    mycursor.execute(sql, (id_client, id_article))
    ligne_a_supprimer = mycursor.fetchone()
    if ligne_a_supprimer is not None:
        sql = ''' DELETE FROM ligne_panier WHERE id_utilisateur=%s AND id_velo=%s '''
        if (mycursor.execute(sql, (id_client, id_article)) == 1):
            sql = ''' UPDATE velo SET stock=stock+%s WHERE id_velo=%s;'''
            if (mycursor.execute(sql, (ligne_a_supprimer['quantite'], id_article)) == 1):
                get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word:" + filter_word + str(len(filter_word)))
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'votre Mot recherché doit uniquement être composé de lettres')
                # FIXME : On doit pouvoir cherché avec des chiffer
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop('filter_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and not filter_prix_max.isdecimal():
            session['filter_prix_min'] = filter_prix_min
        elif not filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            session['filter_prix_max'] = filter_prix_max
        elif filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    # FIXME : les min et max ne peux pas être retirer une fois set 
    print(filter_prix_min,filter_prix_max)
    if filter_types and filter_types != []:
        session['filter_types'] = filter_types
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/article/show')

  
