from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse

from src.infrastructure.config import settings

app = FastAPI(
    title="Weather ETL Web API",
    description="Serves generated weather charts and CSV datasets.",
    version="1.0.0",
)

@app.get(
    "/graphs",
    response_class=FileResponse,
    summary="View Temperature Bar Chart",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Renders the PNG bar chart directly in the browser.",
        },
        404: {"description": "Chart file not found."},
    },
)
def get_temperature_chart():
    chart_path = Path(settings.chart_output_path)

    if not chart_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart image not found. Please run 'python main.py' first.",
        )

    return FileResponse(
        path=chart_path,
        media_type="image/png",
        content_disposition_type="inline",
    )


@app.get(
    "/csv",
    response_class=FileResponse,
    summary="Download Weather CSV",
    responses={
        200: {"content": {"text/csv": {}}, "description": "Returns CSV file."},
        404: {"description": "CSV file not found. Run main.py first."},
    },
)
def get_weather_csv():
    csv_path = Path(settings.csv_output_path)

    if not csv_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CSV file not found. Please run 'python main.py' first.",
        )

    return FileResponse(
        path=csv_path,
        media_type="text/csv",
        filename="weather_data.csv",
    )
