import requests
BASE_URL = "https://yts.mx/api/v2/"

def search_movies(query):
    url = f"{BASE_URL}list_movies.json?query_term={query}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    movies = data["data"].get("movies", [])
    movie_id = movies[0]["id"] if movies else None

    return movie_id

def get_torrent(movie_id):
    url = f"{BASE_URL}movie_details.json?movie_id={movie_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print("error connecting to YTS API")
        return []
    
    data = response.json()
    movie = data["data"].get("movie", {})
    title = movie.get("title", "")
    torrents = movie.get("torrents", [])

    return title, torrents

    

