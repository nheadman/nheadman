# Usage Examples

This document provides comprehensive examples of how to use the Diagnostic Classification Database.

## Table of Contents
- [Command-Line Interface (CLI)](#command-line-interface-cli)
- [Web Interface](#web-interface)
- [REST API](#rest-api)
- [Python Integration](#python-integration)

---

## Command-Line Interface (CLI)

### Basic Search

Search across both DSM-5-TR and ICD-11:
```bash
python3 search_cli.py search "depression"
```

Search with verbose output (shows descriptions):
```bash
python3 search_cli.py search "anxiety" --system both -v
```

Search only DSM-5-TR:
```bash
python3 search_cli.py search "panic" --system dsm5
```

Search only ICD-11:
```bash
python3 search_cli.py search "bipolar" --system icd11
```

Limit number of results:
```bash
python3 search_cli.py search "mood" --limit 10
```

### Code Lookup

Look up a DSM-5-TR code (automatically shows ICD-11 cross-references):
```bash
python3 search_cli.py lookup 296.21
python3 search_cli.py lookup 300.01
python3 search_cli.py lookup 309.81
```

Look up an ICD-11 code (automatically shows DSM-5-TR cross-references):
```bash
python3 search_cli.py lookup 6A70
python3 search_cli.py lookup 6B01
python3 search_cli.py lookup 6B40
```

### Browse by Category

List all DSM-5-TR categories:
```bash
python3 search_cli.py category --list --system dsm5
```

List all ICD-11 categories:
```bash
python3 search_cli.py category --list --system icd11
```

View all disorders in a DSM-5-TR category:
```bash
python3 search_cli.py category "Depressive Disorders" --system dsm5
python3 search_cli.py category "Anxiety Disorders" --system dsm5 -v
```

View all disorders in an ICD-11 category:
```bash
python3 search_cli.py category "Mood disorders" --system icd11
python3 search_cli.py category "Anxiety and fear-related disorders" --system icd11 -v
```

### Cross-References

View all cross-references between DSM-5-TR and ICD-11:
```bash
python3 search_cli.py crossref --list-all
```

### Database Statistics

Show database statistics:
```bash
python3 search_cli.py stats
```

### Help

Get general help:
```bash
python3 search_cli.py --help
```

Get help for a specific command:
```bash
python3 search_cli.py search --help
python3 search_cli.py lookup --help
python3 search_cli.py category --help
```

---

## Web Interface

### Starting the Server

```bash
python3 web_app.py
```

Then open your browser to: http://127.0.0.1:5000

### Available Pages

1. **Home Page** (`/`)
   - Database statistics
   - Quick search form
   - Feature overview

2. **Search Page** (`/search`)
   - Search across both or individual systems
   - Results grouped by classification system
   - Links to detailed disorder pages

3. **Disorder Detail Pages**
   - DSM-5-TR: `/disorder/dsm5/<code>`
   - ICD-11: `/disorder/icd11/<code>`
   - Complete diagnostic information
   - Cross-references to other system

4. **Categories Page** (`/categories`)
   - Browse DSM-5-TR or ICD-11 categories
   - Switch between systems

5. **Category Detail** (`/category/<system>/<category>`)
   - List all disorders in a category
   - Links to individual disorders

6. **Cross-References** (`/crossref`)
   - Visual mapping between systems
   - Relationship types (equivalent/related)

### Example URLs

```
# Home
http://127.0.0.1:5000/

# Search
http://127.0.0.1:5000/search?q=depression&system=both
http://127.0.0.1:5000/search?q=anxiety&system=dsm5

# Disorder details
http://127.0.0.1:5000/disorder/dsm5/296.21
http://127.0.0.1:5000/disorder/icd11/6A70

# Categories
http://127.0.0.1:5000/categories?system=dsm5
http://127.0.0.1:5000/category/dsm5/Depressive%20Disorders

# Cross-references
http://127.0.0.1:5000/crossref
```

---

## REST API

The web application provides JSON API endpoints for programmatic access.

### Search Endpoint

**Endpoint:** `GET /api/search`

**Parameters:**
- `q` (required): Search query
- `system` (optional): `both`, `dsm5`, or `icd11` (default: `both`)

**Example:**
```bash
curl "http://127.0.0.1:5000/api/search?q=depression&system=both"
```

**Response:**
```json
{
  "dsm5": [
    {
      "id": 1,
      "code": "296.21",
      "name": "Major Depressive Disorder, Single Episode, Mild",
      "category": "Depressive Disorders",
      "description": "A mental disorder characterized by...",
      ...
    }
  ],
  "icd11": [
    {
      "id": 1,
      "code": "6A70",
      "name": "Single episode depressive disorder",
      ...
    }
  ]
}
```

### Disorder Lookup Endpoint

**Endpoint:** `GET /api/disorder/<system>/<code>`

**Parameters:**
- `system`: `dsm5` or `icd11`
- `code`: Diagnostic code

**Examples:**
```bash
# DSM-5-TR
curl "http://127.0.0.1:5000/api/disorder/dsm5/296.21"

# ICD-11
curl "http://127.0.0.1:5000/api/disorder/icd11/6A70"
```

**Response:**
```json
{
  "id": 1,
  "code": "296.21",
  "name": "Major Depressive Disorder, Single Episode, Mild",
  "category": "Depressive Disorders",
  "description": "...",
  "diagnostic_criteria": "...",
  "xrefs": [
    {
      "icd11_code": "6A70",
      "icd11_name": "Single episode depressive disorder",
      "relationship_type": "equivalent",
      "notes": "..."
    }
  ]
}
```

### Statistics Endpoint

**Endpoint:** `GET /api/stats`

**Example:**
```bash
curl "http://127.0.0.1:5000/api/stats"
```

**Response:**
```json
{
  "dsm5_disorders": 13,
  "icd11_disorders": 23,
  "cross_references": 16,
  "dsm5_categories": 7,
  "icd11_categories": 7
}
```

---

## Python Integration

### Direct Database Access

```python
from database_operations import DiagnosticDatabase

# Initialize database
db = DiagnosticDatabase()

# Search across both systems
results = db.search_all("depression", limit=10)
print(f"Found {len(results['dsm5'])} DSM-5-TR results")
print(f"Found {len(results['icd11'])} ICD-11 results")

# Search DSM-5-TR only
dsm5_results = db.search_dsm5("anxiety", limit=20)
for disorder in dsm5_results:
    print(f"{disorder['code']}: {disorder['name']}")

# Look up by code
disorder = db.get_dsm5_by_code("296.21")
if disorder:
    print(disorder['name'])
    print(disorder['diagnostic_criteria'])

# Get cross-references
xrefs = db.get_icd11_from_dsm5("296.21")
for xref in xrefs:
    print(f"ICD-11: {xref['icd11_code']} - {xref['icd11_name']}")

# Browse by category
disorders = db.get_dsm5_by_category("Depressive Disorders")
for disorder in disorders:
    print(f"{disorder['code']}: {disorder['name']}")

# Get statistics
stats = db.get_statistics()
print(f"Total disorders: {stats['dsm5_disorders'] + stats['icd11_disorders']}")
```

### Using the API Programmatically

```python
import requests

BASE_URL = "http://127.0.0.1:5000/api"

# Search
response = requests.get(f"{BASE_URL}/search", params={
    "q": "depression",
    "system": "both"
})
results = response.json()

# Get disorder
response = requests.get(f"{BASE_URL}/disorder/dsm5/296.21")
disorder = response.json()

# Get statistics
response = requests.get(f"{BASE_URL}/stats")
stats = response.json()
```

### Custom Query Examples

```python
from database_operations import DiagnosticDatabase

db = DiagnosticDatabase()

# Find all anxiety disorders
anxiety_disorders = db.get_dsm5_by_category("Anxiety")
print(f"Found {len(anxiety_disorders)} anxiety disorders")

# List all categories
categories = db.list_dsm5_categories()
for cat in categories:
    disorders = db.get_dsm5_by_category(cat)
    print(f"{cat}: {len(disorders)} disorders")

# Get all cross-references
all_xrefs = db.get_all_cross_references()
equivalent_count = sum(1 for x in all_xrefs if x['relationship_type'] == 'equivalent')
related_count = sum(1 for x in all_xrefs if x['relationship_type'] == 'related')
print(f"Equivalent mappings: {equivalent_count}")
print(f"Related mappings: {related_count}")
```

---

## Common Use Cases

### 1. Find ICD-11 Code for Billing

```bash
# Look up DSM-5-TR code to find ICD-11 equivalent
python3 search_cli.py lookup 296.21

# Or use the web interface
# Visit: http://127.0.0.1:5000/disorder/dsm5/296.21
```

### 2. Compare Diagnostic Criteria

Look up the same disorder in both systems and compare:
```bash
python3 search_cli.py lookup 296.21  # DSM-5-TR
python3 search_cli.py lookup 6A70    # ICD-11
```

### 3. Explore a Category

```bash
# List all depressive disorders
python3 search_cli.py category "Depressive Disorders" --system dsm5 -v

# Or browse in web interface
# Visit: http://127.0.0.1:5000/category/dsm5/Depressive%20Disorders
```

### 4. Quick Reference During Documentation

```bash
# Search for disorder
python3 search_cli.py search "PTSD"

# Get full details
python3 search_cli.py lookup 309.81
```

### 5. Research and Education

Use the web interface to:
1. Browse all disorders by category
2. Compare diagnostic criteria between systems
3. View prevalence and differential diagnosis information
4. Understand cross-system mappings

---

## Tips and Best Practices

1. **Use Quotes for Multi-Word Searches**
   ```bash
   python3 search_cli.py search "social anxiety"
   ```

2. **Search by Partial Terms**
   - Searching "depress" will find "depression", "depressive", etc.
   - The full-text search is flexible

3. **Use the Web Interface for Detailed Review**
   - CLI is great for quick lookups
   - Web interface is better for exploring and learning

4. **API for Integration**
   - Use API endpoints to integrate with other applications
   - Perfect for building custom tools or workflows

5. **Verbose Mode for More Information**
   ```bash
   python3 search_cli.py search "anxiety" -v
   python3 search_cli.py category "Mood disorders" --system icd11 -v
   ```

---

## Troubleshooting

### Database Not Found Error

If you see: `Error: Database not found`

**Solution:**
```bash
python3 init_database.py
```

### Python Command Not Found

If `python` doesn't work, use `python3`:
```bash
python3 search_cli.py search "depression"
```

### Web Server Won't Start

Make sure Flask is installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use

If port 5000 is busy, edit `web_app.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

---

## Additional Resources

- See `README.md` for full documentation
- Database schema details in `init_database.py`
- API implementation in `web_app.py`
- Core functions in `database_operations.py`
