# Nutrition Insights API

Nutrition Insights API is a Flask-based REST API that integrates with the USDA FoodData Central API to provide nutritional information, nutrient analysis, and food comparisons. The project applies custom business logic to process nutrient data, select the most relevant food results, and generate human-readable insights from nutritional content.

This project was built to demonstrate backend software engineering skills, including API design, layered architecture, dependency injection, testing, and configuration management.

---

## Features

* Search for foods using the USDA FoodData Central API.
* Process USDA nutrient data into a consistent API response format.
* Generate nutrient insights (e.g., "high protein", "low fiber").
* Compare two foods and generate comparison insights.
* Validate user input and handle API errors gracefully.
* Comprehensive unit and API testing using `pytest`.
* Environment variable configuration for API keys.
* Dependency injection for improved testability.
* Mocking of external API calls using `unittest.mock`.

---

## Tech Stack

* Python 3
* Flask
* Pytest
* Requests
* python-dotenv
* USDA FoodData Central API
* Git / GitHub

---

## Project Structure

```text
NutritionInsightsAPI/
│
├── app/
│   ├── api/
│   │   └── food.py
│   │
│   ├── clients/
│   │   └── usda_client.py
│   │
│   ├── core/
│   │   ├── food_service_helper.py
│   │   └── validation.py
│   │
│   ├── services/
│   │   └── food_service.py
│   │
│   ├── config.py
│   ├── extensions.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_food_api.py
│   ├── test_food_service.py
│   ├── test_food_service_helper.py
│   ├── test_usda_client.py
│   └── test_validation.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── requirements.txt
├── README.md
└── run.py
```

---

## Architecture

The application follows a layered architecture:

```text
Client Request
      ↓
API Routes
      ↓
Service Layer
      ↓
Helper Functions
      ↓
USDA Client
      ↓
USDA FoodData Central API
```

This separation of concerns improves maintainability, testability, and scalability.

---

## API Endpoints

### Get Food Information

```http
GET /api/food?query=banana
```

Example Response:

```json
{
    "success": true,
    "data": {
        "food": "Banana, raw",
        "macros": {
            "calories": 89,
            "protein": 1.1
        },
        "insights": [
            "low protein"
        ]
    }
}
```

---

### Compare Foods

```http
GET /api/comparison?food1=chicken&food2=apple
```

Example Response:

```json
{
    "success": true,
    "data": {
        "food1": "Chicken",
        "food2": "Apple",
        "comparison_insights": [
            "Chicken has more protein than Apple - (27 vs 1)"
        ]
    }
}
```

---

### Meal Analysis (Planned)

```http
POST /api/meal
```

> **Note:** Meal analysis is currently under development and planned for a future update.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/BraxtonChatman/NutritionInsightsAPI
cd NutritionInsightsAPI
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root based on `.env.example`.

If no API key is provided, the application defaults to the USDA `DEMO_KEY`.

```env
USDA_API_KEY=your_api_key_here
```

---

## Running the Application

```bash
python run.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

---

## Running Tests

Run all tests:

```bash
python -m pytest
```

Run tests with verbose output:

```bash
python -m pytest -v
```

Current tests include:

* Validation functions
* USDA client
* Service layer
* Helper functions
* API endpoints
* Error handling
* External API mocking

---

## Example Usage

Retrieve food information:

```bash
curl "http://127.0.0.1:5000/api/food?query=banana"
```

Compare two foods:

```bash
curl "http://127.0.0.1:5000/api/comparison?food1=chicken&food2=apple"
```

---

## Future Improvements

* Complete `POST /api/meal` endpoint.
* Add SQLite caching to reduce USDA API calls.
* Add Swagger/OpenAPI documentation.
* Add Docker support.
* Add GitHub Actions CI pipeline.
* Add application logging.
* Add rate limiting.
* Deploy the application to Render.

---

## What I Learned

This project provided hands-on experience with:

* Designing REST APIs with Flask
* Building layered applications
* Managing configuration with environment variables
* Writing unit and API tests with Pytest
* Mocking external dependencies
* Dependency injection patterns
* Error handling and validation
* Organizing maintainable Python applications
* Working with third-party APIs

---

## License

This project is licensed under the MIT License.
