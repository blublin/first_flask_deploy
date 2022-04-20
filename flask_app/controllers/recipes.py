from flask import render_template, redirect, request
from flask_app import app, Bcrypt, flash, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from datetime import datetime

## Toggle to run all debug statements to track data flow
## True = On, False = Off
debug = True



@app.route('/recipes/show/<int:id>')
def show_recipe(id):
    if debug:
        print(f"Session while attempting to access success: {session}")
        print(f"ID of recipe attempting to get: {id}")
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')
    data = {'id' : id}
    recipe = Recipe.get_one(data)

    conv_date = recipe.origin_date.strftime("%B %d, %Y")
    if debug:
        print(conv_date)
    return render_template("recipe_show.html", recipe=recipe, conv_date=conv_date)

@app.route('/recipes/new')
def new_recipe():
    if debug:
        print(f"Session while attempting to access success: {session}")
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')

    return render_template("recipe_edit.html")

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/recipes/create',methods=['POST'])
def create_recipe():
    if debug:
        print(f"Session while attempting to access success: {session}")
        print(f"Request Form dict: {request.form}")
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')    

    data = request.form.copy()
    data['user_id'] = session['user_id']
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')    
    data ={ 
        "id":id
    }
    recipe=Recipe.get_one(data)
    if debug:
        print(f"name: {recipe.name}")
        print(f"description: {recipe.description}")
        print(f"instructions: {recipe.instructions}")
        print(f"under_30: {recipe.under_30}")
        print(f"origin_date: {recipe.origin_date}")
    return render_template("recipe_edit.html",recipe=recipe)

# TODO ONE TO HANDLE THE DATA FROM THE FORM
@app.route('/recipes/update',methods=['POST'])
def update_recipe():
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')    

    Recipe.update(request.form)
    if debug:
        print(f"Update form: {request.form}")
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def destroy_recipe(id):
    if not 'logged_in' in session:
        flash("Please login before continuining.", "login")
        return redirect ('/')    
    data ={ 'id': id }
    Recipe.del_one(data)
    # Redirect show all or index?
    return redirect('/dashboard')