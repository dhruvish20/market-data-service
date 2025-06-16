# Market Data Microservice

A real-time market data microservice designed with FastAPI, Kafka, PostgreSQL, Redis, and Docker. This system allows polling of stock prices from providers like YFinance, stores raw and processed data, and serves the latest price efficiently using Redis caching.

---

## Features

* **FastAPI REST Interface** for polling and fetching stock prices
* **YFinance Provider Integration** to fetch real-time prices
* **Polling Job System** to schedule repeated data pulls
* **Kafka Message Queue** for decoupling data fetch and processing
* **PostgreSQL Database** for storing raw and computed data
* **Redis Cache** to serve latest prices quickly
* **Dockerized Setup** with multi-container orchestration
* **Swagger UI** for testing the API

---

## Architecture Overview

```
Client ──> FastAPI ──┬────> PostgreSQL (Raw Prices + Moving Averages)
                    │
                    ├────> Kafka Producer ──> Kafka ──> Consumer ──> DB + Redis
                    │
                    └────> YFinance API (price polling)
```

---

## Technologies Used

* **FastAPI** — Lightweight modern Python web framework
* **YFinance** — Market data provider
* **PostgreSQL** — Persistent storage for raw and processed prices
* **Kafka + Zookeeper** — Message brokering between polling and consumer logic
* **Redis** — In-memory cache to serve latest prices quickly
* **Docker** — Containerization of all services
* **Uvicorn** — ASGI server to run FastAPI

---

## Folder Structure

```
market-data-service/
├── app/
│   ├── api/          # FastAPI routes
│   ├── core/         # DB & Redis connections
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic request/response schemas
│   └── services/     # Kafka, polling, providers
├── scripts/          # Polling runner & consumer
├── docker-compose.yaml
├── requirements.txt
└── .env              # Environment variables
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/dhruvish20/market-data-service.git
cd market-data-service
```

### 2. Configure Environment Variables

Create a `.env` file with:

```ini
DB_HOST=db
DB_PORT=5432
DB_NAME=marketdata
DB_USER=postgres
DB_PASSWORD=postgres
REDIS_HOST=redis
REDIS_PORT=6379
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
```

### 3. Launch Services

```bash
docker-compose up --build -d
```

### 4. Initialize the Database

```bash
docker-compose exec app bash -c "PYTHONPATH=/app python scripts/init_db.py"
```

---

## 🧪 API Usage

Visit Swagger UI:

```
http://localhost:8000/docs
```

### POST `/prices/poll`

Schedule a polling job:

```json
{
  "symbols": ["AAPL"],
  "interval": 60,
  "provider": "yfinance"
}
```

### GET `/prices/latest`

Query latest price (uses Redis cache if available):

```http
/prices/latest?symbol=AAPL&provider=yfinance
```

### GET `/test-db`

Health check for DB connection.

---

## Running Background Services

### Run Polling Job Runner

```bash
docker-compose exec app bash -c "PYTHONPATH=/app python scripts/run_polling_jobs.py"
```

### Run Kafka Consumer

```bash
docker-compose exec app bash -c "PYTHONPATH=/app python scripts/consumer.py"
```

---

## Key Concepts Explained

### Polling Jobs

Defined via POST `/prices/poll`, they store symbol, provider, and interval in DB. A background runner checks every second for due jobs and fetches fresh prices.

### Kafka Event Pipeline

When a new price is fetched:

1. It is stored in `raw_market_data`
2. A Kafka message is published
3. Kafka consumer computes the moving average of latest 5 prices
4. The result is saved to `symbol_averages` and cached in Redis

### Redis Caching

When the client calls `/prices/latest`, the system:

* First checks Redis (`latest_price_{symbol}_{provider}`)
* If not found, fetches from DB and sets cache with TTL (e.g., 5 mins)

---

##  Deployment (AWS EC2)

### EC2 Setup

* Ubuntu 22.04 t2.micro
* Open ports: 22 (SSH), 8000 (FastAPI), 9092 (Kafka)

### Clone, Setup & Run

```bash
ssh -i ~/.ssh/your-key.pem ubuntu@<EC2-PUBLIC-IP>
git clone <your-repo>
cd market-data-service
nano .env
sudo docker-compose up -d --build
```

### Start Scripts

```bash
sudo docker-compose exec app bash -c "PYTHONPATH=/app python scripts/init_db.py"
sudo docker-compose exec app bash -c "PYTHONPATH=/app python scripts/run_polling_jobs.py"
sudo docker-compose exec app bash -c "PYTHONPATH=/app python scripts/consumer.py"
```

---

## What's Working

* ✅ End-to-end polling of stock prices via YFinance
* ✅ Kafka message queue and consumer logic
* ✅ Moving average computation
* ✅ Redis caching and TTL logic
* ✅ Dockerized deployment
* ✅ Hosted Swagger UI

---

## Future Improvements

* Add `/prices/average` endpoint to expose moving averages
* Add test suite using Pytest
* Auto-scale consumer and polling runners
* Grafana dashboard integration

---

## Contact

Built by Dhruvish Parekh — Open to feedback and collaboration!
