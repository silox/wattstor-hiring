# Meteo hiring task

## Installation

1. Create `.env` file from `template.env` template and fill in neccessary data
2. Install and run:
```
poetry install
poetry shell
cd src/
fastapi dev
```
or
```
docker compose up --build
```


## Place for improvement

- The API is not able to filter temperature by exact time / time interval
- Missing handlers for error responses
- Solution would be better with proper API models handling (factories?)
- Proper http codes on some responses
- and more...
