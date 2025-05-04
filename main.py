from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


df = pd.read_csv('data.csv', encoding='ISO-8859-1', on_bad_lines='skip')
df.fillna('Null', inplace=True) 
df_array = df.to_numpy()

@app.get("/api/all-books")
async def greet():
    return df_array.tolist()

@app.get("/api/books/")
async def get_books(category: str = "", rating: str = "", publishedYear: str = "", searchQuery: str = ""):
    filtered_df = df.copy()

    if category:
        filtered_df = filtered_df[filtered_df['categories'].str.contains(category, case=False, na=False)]
    
    if rating:
        try:
            rating_float = float(rating)
            filtered_df = filtered_df[filtered_df['average_rating'] >= rating_float]
        except ValueError:
            pass  

    if publishedYear:
        filtered_df = filtered_df[filtered_df['published_year'].astype(str).str.contains(publishedYear, na=False)]

    if searchQuery:
        filtered_df = filtered_df[filtered_df['title'].str.contains(searchQuery, case=False, na=False) | 
                                  filtered_df['authors'].str.contains(searchQuery, case=False, na=False)]
        
    filtered_df.fillna('Null', inplace=True)
    filtered_df_array = filtered_df.to_numpy()
    return filtered_df_array.tolist()
