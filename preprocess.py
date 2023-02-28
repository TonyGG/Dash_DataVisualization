import pandas as pd
import numpy as np

def run(df):
    #Treating Version Numbers 
    df['Android_Ver'].replace(to_replace=[r"([1-8]).*", 'Varies with device'], value=[r"\1", "4"], inplace=True, regex=True)

    #Treat missing values of Rating column, replacing nulls by means.
    #Ratings had a lot of NaN entities, dropping them all would have cost us loss of information
    nan_rating_category = df.loc[df['Rating'].isna()].Category.value_counts()
    # print(nan_rating_category)
    for index, value in nan_rating_category.items():
        # print(index, value)
        average = df.loc[df['Category'] == index, 'Rating'].mean()
        df.loc[df['Category'] == index, 'Rating'] = df.loc[df['Category'] == index, 'Rating'].fillna(average)

    #Dropping rows having nulls in any column.
    #Considering "Unrated" as NaN for the case of Content Rating
    df.drop(df[df['Content_Rating'] == 'Unrated'].index, inplace=True)
    #Drop rows with any NaN entry
    df.dropna(inplace=True) 

   #Converting columns' data types to appropriate data types.
    df["Rating"] = pd.to_numeric(df["Rating"])

    df["Reviews"] = pd.to_numeric(df["Reviews"])
 
    df[["Android_Ver"]] = df[["Android_Ver"]].astype(int) 

    df['Installs'] = df['Installs'].str.replace(',','',regex=False)
    df['Installs'] = pd.to_numeric(df['Installs'])

    df['Price'] = df['Price'].str.replace('$','',regex=False)
    df['Price'] = pd.to_numeric(df['Price'])

    #Changing rating to the nearest 0.5
    df['Rating'] = df['Rating'].mul(2).round().div(2)

    return df