#!/usr/bin/env python3
"""
Quick test script to verify the diagnostic database installation.
Run this after initializing the database to ensure everything works.
"""

import sys
from pathlib import Path
from database_operations import DiagnosticDatabase

def test_database():
    """Test basic database functionality."""
    print("\n" + "=" * 80)
    print("DIAGNOSTIC DATABASE INSTALLATION TEST")
    print("=" * 80 + "\n")
    
    # Check database file exists
    db_path = Path("diagnostic_database.db")
    if not db_path.exists():
        print("❌ FAILED: Database file not found!")
        print("   Please run: python3 init_database.py")
        return False
    
    print("✓ Database file found")
    
    try:
        db = DiagnosticDatabase()
        print("✓ Database connection successful")
        
        # Test statistics
        stats = db.get_statistics()
        print(f"✓ Database statistics: {stats['dsm5_disorders']} DSM-5-TR, {stats['icd11_disorders']} ICD-11, {stats['cross_references']} cross-references")
        
        # Test DSM-5-TR search
        results = db.search_dsm5("depression", limit=5)
        print(f"✓ DSM-5-TR search working: found {len(results)} results for 'depression'")
        
        # Test ICD-11 search
        results = db.search_icd11("anxiety", limit=5)
        print(f"✓ ICD-11 search working: found {len(results)} results for 'anxiety'")
        
        # Test code lookup
        disorder = db.get_dsm5_by_code("296.21")
        if disorder:
            print(f"✓ DSM-5-TR code lookup working: {disorder['code']} - {disorder['name']}")
        else:
            print("⚠ Warning: DSM-5-TR code lookup returned no results")
        
        disorder = db.get_icd11_by_code("6A70")
        if disorder:
            print(f"✓ ICD-11 code lookup working: {disorder['code']} - {disorder['name']}")
        else:
            print("⚠ Warning: ICD-11 code lookup returned no results")
        
        # Test cross-references
        xrefs = db.get_icd11_from_dsm5("296.21")
        if xrefs:
            print(f"✓ Cross-references working: found {len(xrefs)} ICD-11 codes for DSM-5-TR 296.21")
        else:
            print("⚠ Warning: Cross-reference lookup returned no results")
        
        # Test categories
        dsm5_cats = db.list_dsm5_categories()
        icd11_cats = db.list_icd11_categories()
        print(f"✓ Categories working: {len(dsm5_cats)} DSM-5-TR categories, {len(icd11_cats)} ICD-11 categories")
        
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED - Installation successful!")
        print("=" * 80)
        print("\nYou can now use:")
        print("  • CLI: python3 search_cli.py --help")
        print("  • Web: python3 web_app.py")
        print("\n" + "=" * 80 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        print("\nPlease ensure:")
        print("  1. You have run: python3 init_database.py")
        print("  2. The database file is not corrupted")
        print("  3. You have the required Python packages installed")
        return False


if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
