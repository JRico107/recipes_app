from flask_app import app
from flask import request, render_template, redirect, session, flash
from flask_app.models.models_recipe import Recipe
from flask_app.models.models_user import User


@app.route("/recipes/home")
def recipes_home():
    if "user_id" not in session:
        flash("Please log in to access the dashboard.")
        return redirect("/")
    
    user = User.get_one_by_id(session["user_id"])
    recipes = Recipe.get_all()
    return render_template("/dashboard.html", user=user, recipes=recipes)

# recipe details
@app.route("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    print("In details:", recipe_id)
    recipe = Recipe.get_one_by_id(recipe_id)
    data = {
            "id": session["user_id"]
        }
    user = User.get_one_by_id(data)
    return render_template('recipe_detail.html', recipe=recipe, user = user )


# new
@app.route("/recipes/new_recipe")
def create_page():
    print("In create route")
    return render_template("new_recipe.html")


# edit page
@app.route('/recipes/edit/<int:recipe_id>')
def edit_page(recipe_id):
    print("In edit page:", recipe_id)
    recipe = Recipe.get_one_by_id(recipe_id)
    return render_template('edit.html',recipe=recipe)

#delete 
@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    print("In delete page:", recipe_id)
    Recipe.delete_by_id(recipe_id)
    return redirect('/recipes/home')


#create (post)
@app.route('/recipes', methods=['POST'])
def create_recipe():
    print("In the create process route:", request.form)
    is_valid = Recipe.is_valid(request.form)

    if is_valid:
        data = {
            'name':request.form['name'], 
            'description':request.form['description'],
            'instructions':request.form['instructions'],
            'date_made':request.form['date_made'],
            'under_30':request.form['under_30'],
            'user_id':session['user_id']

        }
        Recipe.save(data)
        return redirect('/dashboard')
    return redirect('/recipes/new_recipe')

#update (post)
@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    print("In update post route: ",request.form)
    is_valid = Recipe.is_valid(request.form)

    if is_valid:
        Recipe.update_recipe(request.form)
        return redirect('/dashboard')
    return redirect(f'/recipes/edit/{request.form['id']}')

