import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_banking_data(num_records=10000):
    """Generate synthetic banking customer data"""
    
    np.random.seed(42)
    
    # Generate random join dates (last 5 years)
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2024, 1, 1)
    date_range = (end_date - start_date).days
    join_dates = [start_date + timedelta(days=np.random.randint(0, date_range)) 
                  for _ in range(num_records)]
    
    # Generate churn status
    exited = np.random.choice([0, 1], num_records, p=[0.8, 0.2])
    
    # Generate churn dates (only for exited customers)
    churn_dates = []
    for i, is_exited in enumerate(exited):
        if is_exited == 1:
            days_after_join = np.random.randint(30, 1800)
            churn_date = join_dates[i] + timedelta(days=days_after_join)
            churn_dates.append(churn_date)
        else:
            churn_dates.append(None)
    
    data = {
        'RowNumber': range(1, num_records + 1),
        'CustomerId': range(15634602, 15634602 + num_records),
        'Surname': np.random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Peterson', 'Phillips', 'Campbell', 'Parker', 'Evans', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez'], num_records),
        'CreditScore': np.random.randint(300, 850, num_records),
        'Geography': np.random.choice(['France', 'Spain', 'Germany', 'UK', 'USA', 'Canada', 'Australia', 'India', 'Japan', 'Brazil', 'Mexico', 'Italy'], num_records),
        'Gender': np.random.choice(['Male', 'Female'], num_records),
        'Age': np.random.randint(18, 100, num_records),
        'Tenure': np.random.randint(0, 50, num_records),
        'Balance': np.random.uniform(0, 250000, num_records),
        'NumOfProducts': np.random.randint(1, 5, num_records),
        'HasCrCard': np.random.choice([0, 1], num_records),
        'IsActiveMember': np.random.choice([0, 1], num_records),
        'EstimatedSalary': np.random.uniform(20000, 200000, num_records),
        'JoinDate': join_dates,
        'Exited': exited,
        'ChurnDate': churn_dates
    }
    
    df = pd.DataFrame(data)
    return df

def main():
    print("="*70)
    print("PHASE 1: DATA EXTRACTION")
    print("="*70)
    
    print("\nGenerating synthetic banking customer data...")
    df = generate_banking_data(10000)
    
    # Create data folder if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/banking_customers.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nData extracted successfully!")
    print(f"Records: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"File: {output_path}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    return df

if __name__ == "__main__":
    df = main()
