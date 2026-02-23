from extract import extract
from transform import transform
from load import load

def run_pipeline():
    df = extract()
    df = transform(df)
    load(df)
    print("ETL Pipeline Completed Successfully!")

if __name__ == "__main__":
    run_pipeline()
