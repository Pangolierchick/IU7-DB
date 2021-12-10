from flask import Flask, redirect
from flask import render_template, request
from models import *
from db import *
import json
import sys
from datetime import date

@app.route('/', methods=['get', 'post'])
def main():
    return render_template('index.html')

@app.route('/exc1', methods=['get', 'post'])
def exc1():
    accs = Accs.query.join(Inventory, Accs.id == Inventory.user_id).add_columns(Accs.id, Inventory.appid).order_by(Inventory.appid).all()

    res = [{
        'id': acc.id,
        'name': acc.appid
    } for acc in accs]
    return  render_template('table.html', accs=res)

@app.route('/exc2', methods=['get', 'post'])
def exc2():
    apps = Apps.query.all()

    res = str([{
        'id': app.id,
        'name': app.name
    } for app in apps])

    if request.method == 'POST':
        if request.form.get('get_json'):
            return res
        elif request.form.get('update_json'):
            return render_template('insert.html', a_type='exc2_u')
        elif request.form.get('insert_json'):
            return render_template('insert.html', a_type='exc2_i')
    elif request.method == 'GET':
        return render_template('exc2.html')

@app.route('/exc2_i', methods=['get', 'post'])
def insert():
    id = request.form.get('g_id')
    game_name = request.form.get('g_name')
    studio_name = request.form.get('st_name')
    print(id, game_name, studio_name, file=sys.stderr)

    d = date.today().strftime("%d-%m-%Y")

    db.session.add(Apps(id, game_name, studio_name, d, "None", 0, 10))
    db.session.commit()

    r = Apps.query.filter_by(name='Dota 3').all()

    print(r, file=sys.stderr)

    return redirect('/exc2')

@app.route('/exc2_u', methods=['get', 'post'])
def update():
    id = request.form.get('g_id')
    game_name = request.form.get('g_name')
    studio_name = request.form.get('st_name')
    print(id, game_name, studio_name, file=sys.stderr)

    a = Apps.query.filter_by(id=id).first()

    a.name   = game_name
    a.author = studio_name

    db.session.commit()

    return redirect('/exc2')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
