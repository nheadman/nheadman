# Quick Start Guide

Get up and running with the Diagnostic Classification Database in 3 simple steps!

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask (for the web interface). That's it!

### Step 2: Initialize the Database

```bash
python3 init_database.py
```

This creates the SQLite database and populates it with:
- 13 DSM-5-TR disorders
- 23 ICD-11 disorders  
- 16 cross-references between systems

**Expected output:**
```
Initializing Diagnostic Classification Database...
============================================================
✓ Database schema created at /workspace/diagnostic_database.db
✓ Database populated with 13 DSM-5-TR disorders, 23 ICD-11 disorders, and 16 cross-references
============================================================
✓ Database initialization complete!
```

### Step 3: Test the Installation (Optional but Recommended)

```bash
python3 test_installation.py
```

This verifies everything is working correctly.

## Usage

Now choose your preferred interface:

### Option A: Web Interface (Recommended for Beginners)

```bash
python3 web_app.py
```

Then open your browser to: **http://127.0.0.1:5000**

Features:
- 🔍 Search across both classification systems
- 📋 View detailed diagnostic criteria
- 🔗 See cross-references between DSM-5-TR and ICD-11
- 📚 Browse by category
- 💻 Beautiful, modern UI

**To stop the server:** Press `Ctrl+C`

### Option B: Command-Line Interface (Fast for Quick Lookups)

```bash
# Search for disorders
python3 search_cli.py search "depression"

# Look up a specific code
python3 search_cli.py lookup 296.21

# Show help
python3 search_cli.py --help
```

## Quick Examples

### Example 1: Find Depression Disorders
```bash
python3 search_cli.py search "depression" --system both
```

### Example 2: Look Up a Code
```bash
# DSM-5-TR code
python3 search_cli.py lookup 296.21

# ICD-11 code
python3 search_cli.py lookup 6A70
```

### Example 3: Browse a Category
```bash
# List all categories
python3 search_cli.py category --list --system dsm5

# View disorders in a category
python3 search_cli.py category "Anxiety Disorders" --system dsm5
```

### Example 4: View Cross-References
```bash
python3 search_cli.py crossref --list-all
```

### Example 5: Database Statistics
```bash
python3 search_cli.py stats
```

## What's Included?

The database includes sample data from both DSM-5-TR and ICD-11:

**DSM-5-TR Categories:**
- Depressive Disorders (e.g., Major Depressive Disorder, Persistent Depressive Disorder)
- Anxiety Disorders (e.g., Panic Disorder, GAD, Social Anxiety Disorder)
- Trauma and Stressor-Related Disorders (e.g., PTSD, Adjustment Disorder)
- Obsessive-Compulsive Disorders (e.g., OCD)
- Neurodevelopmental Disorders (e.g., ADHD)
- Bipolar and Related Disorders (e.g., Bipolar I, Bipolar II)
- Schizophrenia Spectrum (e.g., Schizophrenia)

**ICD-11 Categories:**
- Mood disorders
- Anxiety and fear-related disorders
- Disorders specifically associated with stress
- Obsessive-compulsive or related disorders
- Neurodevelopmental disorders
- Schizophrenia or other primary psychotic disorders
- And more...

## Need Help?

### Get More Information
- Full documentation: `README.md`
- Usage examples: `EXAMPLES.md`
- Command help: `python3 search_cli.py --help`

### Common Issues

**Problem:** `python: command not found`  
**Solution:** Use `python3` instead of `python`

**Problem:** Database not found error  
**Solution:** Run `python3 init_database.py` first

**Problem:** Flask not found  
**Solution:** Run `pip install -r requirements.txt`

**Problem:** Port 5000 already in use (web app)  
**Solution:** Edit `web_app.py` and change the port number in the last line

## Next Steps

1. **Explore the Web Interface**: Try searching for different disorders, browse categories, and view cross-references

2. **Learn the CLI**: Run `python3 search_cli.py --help` to see all available commands

3. **Check Out Examples**: Read `EXAMPLES.md` for comprehensive usage examples

4. **Integrate with Your Code**: Import `database_operations.py` in your Python scripts

5. **Extend the Database**: Edit `init_database.py` to add more disorders

## Features at a Glance

✅ **Full-text search** across disorder names, descriptions, and criteria  
✅ **Cross-reference lookups** between DSM-5-TR and ICD-11  
✅ **Complete diagnostic criteria** for each disorder  
✅ **Category browsing** to explore related disorders  
✅ **Multiple interfaces**: Web, CLI, and Python API  
✅ **Offline capability**: All data stored locally in SQLite  
✅ **Fast and lightweight**: No external services required  

## Important Note

⚠️ **This database is for educational and reference purposes only.**  
It is NOT intended for clinical diagnosis. Always consult official DSM-5-TR and ICD-11 resources for clinical practice.

---

**Enjoy using the Diagnostic Classification Database!** 🧠

For more detailed information, see:
- `README.md` - Complete documentation
- `EXAMPLES.md` - Comprehensive usage examples
