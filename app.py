import requests
import os
import pickle
import pandas as pd
import streamlit as st

# ----------------------------
# Helper to download files
# ----------------------------
def download_file(file_id, output):
    if os.path.exists(output):
        return
    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={"id": file_id}, stream=True)
    with open(output, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# ----------------------------
# Download artifacts if missing
# ----------------------------
if not os.path.exists("artifacts"):
    os.mkdir("artifacts")

movie_dict_file = "artifacts/movie_dict.pkl"
similarity_file = "artifacts/similarity.pkl"

movie_dict_id = "1Ua1qEsv0QraXCCZKrQmW18XBNCd-Y1Zf"
similarity_id = "1cnXhAy8nqRQDtAW4Q4xolc93bYgfwHIj"

download_file(movie_dict_id, movie_dict_file)
download_file(similarity_id, similarity_file)

# ----------------------------
# Load pickle files
# ----------------------------
with open(movie_dict_file, "rb") as f:
    movies_dict = pickle.load(f)

with open(similarity_file, "rb") as f:
    similarity = pickle.load(f)

movies = pd.DataFrame(movies_dict)

# ----------------------------
# Helper functions
# ----------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return ""

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster

# ----------------------------
# Streamlit app UI
# ----------------------------
st.header("Flair Movies Recommendation System")

movie_list = movies['title'].tolist()
selected_movie = st.selectbox('Select a movie to get a recommendation', movie_list)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        col.text(recommended_movies_name[idx])
        if recommended_movies_poster[idx]:
            col.image(recommended_movies_poster[idx])
