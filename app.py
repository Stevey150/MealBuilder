import os
import pandas as pd
import ast  # To safely convert string representations of lists into actual lists
from flask import Flask, render_template, request

# Load the dataset
dataset_path = "data.csv"  # Update to your actual dataset path
try:
    data = pd.read_csv(dataset_path).iloc[:, 1:]  # Skip the first unnamed column
    print("Dataset loaded successfully.")
    
    # Convert string representations of lists into actual lists
    data['Ingredients'] = data['Ingredients'].apply(ast.literal_eval)
    data['Cleaned_Ingredients'] = data['Cleaned_Ingredients'].apply(ast.literal_eval)

except Exception as e:
    print("Error loading dataset:", e)
    data = pd.DataFrame()

# Initialize Flask app
app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get input ingredients from the form
    input_ingredients = request.form.get('ingredients')
    print("Received input ingredients:", input_ingredients)

    if not input_ingredients:
        return render_template('results.html', recipes=[], message="No ingredients provided.")

    # Process input ingredients into a list of lowercased, stripped terms
    input_ingredients_list = [ingredient.strip().lower() for ingredient in input_ingredients.split(",")]
    print("Input ingredients list:", input_ingredients_list)

    # Filter recipes based on matching any part of the ingredients
    def ingredient_match(cleaned_ingredients):
        # Check if any of the input ingredients are a substring of the recipe ingredients
        for input_ingredient in input_ingredients_list:
            for ingredient in cleaned_ingredients:
                if input_ingredient in ingredient.lower():
                    return True
        return False

    # Apply the matching function
    filtered_data = data[data['Cleaned_Ingredients'].apply(ingredient_match)]

    # Convert filtered recipes to a list of dictionaries for rendering
    recipes = filtered_data[['Title', 'Ingredients', 'Instructions', 'Image_Name']].to_dict(orient='records')

    if recipes:
        return render_template('results.html', recipes=recipes, message=f"Found {len(recipes)} recipes.")
    else:
        return render_template('results.html', recipes=[], message="No recipes found with those ingredients.")

if __name__ == '__main__':
    app.run(debug=True)