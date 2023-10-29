from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rezearch.db'
db = SQLAlchemy(app)

class Rezearch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    link = db.Column(db.String(750), nullable=False)
    prim_category = db.Column(db.String(50), nullable=False)
    sec_category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(300), nullable=False)

@app.route('/submit', methods=['POST'])   
def submit():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        link = request.form['link']
        prim_category = request.form['category_1']
        sec_category = request.form['category_2']
        description = request.form['description']
        keywords = request.form['keywords']
    
        new_research = Rezearch(name=name, date=date, link=link, prim_category=prim_category, sec_category=sec_category, description=description, keywords=keywords)
        db.session.add(new_research)
        db.session.commit()
        return redirect(url_for('homepage_2'))
    
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword-input')
    category = request.form.get('category')

    filters = []
    
    if category == "none" and not keyword:
            return redirect(url_for('view_existing'))
    
    if keyword:
        keyword_filter = (Rezearch.keywords.like(f"%{keyword}%") | 
                          Rezearch.name.like(f"%{keyword}%") | 
                          Rezearch.description.like(f"%{keyword}%"))
        filters.append(keyword_filter)

    if category == "all":
            results = Rezearch.query.filter(*filters).all()
    else:
        if category != "none":
            category_filter = (Rezearch.prim_category == category) | (Rezearch.sec_category == category)
            filters.append(category_filter)

    results = Rezearch.query.filter(*filters).all()
    return render_template('view-table.html', results=results)
    
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/homepage_2')
def homepage_2():
    return render_template('homepage-2.html')

@app.route('/view_existing')
def view_existing():
    return render_template('view-existing.html')

@app.route('/table_view')
def table_view():
    return render_template('view-table.html')

if __name__ == '__main__':
    app.run(debug=True)
