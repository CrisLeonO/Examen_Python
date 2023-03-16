from app import app
from flask import Flask, render_template, request, redirect, session
from app.models.user import User
from app.models.poke import Poke


@app.route('/post_poke', methods=['POST'])
def post_poke():
    if 'user_id' not in session:
        return redirect('/main')

    data = {
        "sender_id":  request.form['sender_id'],
        "receiver_id": request.form['receiver_id'],
    }
    Poke.save(data)
    return redirect('/pokes')


@app.route('/pokes_count')
def count_pokes():
    count = count.count_pokes()
    return render_template('/pokes.html', count = count)
