### Welcome to Game Analytics! 🎮

Hey there! Welcome to Game Analytics, where we take gaming seriously... well, sort of. 😄 Whether you're tracking your favorite games, analyzing player data, or just here for the memes, you've come to the right place.

What is Game Analytics?
Game Analytics is your go-to platform for analyzing, well, games! Just upload the csv in the given formats and filter, query and sort the data as you need.. Powered by Django and hosted on [render](https://game-analytics.onrender.com).

---

### Endpoints 🛣️
Here are some of the key endpoints you'll find useful:

| No. | Endpoint | Description |
| --- | --- | --- |
| 1. | `/` | Home: Start here to explore our awesome game database.You will be redirected to upload a csv url instantly. |
| 2. | `api/upload` | Upload the CSV: Enter the link of csv file or google spreadsheet file as well, and start the expected |
| 3. |  `/api/query` | Query Data:  - Search and filter through our vast collection of games from the CSV you uploaded.|
| 4. |  `/api/game_detail/<game_id>` | Dive deep into the details of a specific game.

---

### Features 🎉

1. Filter Games: Use our powerful search tool to search and filter games by name, release date, price, and more.
2. Sort Games: sort games by price, platform availability and many more.
3. Interactive UI: Our user interface is designed for gamers, by gamers. It's slick, it's cool, and it's easy to use.
4. Data Analysis: Dive into statistics and player demographics, reviews, price and more to understand what makes a game a hit.

---

### Limitations ⚠️

1. As of now, there is no authentication system, and only one request can be handled at as time.
2. The database hosted comes with storage limitations, we suggest you to upload file less than 150MB for faster experience.
3. Service is hoted on a free instance at render.com, there may be lags while processing your request. Please be patient.

---

### How to run locally 🚀
To run Game Analytics locally or contribute to our codebase, follow these steps:

1. Clone the Repository:

```bash
git clone https://github.com/your-repo/game-analytics.git
cd game-analytics
```

2. Build the Docker Image:

```bash
docker build -t game-analytics .
```

3. Run the Docker Container:

```bash
docker run -p 8000:8000 game-analytics
```

4. Open Your Browser and visit http://localhost:8000 to start exploring Game Analytics locally.

