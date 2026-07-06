import streamlit as st
import pickle
import pandas as pd

import requests



session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except Exception as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return None
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster =[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies =pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'how would you like to be contacted',
    movies['title'].values
)
if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])

            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")


