## Singular ETL Home assessment.

Weather ETL Pipeline.

A modular, clean-architecture Python ETL pipeline designed to extract weather data from external APIs, transform and normalize tabular records using Pandas, and persist structured outputs to disk.


### Project Structure
```text
src/
├── application/
│   ├── ports/              # Abstract Interfaces (Extractor, Transformer, Loader)
│   └── services/           # Reusable Generic ETL Engine
├── domain/                 # Domain Entities & Models (City, Weather)
├── infrastructure/         # External Adapters (HTTP Client, OpenMeteo API, CSV Writer)
└── use_cases/              # Concrete Pipelines (Weather Extractor & Transformer)
```

### How to run

#### Prerequisites

* Python 3.12+
* uv (fast Python package installer)

#### Setup & Execution

```bash
uv sync # install dependencies
uv run main.py # run script
```

#### Inspect Output:
The output DataFrame will print to stdout and export directly to weather_data.csv.

## Architecture & Solution Design
This project strictly adheres to Clean Architecture (Ports & Adapters / Hexagonal) principles to decouple core data-processing mechanics from domain logic and framework dependencies.

```text
               ┌───────────────────────────────┐
               │             main.py           │
               └───────────────┬───────────────┘
                               │ (Injects dependencies)
                               ▼
 ┌────────────────────────────────────────────────────────────┐
 │ Application Layer                                          │
 │                                                            │
 │   ETLPipeline (Generic Orchestrator)                       │
 │      ├── ExtractorPort<T>  ◄─── WeatherExtractor           │
 │      ├── TransformerPort   ◄─── WeatherTransformer         │
 │      └── LoaderPort        ◄─── CSVLoader                  │
 └─────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
 ┌────────────────────────────────────────────────────────────┐
 │ Domain Layer                                               │
 │                                                            │
 │  City (Entity)   |   Weather (Value Object with @computed) │
 └────────────────────────────────────────────────────────────┘
```

### Key Architectural Concepts

* **Generic Pipeline Engine (`ETLPipeline`):** The orchestration engine in `application/services/etl_pipeline.py` relies solely on generic interfaces (`ExtractorPort`, `TransformerPort`, and `LoaderPort`). It is completely agnostic to weather data.
* **Pluggable Domain Use Cases:** Domain-specific logic lives entirely inside `use_cases/weather.py`. Adding a new pipeline (e.g., `FinancialPipeline` or `TrafficPipeline`) simply requires implementing new extractor/transformer strategy classes without modifying the pipeline engine.
* **Domain Validation & Computed Attributes:** Raw weather records use Pydantic v2 models (`Weather`). Conversion formulas (Celsius to Fahrenheit, mph to m/s) are encapsulated directly on the domain entity using `@computed_field`, ensuring domain logic is co-located with data guarantees.
* **Vectorized Processing:** Once extracted and validated into domain entities, data is converted into Pandas DataFrames inside `WeatherTransformer` to perform high-performance batch operations (sorting, column reordering, and display mapping).

---

## Pros & Cons of Current Design

### Pros
* **High Maintainability & Decoupling:** Swap out `OpenMeteoClient` for a database, or `CSVLoader` for an S3/Parquet loader without touching transformation or orchestration code.
* **Testability:** Every port and adapter can be independently mocked and unit-tested using `pytest`.
* **Zero Engine Over-Engineering:** A single reusable `ETLPipeline` runner manages the execution flow, preventing file bloat across application layers.

### Cons
* **In-Memory Constraints:** Data loading and Pandas transformations run entirely in single-process memory.
* **Monolithic Execution:** Extraction, transformation, and loading occur sequentially within the same runtime context.

---

## Scope & Production-Grade Scalability

### Assessment Context
For the scope of this assignment, the pipeline runs as a single-process application. This design prioritizes **simplicity, readability, and structural clarity** while demonstrating standard software engineering abstractions.

### Scaling to Production-Grade Data Processing
In a real-world, enterprise-scale production environment, monolithic in-process ETL pipelines introduce performance bottlenecks under high volume. To scale this architecture to handle millions of records or real-time streaming, the extraction, transformation, and loading phases should be decoupled into independent, distributed microservices communicating via message brokers:

```text
[ Extractor Service / Workers ]
           │
           ▼  (Publish Event: "RawDataIngested")
  ┌─────────────────┐
  │ Event Stream    │  (Event Stream: Kafka / RabbitMQ)
  └────────┬────────┘
           │
           ▼  (Consume Event)
[ Transformer Service / Workers ] 
           │
           ▼  (Publish Event: "DataNormalized")
  ┌─────────────────┐
  │ Event Stream    │ 
  └────────┬────────┘
           │
           ▼  (Consume Event)
[ Loader Service / Loaders ] ──► [ Data Warehouse / DBs ]
```

#### 1. Decoupled Microservices with Message Brokers (RabbitMQ / Apache Kafka)
* **Extractor Service:** Periodically fetches or listens for API events, emits raw JSON payload messages to a Kafka topic or RabbitMQ queue, and finishes immediately.
* **Transformer Service:** Stateless worker nodes consume raw messages from the stream, perform batch vectorization (using **Polars** or **Apache Spark** instead of single-threaded Pandas), and push normalized schemas to a processed stream.
* **Loader Service:** Dedicated consumer workers write streams into data warehouses (Snowflake, BigQuery, ClickHouse) or data lakes (S3 Parquet).

#### 2. Trade-Offs of Distributed Scaling

| Metric | Monolithic ETL (Current) | Distributed Microservices (Production Scale) |
| :--- | :--- | :--- |
| **Complexity** | Low — single entry point and process. | High — requires container orchestration (K8s) and stream brokers. |
| **Fault Tolerance** | Low — job fails if one step crashes. | High — failed messages re-queue via Dead Letter Queues (DLQ). |
| **Throughput** | Bound by local process RAM/CPU. | Horizontal — scale worker replicas dynamically based on queue depth. |
| **Latency** | Low overhead for small payloads. | Higher per-message latency due to network and broker serialization. |
