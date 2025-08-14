![Challenge](challenge.png)

## Setup and Installation

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites

- Python 3.10 or higher
- `pip` and `venv`

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd django_swapi
```

### 3. Set Up the Virtual Environment

Create and activate a Python virtual environment to manage project dependencies.

```bash
# For macOS / Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

Install all required packages

```bash
pip install django djangorestframework requests
```

### 5. Apply Database Migrations

Create the database schema based on the models defined in the application.

```bash
python manage.py migrate
```

### 6. Populate the Database

Run the custom management command to fetch data from the SWAPI GraphQL endpoint and populate your local database.

```bash
python manage.py fetch_planets
```

You should see output indicating that planets are being successfully created and saved.

### 7. Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

The API will now be accessible at **`http://127.0.0.1:8000/`**.

## API Endpoints

All endpoints are available under the `/api/` prefix.

#### **List all Planets**

- **Endpoint**: `GET /api/planets/`
- **Description**: Retrieves a list of all planets, ordered by name.
- **`curl` Example**:

  ```bash
  curl http://127.0.0.1:8000/api/planets/
  ```

#### **Retrieve a Single Planet**

- **Endpoint**: `GET /api/planets/{id}/`
- **Description**: Retrieves a single planet by its unique ID.
- **`curl` Example**:

  ```bash
  curl http://127.0.0.1:8000/api/planets/1/
  ```

#### **Create a New Planet**

- **Endpoint**: `POST /api/planets/`
- **Description**: Creates a new planet. Provide climate and terrain names in the `_input` fields. New `Climate` and `Terrain` objects will be created automatically if they don't already exist.
- **`curl` Example**:

  ```bash
  curl -X POST http://127.0.0.1:8000/api/planets/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Coruscant", "population": 1000000000000, "climates_input": ["temperate"], "terrains_input": ["cityscape", "mountains"]}'
  ```

#### **Update a Planet (Full Update)**

- **Endpoint**: `PUT /api/planets/{id}/`
- **Description**: Performs a full update on a planet. All required fields must be provided. The planet's climates and terrains will be replaced with the new lists.
- **`curl` Example**:

  ```bash
  curl -X PUT http://127.0.0.1:8000/api/planets/1/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Tatooine", "population": 250000, "climates_input": ["arid", "hot"], "terrains_input": ["desert"]}'
  ```

#### **Update a Planet (Partial Update)**

- **Endpoint**: `PATCH /api/planets/{id}/`
- **Description**: Performs a partial update on a planet. Only include the fields you want to change.
- **`curl` Example**:

  ```bash
  curl -X PATCH http://127.0.0.1:8000/api/planets/1/ \
  -H "Content-Type: application/json" \
  -d '{"population": 275000}'
  ```

#### **Delete a Planet**

- **Endpoint**: `DELETE /api/planets/{id}/`
- **Description**: Permanently deletes a planet from the database.
- **`curl` Example**:

  ```bash
  curl -X DELETE http://127.0.0.1:8000/api/planets/1/
  ```

## Running Tests

This project includes a comprehensive test suite to ensure functionality and prevent regressions. The tests mock external API calls to run in a sandboxed environment.

To run the tests, execute the following command from the project's root directory:

```bash
python manage.py test
```
