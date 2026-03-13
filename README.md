# Banking Customer Data Quality Testing Pipeline

## Project Overview
 Data quality testing framework for banking customer data using DAMA framework and 15 comprehensive quality tests.

## What This Project Does
- **Phase 1: Extract** - Generates 10,000 synthetic banking customer records
- **Phase 2: Validate** - Runs 15 DAMA-based quality tests (93.3% pass rate)
- **Phase 3: Report** - Generates professional data quality report

## Technologies Used
- Python
- Pandas
- NumPy

## Test Coverage
- Missing values validation
- Duplicate detection
- Format validation
- Data consistency checks
- Plausibility checks
- Bias detection
- Business correlations
- Seasonality analysis
- Anomaly detection
- Segment completeness
- Age range validation
- Balance plausibility
- Tenure validity
- Product count validation
- Credit score range validation

## Results
- Total Tests: 15
- Pass Rate: 93.3%
- Data Quality Score: Approved for business use

## Files
- `1_extract.py` - Generate banking data
- `2_validate.py` - Run 15 quality tests
- `3_report.py` - Generate quality report
- `data/banking_customers.csv` - Generated dataset
- `output/data_quality_report.txt` - Quality report

## How to Run
```bash
python 1_extract.py   # Generate data
python 2_validate.py  # Run tests
python 3_report.py    # Generate report
```

## Key Findings
- Dataset has 93.3% quality compliance
- All critical fields are complete
- Data suitable for churn prediction and customer segmentation
- Recommended for business analysis and modeling

## Author
Varun Ajjampur
```

