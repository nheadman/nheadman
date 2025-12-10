# DSM-5-TR / ICD-11 Searchable Crosswalk (sample)

This repository provides a small, educational example of how to organize a searchable crosswalk between DSM-5-TR and ICD-11. The included data are concise, original summaries and a handful of sample codes; consult the official manuals for complete diagnostic criteria and the full set of conditions.

## How to use

1. Ensure you have Python 3.9+ installed.
2. Run a search by name or code:

```bash
python search.py "depressive"
python search.py "6B00"
```

The script returns matching DSM-5-TR and ICD-11 entries with brief summaries and notes.

## Data format

The JSON file at `data/conditions.json` holds a list of records:

```json
{
  "dsm5_name": "Major Depressive Disorder",
  "dsm5_code": "296.2",
  "icd11_name": "Depressive episode",
  "icd11_code": "6A70",
  "summary": "Persistent depressed mood with related cognitive and physical symptoms that cause impairment.",
  "notes": "ICD-11 groups mild, moderate, and severe episodes under 6A70; DSM-5-TR details symptom duration and severity specifiers."
}
```

Add more conditions by extending the array while keeping descriptions concise and original.
