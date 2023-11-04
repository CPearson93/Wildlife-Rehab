from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import animal

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
        return redirect('/animals')
    return redirect("/animal/new")

@app.route('/animal/edit/<int:num>')
def animal_edit(num):
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.validate_action(num):
        animals = animal.Animal.get_this_show(num)
        return render_template('updateAnimal.html', animals = animals)
    return redirect('/animalList')

@app.route('/animal/change/<int:num>', methods = ["POST"])
def change(num):
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.update_animal(request.form, num):
        return redirect('/animalList')
    return redirect(f'/animal/edit/{num}')

@app.route('/animal/<int:num>')
def show_display(num):
    if 'user_id' not in session: return redirect('/')
    animals = animal.Animal.get_this_animal(num)
    return render_template('display.html', animals = animals)

@app.route('/delete/<int:num>')
def delete(num):
    if 'user_id' not in session: return redirect('/')
    if animal.Animal.validate_action(num):
        animal.Animal.remove_show(num)
        return redirect('/animalList')
    return redirect('/animalList')