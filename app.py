import streamlit as st
import pickle
import requests
import time
import gzip

# --- Page Config ---
st.set_page_config(
    page_title=" Cineva | Discover Movies",
    page_icon="🎥",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
/* Background and Text */
body, .stApp {
    background-color: #0b0c10;
    color: #ffffff;
}

/* Main Title - Cineva */
.main-title {
    font-size: 3.5rem;
    font-weight: 900;
    color: #ffffff;
    text-align: center;
    letter-spacing: 3px;
    text-shadow: 0 0 30px #ffae42, 0 0 60px rgba(255, 174, 66, 0.6);
    margin-top: -10px;
}

/* Tagline */
.tagline {
    font-size: 1.2rem;
    color: #ffae42;
    text-align: center;
    margin-bottom: 50px;
    font-style: italic;
    letter-spacing: 1px;
    opacity: 0.9;
}

/* Dropdown Label */
.stSelectbox label {
    color: #ffae42 !important;
    font-weight: 600;
}

/* Button */
.stButton > button {
    background-color: transparent;
    color: white;
    border: 2px solid #ffae42;
    border-radius: 12px;
    padding: 0.6em 1.3em;
    font-size: 17px;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    background-color: #ffae42;
    color: #0b0c10;
    transform: scale(1.08);
    box-shadow: 0 0 20px #ffae42, 0 0 40px rgba(255,174,66,0.6);
}

/* Section Header (Recommendations) */
.recommend-header {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 25px;
    text-shadow: 0 0 20px rgba(255, 174, 66, 0.6);
}

/* Poster Styling */
/* Poster Styling with Fade-In Animation */
img {
    border-radius: 15px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    box-shadow: 0 0 10px rgba(255,174,66,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease, opacity 0.8s ease;
    opacity: 0;
    animation: fadeIn 1s forwards;
}

img:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(255,174,66,0.7);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

</style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='main-title'>Cineva</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>Discover your next favorite movie with Cineva.</p>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f01207551c40be749ec30ae3a34xxxxx&language=en-US' #Login & use your own API key
    for attempt in range(3):
        try:
            response = requests.get(url, timeout=1)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster+Available"
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )
    recommended_movies_names = []
    recommended_movies_posters = []
    recommended_movie_ratings = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies.iloc[i[0]].title)
        recommended_movie_ratings.append(movies.iloc[i[0]].vote_average)
        time.sleep(0.2)
        
    return recommended_movies_names, recommended_movies_posters, recommended_movie_ratings


# --- Load Data ---
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
with gzip.open('artifacts/similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


movie_list = movies['title'].values
selected_movie = st.selectbox(' Type or select a movie to get recommendations', movie_list)

# --- Button + Results ---
if st.button('Show Recommendation'):
    names, posters, ratings = recommend(selected_movie)
    

    if names:  # Only show header if recommendations exist
        st.markdown("<h2 class='recommend-header'>✨ Top Recommendations for You ✨</h2>", unsafe_allow_html=True)
        
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <div style="text-align:center; background-color:#111; border-radius:12px; padding:10px; margin:0 auto; width:180px;">
                        <img src="{posters[i]}" style="width:100%; border-radius:10px;"/>
                        <p class="movie-title" style="color:#fff; margin:6px 0 2px 0; font-weight:600;">{names[i]}</p>
                        <p style="color:#ffcc00; font-size:14px; margin:0;">⭐ {ratings[i]:.1f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            
