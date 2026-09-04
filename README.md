# Public Data Aggregator REST API

This example demonstrates how to create a simple, registration-free REST API that aggregates data from multiple public, external data sources. It fetches current exchange rates and public holidays from different APIs and combines them into a single JSON response, accessible without any authentication or API keys.

## Language

`python`

## How to Run

1. Save the code as `main.py`.
2. Install Flask and requests: `pip install Flask requests`.
3. Run the application: `python main.py`.
4. Access the API in your browser or with `curl`: `http://localhost:5000/public-data`.

## Original Article

This example accompanies the Turkish article: [25 Günlük Kamu Verisi Sitesi İçin Kayıtsız REST API Oluşturma Rehberi](https://fatihsoysal.com/blog/25-gunluk-kamu-verisi-sitesi-icin-kayitsiz-rest-api-olusturma-rehberi/).

## License

MIT — see [LICENSE](LICENSE).
