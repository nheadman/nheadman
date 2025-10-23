# 🧠 Diagnostic Classification Database

A comprehensive, searchable database that cross-references **DSM-5-TR** and **ICD-11** diagnostic classifications, providing diagnostic criteria and detailed descriptions of mental health conditions.

## 📋 Features

- **🔍 Full-Text Search**: Search across disorder names, descriptions, and diagnostic criteria
- **🔗 Cross-References**: View equivalent and related codes between DSM-5-TR and ICD-11
- **📋 Detailed Criteria**: Access complete diagnostic criteria, specifiers, prevalence data, and differential diagnoses
- **📚 Browse by Category**: Explore disorders organized by diagnostic categories
- **💻 CLI Interface**: Command-line interface for quick searches and lookups
- **🌐 Web Interface**: Modern, user-friendly web application with beautiful UI
- **📊 Statistics**: Database statistics and overview
- **🔌 REST API**: JSON API endpoints for integration with other applications

## 🚀 Quick Start

### 1. Installation

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Initialize the Database

```bash
# Create and populate the database with sample data
python init_database.py
```

This will create `diagnostic_database.db` with:
- 13 DSM-5-TR disorders across multiple categories
- 23 ICD-11 disorders with detailed diagnostic requirements
- 16 cross-references between the systems
- Full-text search indexes

### 3. Use the Application

#### Option A: Web Interface (Recommended)

```bash
# Start the web server
python web_app.py
```

Then open your browser to: http://127.0.0.1:5000

The web interface provides:
- Beautiful, modern UI with responsive design
- Interactive search across both classification systems
- Detailed disorder pages with cross-references
- Category browsing
- Visual cross-reference mappings

#### Option B: Command-Line Interface

```bash
# Search across both systems
python search_cli.py search "depression" --system both

# Search only DSM-5-TR
python search_cli.py search "anxiety" --system dsm5 -v

# Look up a specific code
python search_cli.py lookup 296.21
python search_cli.py lookup 6A70

# Browse categories
python search_cli.py category --list --system dsm5
python search_cli.py category "Depressive Disorders" --system dsm5 -v

# View all cross-references
python search_cli.py crossref --list-all

# Show database statistics
python search_cli.py stats
```

For full CLI help:
```bash
python search_cli.py --help
python search_cli.py search --help
```

## 📚 Database Structure

### DSM-5-TR Table
- **Code**: DSM-5-TR diagnostic code (e.g., 296.21)
- **Name**: Full disorder name
- **Category**: Disorder category (e.g., "Depressive Disorders")
- **Description**: Brief description of the disorder
- **Diagnostic Criteria**: Complete diagnostic criteria from DSM-5-TR
- **Specifiers**: Available specifiers for the diagnosis
- **Prevalence**: Epidemiological data
- **Differential Diagnosis**: Other disorders to consider

### ICD-11 Table
- **Code**: ICD-11 diagnostic code (e.g., 6A70)
- **Name**: Full disorder name
- **Category**: Disorder category (e.g., "Mood disorders")
- **Description**: Description of the disorder
- **Diagnostic Requirements**: Diagnostic requirements from ICD-11
- **Exclusions**: Conditions to exclude
- **Coding Notes**: Additional coding information

### Cross-References Table
- Links DSM-5-TR and ICD-11 codes
- Relationship type: "equivalent" or "related"
- Notes about the mapping

## 🔌 API Endpoints

The web application provides REST API endpoints:

```bash
# Search
GET /api/search?q=depression&system=both

# Get disorder by code
GET /api/disorder/dsm5/296.21
GET /api/disorder/icd11/6A70

# Get statistics
GET /api/stats
```

Example API usage:
```bash
curl "http://127.0.0.1:5000/api/search?q=anxiety&system=both"
curl "http://127.0.0.1:5000/api/disorder/dsm5/300.01"
```

## 📖 Sample Disorders Included

### DSM-5-TR Categories:
- **Depressive Disorders**: Major Depressive Disorder (various severities), Persistent Depressive Disorder
- **Anxiety Disorders**: Panic Disorder, Generalized Anxiety Disorder, Social Anxiety Disorder
- **Trauma and Stressor-Related Disorders**: PTSD, Adjustment Disorder
- **Obsessive-Compulsive Disorders**: OCD
- **Neurodevelopmental Disorders**: ADHD
- **Bipolar Disorders**: Bipolar I, Bipolar II
- **Schizophrenia Spectrum**: Schizophrenia

### ICD-11 Categories:
- **Mood disorders**: Single/Recurrent depressive disorder, Dysthymic disorder, Bipolar disorders
- **Anxiety and fear-related disorders**: Panic disorder, GAD, Social anxiety, Specific phobia, Agoraphobia
- **Disorders specifically associated with stress**: PTSD, Complex PTSD, Prolonged grief, Adjustment disorder
- **Obsessive-compulsive or related disorders**: OCD, Body dysmorphic disorder, Hoarding disorder
- **Neurodevelopmental disorders**: ADHD
- **Schizophrenia or other primary psychotic disorders**: Schizophrenia

## 🎯 Use Cases

1. **Clinical Reference**: Quick lookup of diagnostic codes and criteria
2. **Code Conversion**: Find equivalent ICD-11 codes for DSM-5-TR diagnoses (and vice versa)
3. **Education**: Learning tool for mental health professionals and students
4. **Research**: Compare diagnostic criteria between classification systems
5. **Documentation**: Reference for medical billing and documentation

## ⚠️ Important Notes

- This database contains **sample data** for educational and reference purposes
- **Not intended for clinical diagnosis** - always consult official DSM-5-TR and ICD-11 resources
- The sample dataset includes common disorders but is not comprehensive
- Cross-references are approximate - some diagnoses may not have exact equivalents
- Always refer to the latest official publications for clinical practice

## 🛠️ Technical Details

- **Database**: SQLite with FTS5 (Full-Text Search)
- **Backend**: Python 3.7+
- **Web Framework**: Flask
- **CLI**: argparse
- **No external dependencies** beyond Flask for web interface

### Project Structure

```
diagnostic-classification-database/
├── init_database.py          # Database initialization and data population
├── database_operations.py    # Core database operations and search functions
├── search_cli.py            # Command-line interface
├── web_app.py               # Flask web application
├── templates/               # HTML templates for web interface
│   ├── base.html
│   ├── index.html
│   ├── search.html
│   ├── dsm5_detail.html
│   ├── icd11_detail.html
│   ├── categories.html
│   ├── category_detail.html
│   ├── crossref.html
│   └── 404.html
├── requirements.txt         # Python dependencies
├── diagnostic_database.db   # SQLite database (created by init_database.py)
└── README.md               # This file
```

## 🔄 Extending the Database

To add more disorders:

1. Edit `init_database.py`
2. Add entries to `dsm5_data` or `icd11_data` lists
3. Add cross-references to `cross_refs` list
4. Run `python init_database.py` to rebuild the database

## 📝 License

This project is for educational purposes. Diagnostic criteria are summarized from:
- **DSM-5-TR**: American Psychiatric Association
- **ICD-11**: World Health Organization

## 🤝 Contributing

This is a sample implementation. To extend:
- Add more disorders from DSM-5-TR and ICD-11
- Implement more sophisticated search algorithms
- Add user authentication for saved searches
- Export functionality (PDF, CSV)
- Multi-language support

## 📧 Contact

For questions or suggestions about this implementation, please refer to the repository.

---

**Disclaimer**: This tool is for educational and reference purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with questions regarding medical conditions.
