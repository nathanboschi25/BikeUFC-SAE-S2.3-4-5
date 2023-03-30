#! /usr/bin/python
# -*- coding:utf-8 -*-
import datetime

from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_liste_envies = Blueprint('client_liste_envies', __name__,
                                template_folder='templates')


@client_liste_envies.route('/client/envie/add', methods=['get'])
def client_liste_envies_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    return redirect('/client/article/show')


@client_liste_envies.route('/client/envie/delete', methods=['get'])
def client_liste_envies_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')
    return redirect('/client/envies/show')


@client_liste_envies.route('/client/envies/show', methods=['get'])
def client_liste_envies_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    articles_liste_envies = []

    sql = '''SELECT
                h.id_velo as id_article,
                v.libelle_velo as nom,
                v.prix_velo as prix,
                v.image_velo as image
             FROM historique h
             LEFT JOIN velo v on h.id_velo = v.id_velo
             WHERE id_utilisateur=%s;'''
    mycursor.execute(sql, id_client)
    articles_historique = mycursor.fetchall()
    return render_template('client/liste_envies/liste_envies_show.html'
                           , articles_liste_envies=articles_liste_envies
                           , articles_historique=articles_historique
                           # , nb_liste_envies= nb_liste_envies
                           )


def client_historique_add(article_id, client_id):
    mycursor = get_db().cursor()
    sql = "SELECT * FROM historique WHERE id_utilisateur=%s AND id_velo=%s ORDER BY datetime_visite DESC LIMIT 1"
    mycursor.execute(sql, (client_id, article_id))
    historique = mycursor.fetchone()
    if len(historique) == 0 :
        sql = "INSERT INTO historique VALUE (%s, %s, NOW())"
        mycursor.execute(sql, (client_id, article_id))
        sql = '''
            DELETE FROM historique
            WHERE id_utilisateur=%s 
                and (id_utilisateur, id_velo, datetime_visite) 
                NOT IN (
                SELECT * FROM(
                    SELECT id_utilisateur, id_velo, datetime_visite
                    FROM historique
                    WHERE id_utilisateur = %s
                    ORDER BY datetime_visite DESC
                    LIMIT 6
                ) as t);
        '''
        mycursor.execute(sql, (client_id, client_id))
        get_db().commit()

@client_liste_envies.route('/client/envies/up', methods=['get'])
@client_liste_envies.route('/client/envies/down', methods=['get'])
@client_liste_envies.route('/client/envies/last', methods=['get'])
@client_liste_envies.route('/client/envies/first', methods=['get'])
def client_liste_envies_article_move():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.args.get('id_article')

    return redirect('/client/envies/show')
