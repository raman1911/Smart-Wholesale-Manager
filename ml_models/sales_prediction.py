import pandas as pd
from sklearn.linear_model import LinearRegression
from database.sales_db import get_sales_data_for_ml
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

def prepare_product_sales(company_id, product_id):

    df = get_sales_data_for_ml(company_id)
    if df is None or df.empty:
        return None

    df = df[df["product_id"] == product_id].copy()
    if len(df) < 5:
        return None

    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    df = df.dropna(subset=["sale_date"])
    if len(df) < 5:
        return None

    df["day"] = df["sale_date"].dt.day
    df["month"] = df["sale_date"].dt.month
    df["year"] = df["sale_date"].dt.year
    df["day_of_week"] = df["sale_date"].dt.dayofweek
    df["day_of_year"] = df["sale_date"].dt.dayofyear

    return df

def train_sales_model(company_id, product_id):

    df = prepare_product_sales(company_id, product_id)

    if df is None:
        return None

    X = df[["day", "month", "year", "day_of_week", "day_of_year"]]
    y = df["total_amount"]

    model = LinearRegression()
    model.fit(X, y)

    return model

def predict_sales(company_id, product_id, day, month, year, selling_price):

    df = prepare_product_sales(company_id, product_id)

    if df is None or len(df) < 5:
        return None

    features = ["day", "month", "year", "day_of_week", "day_of_year"]

    X = df[features]
    y = df["total_amount"]

    model = LinearRegression()
    model.fit(X, y)

    prediction_date = pd.Timestamp(year, month, day)

    input_data = pd.DataFrame([{
        "day": prediction_date.day,
        "month": prediction_date.month,
        "year": prediction_date.year,
        "day_of_week": prediction_date.dayofweek,
        "day_of_year": prediction_date.dayofyear
    }])

    prediction = model.predict(input_data)[0]
    prediction = max(0, prediction)

    return round(prediction, 2)

def evaluate_sales_model(company_id, product_id):
    df = prepare_product_sales(company_id, product_id)

    if df is None or len(df) < 5:
        return None

    features = ["day", "month", "year", "day_of_week", "day_of_year"]
    X = df[features]
    y = df["total_amount"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    error = mean_absolute_error(y_test, predictions)

    return round(error, 2)