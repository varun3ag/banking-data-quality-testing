import pandas as pd
import numpy as np
from datetime import datetime

def run_validation_tests():
    """Run 15 data quality tests on banking data"""
    
    # Load the extracted data
    df = pd.read_csv('data/banking_customers.csv')
    
    print("="*70)
    print("PHASE 2: DATA VALIDATION")
    print("="*70)
    print(f"\nTesting {len(df)} records with 15 quality tests...\n")
    
    results = {}
    
    # TEST 1: Missing Values Check
    print("TEST 1: Missing Values Check")
    missing = df.isnull().sum().sum()
    if missing == 0:
        print("PASS - No missing values found\n")
        results['Test 1'] = 'PASS'
    else:
        print(f"FAIL - Found {missing} missing values\n")
        results['Test 1'] = 'FAIL'
    
    # TEST 2: Duplicate Records
    print("TEST 2: Duplicate Records")
    duplicates = df.duplicated(subset=['CustomerId']).sum()
    if duplicates == 0:
        print("PASS - No duplicate customer IDs\n")
        results['Test 2'] = 'PASS'
    else:
        print(f"FAIL - Found {duplicates} duplicate records\n")
        results['Test 2'] = 'FAIL'
    
    # TEST 3: Format Validation
    print("TEST 3: Format Validation")
    try:
        df['JoinDate'] = pd.to_datetime(df['JoinDate'])
        df['ChurnDate'] = pd.to_datetime(df['ChurnDate'])
        print("PASS - Date formats are valid\n")
        results['Test 3'] = 'PASS'
    except:
        print("FAIL - Invalid date format\n")
        results['Test 3'] = 'FAIL'
    
    # TEST 4: Data Consistency
    print("TEST 4: Data Consistency")
    consistency_issues = 0
    for idx, row in df.iterrows():
        if row['Exited'] == 1 and pd.isna(row['ChurnDate']):
            consistency_issues += 1
    if consistency_issues == 0:
        print("PASS - Churned customers have ChurnDate\n")
        results['Test 4'] = 'PASS'
    else:
        print(f"FAIL - {consistency_issues} churned customers missing ChurnDate\n")
        results['Test 4'] = 'FAIL'
    
    # TEST 5: Plausibility Checks
    print("TEST 5: Plausibility Checks")
    implausible = 0
    if (df['Balance'] < 0).any():
        implausible += (df['Balance'] < 0).sum()
    if (df['Tenure'] < 0).any():
        implausible += (df['Tenure'] < 0).sum()
    if implausible == 0:
        print("PASS - All values are plausible\n")
        results['Test 5'] = 'PASS'
    else:
        print(f"FAIL - Found {implausible} implausible values\n")
        results['Test 5'] = 'FAIL'
    
    # TEST 6: Bias Checks
    print("TEST 6: Bias Checks (Gender Distribution)")
    gender_dist = df['Gender'].value_counts()
    min_pct = (gender_dist.min() / len(df)) * 100
    if min_pct > 30:
        print(f"PASS - Balanced gender distribution: {dict(gender_dist)}\n")
        results['Test 6'] = 'PASS'
    else:
        print(f"WARNING - Imbalanced gender: {dict(gender_dist)}\n")
        results['Test 6'] = 'WARNING'
    
    # TEST 7: Business Correlation
    print("TEST 7: Business Correlation (Churn vs Tenure)")
    correlation = df['Tenure'].corr(df['Exited'])
    if abs(correlation) > 0.1:
        print(f"PASS - Correlation found: {correlation:.3f}\n")
        results['Test 7'] = 'PASS'
    else:
        print(f"WARNING - Weak correlation: {correlation:.3f}\n")
        results['Test 7'] = 'WARNING'
    
    # TEST 8: Seasonality Checks
    print("TEST 8: Seasonality Checks")
    df['JoinMonth'] = df['JoinDate'].dt.month
    month_dist = df['JoinMonth'].value_counts()
    if len(month_dist) == 12:
        print("PASS - Customers spread across all months\n")
        results['Test 8'] = 'PASS'
    else:
        print(f"WARNING - Missing data for {12 - len(month_dist)} months\n")
        results['Test 8'] = 'WARNING'
    
    # TEST 9: Sudden Shift Detection
    print("TEST 9: Sudden Shift Detection")
    df_sorted = df.sort_values('JoinDate')
    df_sorted['Balance_change'] = df_sorted['Balance'].pct_change()
    sudden_shifts = (abs(df_sorted['Balance_change']) > 2).sum()
    if sudden_shifts < len(df) * 0.01:
        print(f"PASS - No suspicious shifts (found {sudden_shifts})\n")
        results['Test 9'] = 'PASS'
    else:
        print(f"WARNING - Found {sudden_shifts} suspicious shifts\n")
        results['Test 9'] = 'WARNING'
    
    # TEST 10: Segment Completeness
    print("TEST 10: Segment Completeness")
    segments = df['Geography'].unique()
    segment_completeness = {}
    all_complete = True
    for segment in segments:
        segment_data = df[df['Geography'] == segment]
        if len(segment_data) < 100:
            all_complete = False
        segment_completeness[segment] = len(segment_data)
    if all_complete:
        print(f"PASS - All segments have complete data: {segment_completeness}\n")
        results['Test 10'] = 'PASS'
    else:
        print(f"WARNING - Some segments incomplete: {segment_completeness}\n")
        results['Test 10'] = 'WARNING'
    
    # TEST 11: Age Range Validation
    print("TEST 11: Age Range Validation")
    invalid_ages = ((df['Age'] < 18) | (df['Age'] > 120)).sum()
    if invalid_ages == 0:
        print(f"PASS - All ages in valid range (18-120)\n")
        results['Test 11'] = 'PASS'
    else:
        print(f"FAIL - Found {invalid_ages} invalid ages\n")
        results['Test 11'] = 'FAIL'
    
    # TEST 12: Balance Plausibility
    print("TEST 12: Balance Plausibility")
    invalid_balance = (df['Balance'] < 0).sum()
    if invalid_balance == 0:
        print(f"PASS - All balances are non-negative\n")
        results['Test 12'] = 'PASS'
    else:
        print(f"FAIL - Found {invalid_balance} negative balances\n")
        results['Test 12'] = 'FAIL'
    
    # TEST 13: Tenure Validity
    print("TEST 13: Tenure Validity")
    invalid_tenure = ((df['Tenure'] < 0) | (df['Tenure'] > 100)).sum()
    if invalid_tenure == 0:
        print(f"PASS - All tenure values are valid (0-100 years)\n")
        results['Test 13'] = 'PASS'
    else:
        print(f"FAIL - Found {invalid_tenure} invalid tenure values\n")
        results['Test 13'] = 'FAIL'
    
    # TEST 14: Product Count Validity
    print("TEST 14: Product Count Validity")
    invalid_products = ((df['NumOfProducts'] < 1) | (df['NumOfProducts'] > 4)).sum()
    if invalid_products == 0:
        print(f"PASS - All product counts valid (1-4)\n")
        results['Test 14'] = 'PASS'
    else:
        print(f"FAIL - Found {invalid_products} invalid product counts\n")
        results['Test 14'] = 'FAIL'
    
    # TEST 15: Credit Score Range
    print("TEST 15: Credit Score Range Validation")
    invalid_scores = ((df['CreditScore'] < 300) | (df['CreditScore'] > 850)).sum()
    if invalid_scores == 0:
        print(f"PASS - All credit scores in valid range (300-850)\n")
        results['Test 15'] = 'PASS'
    else:
        print(f"FAIL - Found {invalid_scores} invalid credit scores\n")
        results['Test 15'] = 'FAIL'
    
    # SUMMARY
    print("="*70)
    print("SUMMARY")
    print("="*70)
    passed = sum(1 for v in results.values() if v == 'PASS')
    failed = sum(1 for v in results.values() if v == 'FAIL')
    warnings = sum(1 for v in results.values() if v == 'WARNING')
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")
    print(f"WARNING: {warnings}")
    print(f"Data Quality Score: {(passed/len(results))*100:.1f}%")
    print("\n" + "="*70)

if __name__ == "__main__":
    run_validation_tests()