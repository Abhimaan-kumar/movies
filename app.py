import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd167966397ea12ac168da84d2e8&language=en-US')
    data = response.json()
    

    # Check if 'poster_path' is present in the data
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        # Return a placeholder image if 'poster_path' is missing
        return "https://via.placeholder.com/500x750?text=No+Image+Available"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    posters = []

    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure you're accessing the movie ID from the DataFrame
        movie_title = movies.iloc[i[0]].title
        posters.append(fetch_poster(movie_id))
        recommended_movies.append(movie_title)

    return recommended_movies, posters


st.title('Movies Recommender System')

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

option = st.selectbox(
'How would you like to be contacted?',
movies['title'].values)

if st.button('Recommend'):
    recommendations, post = recommend(option)
    cols = st.columns(5)  # Create 5 columns

    for i in range(min(len(recommendations), 5)):  # Ensure we only loop up to the number of columns
        with cols[i]:
            st.text(recommendations[i])
            st.image(post[i])
