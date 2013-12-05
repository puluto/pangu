# -*- coding: utf-8 -*
from flask import Blueprint, render_template, flash, redirect, url_for, session, request, g
from pangu import db, app
from pangu.manufacture.forms import EditForm, DetailForm 
from pangu.manufacture.models import Manufacture

mod = Blueprint('manufacture', __name__)

@mod.route('/delete/<int:id>')
def delete(id):
    manufacture = Manufacture.query.filter_by(id=id).first()
    db.session.delete(manufacture)
    db.session.commit()
    return redirect(url_for('manufacture.list'))

@mod.route('/')
def list():
    manufactures = Manufacture.query.order_by(Manufacture.id)
    return render_template('manufacture/list.html', manufactures=manufactures)

@mod.route('/add/', methods=['GET', 'POST'])
def add():
    form = EditForm(request.form)
    if form.validate_on_submit():
        manufacture = Manufacture()
        form.populate_obj(manufacture)
        db.session.add(manufacture)
        db.session.commit()
        return redirect(url_for('manufacture.list')) 
    return render_template('manufacture/edit.html', form=form)

@mod.route('/detail/<int:id>')
def detail(id):
    manufacture = Manufacture.query.filter_by(id=id).first()
    form = DetailForm(request.form, manufacture)
    return render_template('manufacture/detail.html', form=form)

@mod.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    manufacture = Manufacture.query.filter_by(id=id).first()
    form = EditForm(request.form, manufacture)
    if form.validate_on_submit():
        form.populate_obj(manufacture)
        db.session.commit()
        return redirect(url_for('manufacture.list')) 
    return render_template('manufacture/edit.html', form=form)
