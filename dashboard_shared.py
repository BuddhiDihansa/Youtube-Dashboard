import pandas as pd

DATA_PATH = "global_youtube_creator_data_large.csv"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    # Load with explicit columns/dtypes to reduce parse time and memory on large CSV files.
    df = pd.read_csv(
        path,
        usecols=[
            "timestamp",
            "video_id",
            "category",
            "language",
            "region",
            "duration_sec",
            "views",
            "likes",
            "comments",
            "shares",
            "sentiment_score",
            "ads_enabled",
        ],
        dtype={
            "video_id": "string",
            "category": "category",
            "language": "category",
            "region": "category",
            "duration_sec": "int32",
            "views": "int64",
            "likes": "int64",
            "comments": "int32",
            "shares": "int32",
            "sentiment_score": "float32",
            "ads_enabled": "string",
        },
        parse_dates=["timestamp"],
    )

    df["views"] = df["views"].clip(lower=1)
    df["engagement"] = (df["likes"] + df["comments"] + df["shares"]) / df["views"]

    df["month"] = df["timestamp"].dt.month.astype("Int8")
    df["hour"] = df["timestamp"].dt.hour.astype("Int8")

    return df


def apply_filters(df, category=None, region=None, language=None):
    filtered = df

    if category:
        filtered = filtered[filtered["category"].isin(category)]
    if region:
        filtered = filtered[filtered["region"].isin(region)]
    if language:
        filtered = filtered[filtered["language"].isin(language)]

    return filtered