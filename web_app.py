#!/usr/bin/env python3
"""
Web interface for the diagnostic classification database.
A modern Flask application for searching and browsing DSM-5-TR and ICD-11.
"""

from flask import Flask, render_template, request, jsonify
from database_operations import DiagnosticDatabase
from pathlib import Path

app = Flask(__name__)
db = DiagnosticDatabase()

# Color schemes for different categories
CATEGORY_COLORS = {
    'Depressive': '#4A90E2',
    'Anxiety': '#50C878',
    'Trauma': '#E94B3C',
    'Obsessive': '#9B59B6',
    'Neurodevelopmental': '#F39C12',
    'Bipolar': '#E67E22',
    'Schizophrenia': '#95A5A6',
    'Mood': '#3498DB',
}


@app.route('/')
def index():
    """Home page."""
    stats = db.get_statistics()
    return render_template('index.html', stats=stats)


@app.route('/search')
def search():
    """Search page."""
    query = request.args.get('q', '')
    system = request.args.get('system', 'both')
    
    if not query:
        return render_template('search.html', results=None, query='', system=system)
    
    if system == 'both':
        results = db.search_all(query, limit=50)
    elif system == 'dsm5':
        results = {'dsm5': db.search_dsm5(query, limit=50), 'icd11': []}
    else:
        results = {'dsm5': [], 'icd11': db.search_icd11(query, limit=50)}
    
    return render_template('search.html', results=results, query=query, system=system)


@app.route('/disorder/dsm5/<code>')
def dsm5_disorder(code):
    """DSM-5-TR disorder detail page."""
    disorder = db.get_dsm5_by_code(code)
    if not disorder:
        return render_template('404.html', message=f"DSM-5-TR disorder {code} not found"), 404
    
    xrefs = db.get_icd11_from_dsm5(code)
    return render_template('dsm5_detail.html', disorder=disorder, xrefs=xrefs)


@app.route('/disorder/icd11/<code>')
def icd11_disorder(code):
    """ICD-11 disorder detail page."""
    disorder = db.get_icd11_by_code(code)
    if not disorder:
        return render_template('404.html', message=f"ICD-11 disorder {code} not found"), 404
    
    xrefs = db.get_dsm5_from_icd11(code)
    return render_template('icd11_detail.html', disorder=disorder, xrefs=xrefs)


@app.route('/categories')
def categories():
    """Browse categories page."""
    system = request.args.get('system', 'dsm5')
    
    if system == 'dsm5':
        cats = db.list_dsm5_categories()
    else:
        cats = db.list_icd11_categories()
    
    return render_template('categories.html', categories=cats, system=system)


@app.route('/category/<system>/<category>')
def category_detail(system, category):
    """Category detail page showing all disorders in category."""
    if system == 'dsm5':
        disorders = db.get_dsm5_by_category(category)
    else:
        disorders = db.get_icd11_by_category(category)
    
    return render_template('category_detail.html', 
                          disorders=disorders, 
                          category=category, 
                          system=system)


@app.route('/crossref')
def crossref():
    """Cross-reference page."""
    xrefs = db.get_all_cross_references()
    return render_template('crossref.html', xrefs=xrefs)


@app.route('/api/search')
def api_search():
    """API endpoint for search."""
    query = request.args.get('q', '')
    system = request.args.get('system', 'both')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    if system == 'both':
        results = db.search_all(query, limit=50)
    elif system == 'dsm5':
        results = {'dsm5': db.search_dsm5(query, limit=50), 'icd11': []}
    else:
        results = {'dsm5': [], 'icd11': db.search_icd11(query, limit=50)}
    
    return jsonify(results)


@app.route('/api/disorder/<system>/<code>')
def api_disorder(system, code):
    """API endpoint for disorder lookup."""
    if system == 'dsm5':
        disorder = db.get_dsm5_by_code(code)
        if disorder:
            disorder['xrefs'] = db.get_icd11_from_dsm5(code)
    else:
        disorder = db.get_icd11_by_code(code)
        if disorder:
            disorder['xrefs'] = db.get_dsm5_from_icd11(code)
    
    if not disorder:
        return jsonify({'error': 'Disorder not found'}), 404
    
    return jsonify(disorder)


@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics."""
    return jsonify(db.get_statistics())


@app.template_filter('get_category_color')
def get_category_color(category):
    """Template filter to get color for category."""
    for key, color in CATEGORY_COLORS.items():
        if key.lower() in category.lower():
            return color
    return '#34495E'  # Default color


if __name__ == '__main__':
    # Ensure database exists
    if not Path('diagnostic_database.db').exists():
        print("Error: Database not found. Please run 'python init_database.py' first.")
        exit(1)
    
    print("\n" + "=" * 80)
    print("Diagnostic Classification Database - Web Interface")
    print("=" * 80)
    print("\nStarting server at http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server\n")
    print("=" * 80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
