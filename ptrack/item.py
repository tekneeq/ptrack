from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ptrack.auth import login_required
from ptrack.db import get_db

bp = Blueprint('item', __name__)

@bp.route('/')
def index():
    db = get_db()
    items = db.execute(
        'SELECT i.id, title, body, created, user_id, username'
        ' FROM item i JOIN user u ON i.user_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('item/index.html', items=items)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO item (title, body, user_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('item.index'))

    return render_template('item/create.html')

def get_item(id, check_author=True):
    item = get_db().execute(
        'SELECT i.id, title, body, created, user_id, username'
        ' FROM item i JOIN user u ON i.user_id = u.id'
        ' WHERE i.id = ?',
        (id,)
    ).fetchone()

    if item is None:
        abort(404, f"Item id {id} doesn't exist.")

    if check_author and item['user_id'] != g.user['id']:
        abort(403)

    return item

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    item = get_item(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE item SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('item.index'))

    return render_template('item/update.html', item=item)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_item(id)
    db = get_db()
    db.execute('DELETE FROM item WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('item.index'))