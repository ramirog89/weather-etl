## Singular ETL Home assessment.

Weather ETL Pipeline.

A modular, clean-architecture Python ETL pipeline designed to extract weather data from external APIs, transform and normalize tabular records using Pandas, and persist structured outputs to disk.


### Project Structure
```text
src/
├── application/
│   ├── ports/              # Abstract Interfaces (Extractor, Transformer, Loader, Geocoding)
│   └── services/           # Application Services (ETLPipeline, CityResolverService)
├── domain/                 # Domain Entities & Models (City, Weather, Custom Exceptions)
├── infrastructure/         # External Adapters (HTTP Client, OpenMeteo APIs, CSV Loader, Visualizer)
└── use_cases/              # Pipeline Use Cases (Weather Extractor & Transformer)
```

### How to run

#### Prerequisites

* Python 3.12+

### Option 1: Using `uv` (Recommended)

```bash
# Sync environment and install dependencies
uv sync

# Run pipeline with default cities
uv run main.py

# Run pipeline with custom cities
uv run main.py --cities "New York" Tokyo "Buenos Aires"
```

### Option 2: Using standard `pip` and `venv`

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python main.py --cities "New York" Tokyo "Buenos Aires"
```

### Web API Server

1. **Run the ETL pipeline to generate outputs:**
```bash
uv run main.py
```

2. **Start the API server:**
```bash
# uv
uv run uvicorn src.infrastructure.http.server:app --reload

# python
python -m uvicorn src.infrastructure.http.server:app --reload
```

3. **Access Endpoints:**

* Chart Image: http://127.0.0.1:8000/graphs
* CSV Download: http://127.0.0.1:8000/csv


## Interpreting the Output

Upon successful execution, the pipeline generates two output artifacts in the `output/` directory:

### 1. Weather Data CSV (`output/weather_data.csv`)
The primary tabular output containing normalized weather metrics for all resolved cities, sorted by current temperature in descending order (warmest to coolest).

* **`City`**: Name of the target city.
* **`Temperature (C)`**: Current ambient temperature in degrees Celsius (°C).
* **`Temperature (F)`**: Current ambient temperature in degrees Fahrenheit (°F).
* **`Humidity (%)`**: Current relative humidity %.
* **`Wind Speed (m/s)`**: Current wind speed measured in meters per second (ms).
* **`Wind Speed (mph)`**: Current wind speed measured in miles per hour (mp/h).

### 2. Temperature Comparison Chart (`output/temperature_chart.png`)
A generated bar chart visually comparing the current temperatures across all processed cities. This provides an immediate visual summary of regional temperature variations without parsing raw CSV rows.
