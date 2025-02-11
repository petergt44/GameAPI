
# GameAPI

## Overview

This project provides a centralized API for interacting with multiple third-party game providers. It includes an admin dashboard for managing accounts and API keys, and supports high concurrency and scalability.

## Setup

1. Clone the repository.

2. Create a virtual environment and install dependencies:

```bash

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

3. Set up the databases

```bash

flask db init

flask db migrate

flask db upgrade
```

4. Run the application:

```bash

python run.py
```
## API Documentation

Admin API: /admin/api/ 

Game Provider API: /api/