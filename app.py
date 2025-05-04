import pickle
import streamlit as st
import requests

# --- Load data ---
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# --- Streamlit page setup ---
st.set_page_config(page_title=" Movie Recommender", layout="wide")

# --- Sidebar ---
st.sidebar.title("Settings")

# Theme Toggle
theme = st.sidebar.radio("Theme", ["Dark", "Light"], index=0)

# Genre Dropdown (UI only for now)
genre = st.sidebar.selectbox("Genre (for UI only)", ["All", "Action", "Comedy", "Drama", "Horror", "Sci-Fi"])

# Search Input
search_query = st.sidebar.text_input("Search Movie Title")

# --- Apply Theme CSS ---
dark_css = """
    <style>
        .stApp {
            background-color: #000000;
        }
        .main-title {
            color: #FFFFFF;
        }
        .movie-box {
            background-color: #1a1a1a;
            border: 1px solid #333;
        }
        .stButton > button {
            background-color: #ff4b2b;
            color: white;
        }
        .stButton > button:hover {
            background-color: #e03e1f;
            color: #FFFFFF;
        }
        .stButton > button:active {
            background-color: #e03e1f;
            color: #FFFFFF;
        }
        .css-18e3th9 { background-color: #000000; }  /* Sidebar */
        .css-1d391kg { background-color: #000000; }  /* Main container */
    </style>
"""

light_css = """
    <style>
        .stApp {
            background-color: #FFFFFF;
        }
        .main-title {
            color: #000000;
        }
        .movie-box {
            background-color: #f2f2f2;
            border: 1px solid #ccc;
        }
        .stButton > button {
            background-color: #ff4b2b;
            color: white;
        }
        .stButton > button:hover {
            background-color: #e03e1f;
            color: white;
        }
        .css-18e3th9 { background-color: #FFFFFF; }  /* Sidebar */
        .css-1d391kg { background-color: #FFFFFF; }  /* Main container */
    </style>
"""
# Font and Style
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Raleway', sans-serif;
        }
        .main-title {
            font-size: 3em;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .movie-title {
            font-weight: 600;
            text-align: center;
            margin-top: 8px;
            font-size: 16px;
        }
        .movie-box {
            padding: 10px;
            border-radius: 12px;
            transition: 0.3s;
        }
        .movie-box:hover {
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# Inject selected theme
st.markdown(dark_css if theme == "Dark" else light_css, unsafe_allow_html=True)

# --- Movie Filtering ---
movie_list = movies['title'].values
if search_query:
    movie_list = [title for title in movie_list if search_query.lower() in title.lower()]

# --- Main UI ---
st.markdown('<div class="main-title">Movie Recommender System</div>', unsafe_allow_html=True)
selected_movie = st.selectbox("Select a movie to get recommendations", movie_list)

# --- API Fetch Poster ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"

# --- Recommend Function ---
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# --- Show Recommendations ---
if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown('<div class="movie-box">', unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)
            st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
