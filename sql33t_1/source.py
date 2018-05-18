# Embedded file name: /app/sqli_lv1/content/app/sql/views.py
from flask import render_template, request, flash, current_app, send_file
from ..app import db
from . import sql
from .models import Darkside, Lightside
from hashlib import sha256
import re
import sqlite3

@sql.before_app_first_request
def init_app():
    if db.session.query(Lightside).count() == 2:
        return
    realJEDI = Lightside(username=current_app.config['USER'], password=sha256(current_app.config['PASSWD']).hexdigest())
    jedi = Lightside(username=current_app.config['USER'], password=sha256(current_app.config['USER']).hexdigest())
    stormtrooper = Darkside(username='stormtrooper', password=sha256('stormtrooper').hexdigest())
    db.session.add(stormtrooper)
    db.session.add(jedi)
    db.session.add(realJEDI)
    db.session.commit()


@sql.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@sql.route('/pyc', methods=['GET'])
def pyc():
    return send_file(__file__)


@sql.route('/login', methods=['GET'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')
    side = request.args.get('side', '')
    if username == '':
        flash('Please enter a username')
        return render_template('login.html')
    elif password == '':
        flash('Please enter a password')
        return render_template('login.html')
    elif side == '':
        flash('Please select a side')
        return render_template('login.html')
    else:
        con = sqlite3.connect('app/sqli_lv1.sqlite')
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        try:
            query = " SELECT username\n                        FROM `%s`\n                        WHERE username='%s' LIMIT 1" % (sql_filter(side), sql_filter(username))
            cur.execute(query)
            result = cur.fetchone()
            if result != None:
                query = " SELECT *\n                            FROM `%s`\n                            WHERE password='%s' and username='%s' LIMIT 1" % (sql_filter(side), sha256(password).hexdigest(), sql_filter(username))
                cur.execute(query)
            else:
                flash('That username did not exist!')
                return render_template('login.html')
        except sqlite3.Error as e:
            error_msg = xss_filter('error: {0}.'.format(e.args[0]))
            query = xss_filter('query: {0}.'.format(query))
            print '[+] sql error: ', e, query

        result = cur.fetchone()
        if result == None:
            flash('Invalid username/password')
        elif result['username'] == current_app.config['USER'] and result['password'] == sha256(current_app.config['PASSWD']).hexdigest():
            flash('Are you realJEDI? This is your lightsaber! {0}'.format(current_app.config['FLAG']))
        else:
            flash('Welcome back <b>{0}</b> ! Sorry, we are under construction!'.format(xss_filter(username)))
        return render_template('login.html')


def xss_filter(payload):
    payload = payload.replace('<', '&lt;').replace('>', '&gt;')
    return payload


sql_blacklist = ['drop',
 'my',
 'heart',
 'set',
 'love',
 '=',
 'null',
 'where',
 'you',
 'is',
 'not',
 'like',
 'me',
 'by',
 'insert',
 'limit',
 'from',
 '1',
 '2',
 '3',
 '5',
 ';']

def addslashes(s):
    d = {'"': '\\"',
     "'": "\\'",
     '\x00': '\\\x00',
     '\\': '\\\\'}
    return ''.join((d.get(c, c) for c in s))


def sql_filter(payload):
    for badword in sql_blacklist:
        regex = re.compile(re.escape(badword), re.I)
        payload = regex.sub('***', payload)

    payload = addslashes(payload)
    return payload