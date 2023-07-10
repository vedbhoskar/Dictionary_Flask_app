from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get the search term from the form
    search_term = request.form['term']

    # Make a request to the Merriam-Webster Dictionary API
    merriam_webster_api_key = '0e3fdd96-c60f-48d9-bebe-3f2f5e4948f9'
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{search_term}'
    params = {'key': merriam_webster_api_key}
    response = requests.get(url, params=params)

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            definitions = [entry['shortdef'][0] for entry in data if 'shortdef' in entry]
            if definitions:
                return render_template('results.html', term=search_term, definitions=definitions)
        return render_template('results.html', term=search_term, error='No definitions found.')
    else:
        return render_template('results.html', term=search_term, error='An error occurred.')

if __name__ == '__main__':
    app.run(debug=True)
