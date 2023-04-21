import streamlit as st

import pickle
import requests
import gzip

movies = pickle.load(open("movies.pkl", "rb"))

def load_zipped_pickle(filename):
    with gzip.open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object

similarity = load_zipped_pickle("similarity.pkl")

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=7abe55021fbd937945a1d7fc5a996fb5&language=en-US_id".format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

def recommend(movie):
    indice = movies[movies.title == movie].index[0]
    dist = list(sorted(enumerate(similarity[indice]), reverse=True, key=lambda x: x[1]))[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for x in dist:
        recommended_movies.append(movies.title.iloc[x[0]])
        # Fetching poster from API
        requested_id = movies.iloc[x[0]].movie_id
        recommended_movies_poster.append(fetch_poster(requested_id))

    return recommended_movies, recommended_movies_poster






movies_list = movies["title"].values
st.title("MOVIE RECOMMENDER SYSTEM")

selected_movie_name = st.selectbox("Select a movie to find out similar movies",
                      movies_list
                      )

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
