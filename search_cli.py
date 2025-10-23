#!/usr/bin/env python3
"""
Command-line interface for searching the diagnostic classification database.
"""

import argparse
import sys
from pathlib import Path
from database_operations import DiagnosticDatabase, format_disorder_display


def search_command(args):
    """Handle search command."""
    db = DiagnosticDatabase()
    
    if args.system == 'both':
        results = db.search_all(args.query, limit=args.limit)
        
        print(f"\n{'=' * 80}")
        print(f"SEARCH RESULTS FOR: '{args.query}'")
        print(f"{'=' * 80}\n")
        
        # Display DSM-5-TR results
        print(f"\n{'─' * 80}")
        print(f"DSM-5-TR RESULTS ({len(results['dsm5'])} found)")
        print(f"{'─' * 80}")
        if results['dsm5']:
            for disorder in results['dsm5']:
                print(f"\n  [{disorder['code']}] {disorder['name']}")
                print(f"  Category: {disorder['category']}")
                if args.verbose:
                    print(f"  Description: {disorder['description'][:150]}...")
        else:
            print("  No results found.")
        
        # Display ICD-11 results
        print(f"\n{'─' * 80}")
        print(f"ICD-11 RESULTS ({len(results['icd11'])} found)")
        print(f"{'─' * 80}")
        if results['icd11']:
            for disorder in results['icd11']:
                print(f"\n  [{disorder['code']}] {disorder['name']}")
                print(f"  Category: {disorder['category']}")
                if args.verbose:
                    print(f"  Description: {disorder['description'][:150]}...")
        else:
            print("  No results found.")
            
    elif args.system == 'dsm5':
        results = db.search_dsm5(args.query, limit=args.limit)
        print(f"\n{'=' * 80}")
        print(f"DSM-5-TR SEARCH RESULTS FOR: '{args.query}'")
        print(f"{'=' * 80}")
        if results:
            for disorder in results:
                print(f"\n  [{disorder['code']}] {disorder['name']}")
                print(f"  Category: {disorder['category']}")
                if args.verbose:
                    print(f"  Description: {disorder['description'][:150]}...")
        else:
            print("\nNo results found.")
            
    else:  # icd11
        results = db.search_icd11(args.query, limit=args.limit)
        print(f"\n{'=' * 80}")
        print(f"ICD-11 SEARCH RESULTS FOR: '{args.query}'")
        print(f"{'=' * 80}")
        if results:
            for disorder in results:
                print(f"\n  [{disorder['code']}] {disorder['name']}")
                print(f"  Category: {disorder['category']}")
                if args.verbose:
                    print(f"  Description: {disorder['description'][:150]}...")
        else:
            print("\nNo results found.")
    
    print(f"\n{'=' * 80}\n")


def lookup_command(args):
    """Handle lookup by code command."""
    db = DiagnosticDatabase()
    
    # Determine which system based on code format
    if args.code.replace('.', '').isdigit():
        # DSM-5-TR codes are numeric
        disorder = db.get_dsm5_by_code(args.code)
        if disorder:
            print(format_disorder_display(disorder, "DSM-5-TR"))
            
            # Show cross-references
            xrefs = db.get_icd11_from_dsm5(args.code)
            if xrefs:
                print(f"\n{'─' * 80}")
                print("CORRESPONDING ICD-11 CODES:")
                print(f"{'─' * 80}")
                for xref in xrefs:
                    print(f"\n  [{xref['icd11_code']}] {xref['icd11_name']}")
                    print(f"  Relationship: {xref['relationship_type']}")
                    if xref['notes']:
                        print(f"  Notes: {xref['notes']}")
                print(f"\n{'─' * 80}\n")
        else:
            print(f"\nDSM-5-TR disorder with code '{args.code}' not found.\n")
    else:
        # ICD-11 codes are alphanumeric
        disorder = db.get_icd11_by_code(args.code)
        if disorder:
            print(format_disorder_display(disorder, "ICD-11"))
            
            # Show cross-references
            xrefs = db.get_dsm5_from_icd11(args.code)
            if xrefs:
                print(f"\n{'─' * 80}")
                print("CORRESPONDING DSM-5-TR CODES:")
                print(f"{'─' * 80}")
                for xref in xrefs:
                    print(f"\n  [{xref['dsm5_code']}] {xref['dsm5_name']}")
                    print(f"  Relationship: {xref['relationship_type']}")
                    if xref['notes']:
                        print(f"  Notes: {xref['notes']}")
                print(f"\n{'─' * 80}\n")
        else:
            print(f"\nICD-11 disorder with code '{args.code}' not found.\n")


def category_command(args):
    """Handle browse by category command."""
    db = DiagnosticDatabase()
    
    if args.system == 'dsm5':
        if args.list:
            categories = db.list_dsm5_categories()
            print(f"\n{'=' * 80}")
            print("DSM-5-TR CATEGORIES")
            print(f"{'=' * 80}")
            for cat in categories:
                print(f"  • {cat}")
            print(f"\n{'=' * 80}\n")
        else:
            disorders = db.get_dsm5_by_category(args.category)
            print(f"\n{'=' * 80}")
            print(f"DSM-5-TR DISORDERS IN CATEGORY: {args.category}")
            print(f"{'=' * 80}")
            if disorders:
                for disorder in disorders:
                    print(f"\n  [{disorder['code']}] {disorder['name']}")
                    if args.verbose:
                        print(f"  Description: {disorder['description'][:150]}...")
            else:
                print("\nNo disorders found in this category.")
            print(f"\n{'=' * 80}\n")
    else:  # icd11
        if args.list:
            categories = db.list_icd11_categories()
            print(f"\n{'=' * 80}")
            print("ICD-11 CATEGORIES")
            print(f"{'=' * 80}")
            for cat in categories:
                print(f"  • {cat}")
            print(f"\n{'=' * 80}\n")
        else:
            disorders = db.get_icd11_by_category(args.category)
            print(f"\n{'=' * 80}")
            print(f"ICD-11 DISORDERS IN CATEGORY: {args.category}")
            print(f"{'=' * 80}")
            if disorders:
                for disorder in disorders:
                    print(f"\n  [{disorder['code']}] {disorder['name']}")
                    if args.verbose:
                        print(f"  Description: {disorder['description'][:150]}...")
            else:
                print("\nNo disorders found in this category.")
            print(f"\n{'=' * 80}\n")


def crossref_command(args):
    """Handle cross-reference command."""
    db = DiagnosticDatabase()
    
    if args.list_all:
        xrefs = db.get_all_cross_references()
        print(f"\n{'=' * 80}")
        print(f"ALL CROSS-REFERENCES ({len(xrefs)} total)")
        print(f"{'=' * 80}")
        for xref in xrefs:
            print(f"\nDSM-5-TR: [{xref['dsm5_code']}] {xref['dsm5_name']}")
            print(f"  ↔ ({xref['relationship_type']})")
            print(f"ICD-11:   [{xref['icd11_code']}] {xref['icd11_name']}")
            if xref['notes']:
                print(f"Notes: {xref['notes']}")
            print(f"{'-' * 80}")
        print(f"\n{'=' * 80}\n")
    else:
        print("\nUse --list-all to see all cross-references, or use 'lookup <code>' to see cross-references for a specific code.\n")


def stats_command(args):
    """Handle statistics command."""
    db = DiagnosticDatabase()
    stats = db.get_statistics()
    
    print(f"\n{'=' * 80}")
    print("DATABASE STATISTICS")
    print(f"{'=' * 80}")
    print(f"\nDSM-5-TR Disorders:       {stats['dsm5_disorders']}")
    print(f"DSM-5-TR Categories:      {stats['dsm5_categories']}")
    print(f"\nICD-11 Disorders:         {stats['icd11_disorders']}")
    print(f"ICD-11 Categories:        {stats['icd11_categories']}")
    print(f"\nCross-References:         {stats['cross_references']}")
    print(f"\n{'=' * 80}\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Search and browse the diagnostic classification database (DSM-5-TR & ICD-11)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search across both systems
  %(prog)s search "depression" --system both
  
  # Search only DSM-5-TR
  %(prog)s search "anxiety" --system dsm5
  
  # Look up a specific code
  %(prog)s lookup 296.21
  %(prog)s lookup 6A70
  
  # Browse categories
  %(prog)s category --list --system dsm5
  %(prog)s category "Depressive Disorders" --system dsm5
  
  # View cross-references
  %(prog)s crossref --list-all
  
  # Show database statistics
  %(prog)s stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for disorders by term')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--system', choices=['both', 'dsm5', 'icd11'], 
                               default='both', help='Which system to search (default: both)')
    search_parser.add_argument('--limit', type=int, default=20, 
                               help='Maximum number of results (default: 20)')
    search_parser.add_argument('-v', '--verbose', action='store_true',
                               help='Show more details in results')
    search_parser.set_defaults(func=search_command)
    
    # Lookup command
    lookup_parser = subparsers.add_parser('lookup', help='Look up disorder by code')
    lookup_parser.add_argument('code', help='Diagnostic code (DSM-5-TR or ICD-11)')
    lookup_parser.set_defaults(func=lookup_command)
    
    # Category command
    category_parser = subparsers.add_parser('category', help='Browse disorders by category')
    category_parser.add_argument('category', nargs='?', help='Category name to browse')
    category_parser.add_argument('--system', choices=['dsm5', 'icd11'], 
                                 default='dsm5', help='Which system (default: dsm5)')
    category_parser.add_argument('--list', action='store_true',
                                 help='List all available categories')
    category_parser.add_argument('-v', '--verbose', action='store_true',
                                 help='Show more details in results')
    category_parser.set_defaults(func=category_command)
    
    # Cross-reference command
    crossref_parser = subparsers.add_parser('crossref', help='View cross-references between systems')
    crossref_parser.add_argument('--list-all', action='store_true',
                                 help='List all cross-references')
    crossref_parser.set_defaults(func=crossref_command)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.set_defaults(func=stats_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        args.func(args)
        return 0
    except FileNotFoundError as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("Please run 'python init_database.py' first to create the database.\n", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
