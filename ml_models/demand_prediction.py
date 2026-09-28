import pandas as pd
from sklearn.linear_model import LinearRegression
from database.sales_db import get_sales_data_for_ml

def prepare_product_demand(company_id, product_id):
   
    df = get_sales_data_for_ml(company_id)

    if df is None or df.empty:
        return None
    
    df = df[df["product_id"] == product_id].copy()

    if len(df) < 5:
        return None

    df["sale_date"] = pd.to_datetime(df["sale_date"])

    df["day"] = df["sale_date"].dt.day
    df["month"] = df["sale_date"].dt.month
    df["year"] = df["sale_date"].dt.year
    df["day_of_week"] = df["sale_date"].dt.dayofweek
    df["day_of_year"] = df["sale_date"].dt.dayofyear

    return df

def predict_demand(company_id, product_id, day, month, year):
    
    df = prepare_product_demand(company_id, product_id)

    if df is None:
        return None

    features = ["day", "month", "year", "day_of_week", "day_of_year"]

    X = df[features]
    y = df["quantity"]

    model = LinearRegression()
    model.fit(X, y)

    prediction_date = pd.Timestamp(year=year, month=month, day=day)

    input_data = pd.DataFrame([{
        "day": day,
        "month": month,
        "year": year,
        "day_of_week": prediction_date.dayofweek,
        "day_of_year": prediction_date.dayofyear
    }])

    prediction = model.predict(input_data)[0]
    prediction = max(0, prediction)

    return round(prediction)