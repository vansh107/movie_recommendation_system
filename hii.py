import requests
import time

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0"
}

for i in range(10):
    try:
        r = session.get(
            "https://api.themoviedb.org/3/movie/550?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US",
            headers=headers,
            timeout=10
        )
        print(i, r.status_code)
        time.sleep(1)   # 1 second wait
    except Exception as e:
        print(i, e)