from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import animal
from flask_app.models import user

@app.route('/animalList')
def animals_list():
    if 'user_id' not in session: return redirect('/')
    animals = animal.Animal.getAll()
    return render_template('animalList.html', animals = animals)

@app.route('/animal/new')
def animal_new():
    if 'user_id' not in session: return redirect('/')
    return render_template('newAnimal.html')

@app.route("/animal/create", methods = ['POST'])
def animal_show():
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.save(request.form):
        return redirect('/animalList')
    return redirect("/animal/new")

@app.route('/animal/edit/<int:num>')
def animal_edit(num):
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.is_user_creator_of_animal(num):
        animals = animal.Animal.getOne(num)
        return render_template('updateAnimal.html', animals = animals)
    return redirect('/animalList')

@app.route('/animal/change/<int:num>', methods = ["POST"])
def change(num):
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.update(request.form, num):
        return redirect('/animalList')
    return redirect(f'/animal/edit/{num}')

@app.route('/animal/<int:id>')
def animal_display(id):
    if 'user_id' not in session: return redirect('/')
    animals = animal.Animal.getOne(id)
    return render_template('display.html', animals = animals)

@app.route('/delete/<int:num>')
def delete(num):
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.is_user_creator_of_animal(num):
        animal.Animal.delete(num)
        return redirect('/animalList')
    return redirect('/animalList')