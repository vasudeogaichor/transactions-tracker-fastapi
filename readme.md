# Project Overview
This project utilizes the FastAPI framework to create a web application that handles various operations related to transactions, including uploading files, creating transactions, and retrieving statistics and reports.

# Getting Started
1. Clone the repository:
    ```
    git clone https://github.com/vasudeogaichor/transactions-tracker-fastapi.git
    cd transactions-tracker-fastapi
    ```
2. Install dependencies(if needed create a virtual environment):
    ```
    pip install -r requirements.txt
    ```
3. Create database using docker-compose:
    ```bash
    docker-compose up --build
    ```
4. Run the FastAPI application:
    ```
    uvicorn main:app --reload
    ```
Visit http://localhost:8000/docs to explore the API documentation using Swagger UI.

# Endpoints
## 1. Upload PDF File
<li>Endpoint: `/files/upload/`
<li>Method: `POST`
<li>Description: Upload a PDF file containing transaction data.
<li>Example:

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf" \
  http://localhost:8000/files/upload/
```

## 2. Create Transaction
<li>Endpoint: `/transactions/`
<li>Method: `POST`
<li>Description: Create a new transaction.
<li>Example:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": 80185884,"xref": 100305936, 
    "borrower_name": "CHELSEA BIANCA VANDERAA",
    "description": "Upfront Commission",
    "total_loan_amount": "35,890.00",
    "comm_rate": "1.80",
    "upfront": "646.02",
    "upfront_incl_gst": "710.62"
    }' \
  http://localhost:8000/transactions/
```

## 3. Get Statistics
<li>Endpoint: `/stats/`
<li>Method: `GET`
<li>Description: Get transaction statistics within a specified date range and broker.
<li>Example:

```bash
curl -X GET \
  "http://localhost:8000/stats/?start_date=2023-01-01&end_date=2023-12-31&broker=your_broker"
```

## 4. Generate Report
<li>Endpoint: `/reports/`
<li>Method: `GET`
<li>Description: Generate a report for a specific broker and period (default is daily).
<li>Example:

```bash
curl -X GET \
  "http://localhost:8000/reports/?broker=your_broker&period=monthly"
```