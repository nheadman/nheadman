"""
Database operations module for the diagnostic classification database.
Provides search and query functionality for DSM-5-TR and ICD-11.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

DATABASE_PATH = Path(__file__).parent / "diagnostic_database.db"


@dataclass
class DSM5Disorder:
    """Data class for DSM-5-TR disorder."""
    id: int
    code: str
    name: str
    category: str
    description: str
    diagnostic_criteria: str
    specifiers: str
    prevalence: str
    differential_diagnosis: str


@dataclass
class ICD11Disorder:
    """Data class for ICD-11 disorder."""
    id: int
    code: str
    name: str
    category: str
    description: str
    diagnostic_requirements: str
    exclusions: str
    coding_notes: str


@dataclass
class CrossReference:
    """Data class for cross-reference between DSM-5-TR and ICD-11."""
    dsm5_code: str
    dsm5_name: str
    icd11_code: str
    icd11_name: str
    relationship_type: str
    notes: str


class DiagnosticDatabase:
    """Main database interface for diagnostic classifications."""
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"Database not found at {db_path}. "
                "Please run init_database.py first."
            )
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ========== DSM-5-TR Queries ==========
    
    def search_dsm5(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Full-text search in DSM-5-TR disorders.
        
        Args:
            query: Search term
            limit: Maximum number of results
            
        Returns:
            List of matching disorders
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Use FTS5 for full-text search
        cursor.execute("""
            SELECT d.*, rank
            FROM dsm5_disorders d
            JOIN dsm5_search s ON d.id = s.rowid
            WHERE dsm5_search MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_dsm5_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Get DSM-5-TR disorder by code.
        
        Args:
            code: DSM-5-TR diagnostic code
            
        Returns:
            Disorder information or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dsm5_disorders WHERE code = ?
        """, (code,))
        
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_dsm5_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all DSM-5-TR disorders in a category.
        
        Args:
            category: Category name
            
        Returns:
            List of disorders in the category
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dsm5_disorders 
            WHERE category LIKE ?
            ORDER BY code
        """, (f"%{category}%",))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def list_dsm5_categories(self) -> List[str]:
        """
        Get all unique DSM-5-TR categories.
        
        Returns:
            List of category names
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT category FROM dsm5_disorders ORDER BY category
        """)
        
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
    
    # ========== ICD-11 Queries ==========
    
    def search_icd11(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Full-text search in ICD-11 disorders.
        
        Args:
            query: Search term
            limit: Maximum number of results
            
        Returns:
            List of matching disorders
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT d.*, rank
            FROM icd11_disorders d
            JOIN icd11_search s ON d.id = s.rowid
            WHERE icd11_search MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_icd11_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """
        Get ICD-11 disorder by code.
        
        Args:
            code: ICD-11 diagnostic code
            
        Returns:
            Disorder information or None if not found
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM icd11_disorders WHERE code = ?
        """, (code,))
        
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def get_icd11_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all ICD-11 disorders in a category.
        
        Args:
            category: Category name
            
        Returns:
            List of disorders in the category
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM icd11_disorders 
            WHERE category LIKE ?
            ORDER BY code
        """, (f"%{category}%",))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def list_icd11_categories(self) -> List[str]:
        """
        Get all unique ICD-11 categories.
        
        Returns:
            List of category names
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT category FROM icd11_disorders ORDER BY category
        """)
        
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return results
    
    # ========== Cross-Reference Queries ==========
    
    def get_icd11_from_dsm5(self, dsm5_code: str) -> List[Dict[str, Any]]:
        """
        Get ICD-11 codes that correspond to a DSM-5-TR code.
        
        Args:
            dsm5_code: DSM-5-TR diagnostic code
            
        Returns:
            List of cross-references with ICD-11 information
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                cr.dsm5_code,
                d5.name as dsm5_name,
                cr.icd11_code,
                i11.name as icd11_name,
                cr.relationship_type,
                cr.notes
            FROM cross_references cr
            JOIN dsm5_disorders d5 ON cr.dsm5_code = d5.code
            JOIN icd11_disorders i11 ON cr.icd11_code = i11.code
            WHERE cr.dsm5_code = ?
        """, (dsm5_code,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_dsm5_from_icd11(self, icd11_code: str) -> List[Dict[str, Any]]:
        """
        Get DSM-5-TR codes that correspond to an ICD-11 code.
        
        Args:
            icd11_code: ICD-11 diagnostic code
            
        Returns:
            List of cross-references with DSM-5-TR information
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                cr.dsm5_code,
                d5.name as dsm5_name,
                cr.icd11_code,
                i11.name as icd11_name,
                cr.relationship_type,
                cr.notes
            FROM cross_references cr
            JOIN dsm5_disorders d5 ON cr.dsm5_code = d5.code
            JOIN icd11_disorders i11 ON cr.icd11_code = i11.code
            WHERE cr.icd11_code = ?
        """, (icd11_code,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_all_cross_references(self) -> List[Dict[str, Any]]:
        """
        Get all cross-references between DSM-5-TR and ICD-11.
        
        Returns:
            List of all cross-references
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                cr.dsm5_code,
                d5.name as dsm5_name,
                cr.icd11_code,
                i11.name as icd11_name,
                cr.relationship_type,
                cr.notes
            FROM cross_references cr
            JOIN dsm5_disorders d5 ON cr.dsm5_code = d5.code
            JOIN icd11_disorders i11 ON cr.icd11_code = i11.code
            ORDER BY cr.dsm5_code, cr.icd11_code
        """)
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    # ========== Combined Search ==========
    
    def search_all(self, query: str, limit: int = 50) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search both DSM-5-TR and ICD-11 simultaneously.
        
        Args:
            query: Search term
            limit: Maximum number of results per system
            
        Returns:
            Dictionary with 'dsm5' and 'icd11' keys containing results
        """
        return {
            'dsm5': self.search_dsm5(query, limit),
            'icd11': self.search_icd11(query, limit)
        }
    
    # ========== Statistics ==========
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with counts of disorders and cross-references
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM dsm5_disorders")
        dsm5_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM icd11_disorders")
        icd11_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM cross_references")
        xref_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT category) FROM dsm5_disorders")
        dsm5_categories = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT category) FROM icd11_disorders")
        icd11_categories = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'dsm5_disorders': dsm5_count,
            'icd11_disorders': icd11_count,
            'cross_references': xref_count,
            'dsm5_categories': dsm5_categories,
            'icd11_categories': icd11_categories
        }


def format_disorder_display(disorder: Dict[str, Any], system: str = "DSM-5-TR") -> str:
    """
    Format a disorder for display.
    
    Args:
        disorder: Disorder dictionary
        system: "DSM-5-TR" or "ICD-11"
        
    Returns:
        Formatted string for display
    """
    if system == "DSM-5-TR":
        output = f"""
{'=' * 80}
{system} DISORDER
{'=' * 80}
Code:        {disorder['code']}
Name:        {disorder['name']}
Category:    {disorder['category']}

DESCRIPTION:
{disorder['description']}

DIAGNOSTIC CRITERIA:
{disorder['diagnostic_criteria']}

SPECIFIERS:
{disorder['specifiers']}

PREVALENCE:
{disorder['prevalence']}

DIFFERENTIAL DIAGNOSIS:
{disorder['differential_diagnosis']}
{'=' * 80}
"""
    else:  # ICD-11
        output = f"""
{'=' * 80}
{system} DISORDER
{'=' * 80}
Code:        {disorder['code']}
Name:        {disorder['name']}
Category:    {disorder['category']}

DESCRIPTION:
{disorder['description']}

DIAGNOSTIC REQUIREMENTS:
{disorder['diagnostic_requirements']}

EXCLUSIONS:
{disorder['exclusions']}

CODING NOTES:
{disorder['coding_notes']}
{'=' * 80}
"""
    return output
