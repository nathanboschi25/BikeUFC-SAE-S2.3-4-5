#! /usr/bin/python
# -*- coding:utf-8 -*-
import pymysql
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_coordonnee = Blueprint('client_coordonnee', __name__,
                        template_folder='templates')

@client_coordonnee.route('/client/coordonnee/show')
def client_coordonnee_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = 'SELECT * FROM adresse WHERE id_utilisateur=%s'
    mycursor.execute(sql, id_client)
    adresses = mycursor.fetchall()

    sql = 'SELECT * FROM utilisateur WHERE id_utilisateur=%s'
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()

    nb_adresses = 10
    return render_template('client/coordonnee/show_coordonnee.html'
                           , utilisateur=utilisateur
                           , adresses=adresses
                           , nb_adresses=nb_adresses
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['GET'])
def client_coordonnee_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = 'SELECT * FROM utilisateur WHERE id_utilisateur=%s'
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()
    return render_template('client/coordonnee/edit_coordonnee.html'
                           , user=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/edit', methods=['POST'])
def client_coordonnee_edit_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom = request.form.get('nom')
    login = request.form.get('login')
    email = request.form.get('email')

    sql = 'UPDATE utilisateur SET nom=%s, login=%s, email=%s WHERE id_utilisateur=%s'
    mycursor.execute(sql, (nom, login, email, id_client))

    get_db().commit()
    return redirect('/client/coordonnee/show')


@client_coordonnee.route('/client/coordonnee/delete_adresse',methods=['POST'])
def client_coordonnee_delete_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse= request.form.get('id_adresse')

    try:
        mycursor.execute('DELETE FROM adresse WHERE id_utilisateur=%s AND id_adresse=%s', (id_client, id_adresse))
        get_db().commit()
    except pymysql.Error as e:
        flash("Erreur : L'adresse n'as pas pu être supprimée", 'alert-warning')
    return redirect('/client/coordonnee/show')

@client_coordonnee.route('/client/coordonnee/add_adresse')
def client_coordonnee_add_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = 'SELECT * FROM utilisateur WHERE id_utilisateur=%s'
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()
    return render_template('client/coordonnee/add_adresse.html'
                           , utilisateur=utilisateur
                           )

@client_coordonnee.route('/client/coordonnee/add_adresse',methods=['POST'])
def client_coordonnee_add_adresse_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    sql = 'INSERT INTO adresse(id_utilisateur, nom, rue, code_postal, ville) VALUE (%s, %s, %s, %s, %s)'
    mycursor.execute(sql, (id_client, nom, rue, code_postal, ville))
    get_db().commit()
    return redirect('/client/commande/valide')

@client_coordonnee.route('/client/coordonnee/edit_adresse')
def client_coordonnee_edit_adresse():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse = request.args.get('id_adresse')

    sql = 'SELECT * FROM utilisateur WHERE id_utilisateur=%s'
    mycursor.execute(sql, id_client)
    utilisateur = mycursor.fetchone()

    sql = 'SELECT * FROM adresse WHERE id_adresse=%s'
    mycursor.execute(sql, id_adresse)
    adresse = mycursor.fetchone()
    return render_template('/client/coordonnee/edit_adresse.html'
                            , utilisateur=utilisateur
                            , adresse=adresse
                           )

@client_coordonnee.route('/client/coordonnee/edit_adresse',methods=['POST'])
def client_coordonnee_edit_adresse_recoit():
    mycursor = get_db().cursor()
    nom= request.form.get('nom')
    rue = request.form.get('rue')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')
    id_adresse = request.form.get('id_adresse')

    sql = 'UPDATE adresse SET nom=%s, rue=%s, code_postal=%s, ville=%s WHERE id_adresse=%s'
    mycursor.execute(sql, (nom, rue, code_postal, ville, id_adresse))
    get_db().commit()

    return redirect('/client/coordonnee/show')