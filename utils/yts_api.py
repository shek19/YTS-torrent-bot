import requests
import re
BASE_URL = "https://yts.mx/api/v2/"

def search_movies(query):
    match = re.search(r"\b(19\d{2}|20\d{2})\b", query)
    year = None
    if match:
        year = int(match.group(0))
        title = query.replace(str(year), "").strip()
    else:
        title = query

    try:
        url = f"{BASE_URL}list_movies.json?query_term={query}"
        response = requests.get(url, timeout=10) 
        response.raise_for_status()  # raises HTTPError if not 200
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return None
    except ValueError:
        print("Invalid JSON from YTS API")
        return None
    movies = data.get("data",{}).get("movies", [])
    if not movies:
        return None

    if year:            
        #filtering by movie year
        for movie in movies:
            if movie.get("title", "").lower() == title.lower() and movie.get("year") == year:
                return movie["id"]
            
    return movies[0].get("id")

def get_torrent(movie_id):
    try:
        url = f"{BASE_URL}movie_details.json?movie_id={movie_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return None, None, []
    except ValueError:
        print("Invalid JSON from YTS API")
        return None, None, []

    movie = data.get("data", {}).get("movie", {})
    title = movie.get("title", "")
    year = movie.get("year", None)
    torrents_raw = movie.get("torrents", [])
    
    torrents = []
    for torrent in torrents_raw:
        torrent_info = {
            'quality': torrent.get('quality', 'Unknown'),
            'size': torrent.get('size', 'Unknown'),
            'url': torrent.get('url', '')  # This is the direct .torrent download URL
        }
        torrents.append(torrent_info)

    return title, year, torrents

