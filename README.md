# GameAPI

## Overview

This project provides a centralized API for interacting with multiple third-party game providers across five categories. It includes an admin dashboard for managing accounts and API keys and supports high concurrency and scalability using Flask, Flask-RESTx, Flask-SQLAlchemy, and Redis caching.

The API supports the following game provider categories:

- **Category 1**: Gameroom, Cash Machine, Mr All In One, Cash Frenzy, Mafia, King of Pop
- **Category 2**: Game Vault, Vegas Sweeps, Juwa
- **Category 3**: Orion Stars, Panda Master, Milkyway, Fire Kirin
- **Category 4**: River Sweeps
- **Category 5**: Vblink, Egame, Ultra Panda

## Setup

### 1. Clone the Repository
```bash
git clone <repository_url>
cd GameAPI
```

### 2. Create a Virtual Environment and Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set Up Environment Variables (optional)
- Create a `.env` file in the root directory:

  ```text
  SECRET_KEY=your_secret_key
  CAPTCHA_API_KEY=your_2captcha_api_key
  ```

- The `config.py` file defaults to `postgresql://username:password@127.0.0.1:5432/db` and Redis at `localhost:6379/0` if not overridden.

### 4. Set Up the Database
- Initialize and migrate the database:

  ```bash
  flask db init
  flask db migrate
  flask db upgrade
  ```

- Populate the `Provider` table with initial data:

  ```bash
  python seed_providers.py
  ```

### 5. Ensure Redis is Running
- Install Redis (`sudo apt-get install redis-server` on Ubuntu or `brew install redis` on macOS).
- Start Redis:

  ```bash
  redis-server &
  ```

### 6. Run the Application
```bash
python run.py
```

## API Documentation

### Admin API
- **Base URL**: `/admin/api/`
- **Endpoints**: `login`, `accounts`, `tokens`, `logs`

### Game Provider API
- **Base URL**: `/categoryX/` (where X is 1–5)
- **Endpoints**: `login`, `add_user`, `recharge`, `redeem`, `reset_password`, `balance`, `agent_balance`

### Swagger UI
- Access interactive documentation at: [localhost/swagger/](http://192.168.100.9:8080/swagger/