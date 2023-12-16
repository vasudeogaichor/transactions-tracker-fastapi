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
<li>Example Request:

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf" \
  http://localhost:8000/files/upload/
```
<li> Example Response:

```bash
{
    "message": "No. of Successful transactions: 84, 
    Unsuccessful transactions: []"
}
```

## 2. Create Transaction
<li>Endpoint: `/transactions/`
<li>Method: `POST`
<li>Description: Create a new transaction.
<li>Example Request:

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
<li> Example Response:

```bash
{
    "id": 632,
    "tier": 3,
    "app_id": 80185884,
    "xref": 100305936,
    "settlement_date": "17/10/2023",
    "broker": "Cheston La'Porte",
    "borrower_name": "CHELSEA BIANCA VANDERAA",
    "description": "Upfront Commission",
    "total_loan_amount": "35,890.00",
    "comm_rate": "1.80",
    "upfront": "646.02",
    "upfront_incl_gst": "710.62"
}
```
## 3. Get Statistics
<li>Endpoint: `/stats/`
<li>Method: `GET`
<li>Description: Get transaction statistics within a specified date range and broker.
<li>Example Request:

```bash
curl -X GET \
  "http://localhost:8000/stats/?start_date=2023-01-01&end_date=2023-12-31&broker=your_broker"
```
<li> Example Response:

```bash
{
    "total_number_of_loans": 46,
    "total_loan_amount": 2057387.4000000001,
    "average_loan_amount": 44725.813043478265,
    "loan_with_lowest_amount": {
        "app_id": 80187980,
        "xref": 100305835,
        "settlement_date": "2023-10-17",
        "broker": "Auswide Financial Solutions Pty Ltd",
        "sub_broker": "Carole Leedham RICHARD EDWARDS",
        "borrower_name": "",
        "description": "Upfront Commission",
        "total_loan_amount": 17168.11,
        "comm_rate": 1.8,
        "upfront": 309.03,
        "upfront_incl_gst": 339.93,
        "id": 629,
        "tier": 3
    },
    "loan_with_highest_amount": {
        "app_id": 80185966,
        "xref": 100306529,
        "settlement_date": "2023-10-24",
        "broker": "Chris Stafford",
        "sub_broker": null,
        "borrower_name": "DAMIAN JAMES WORTH ",
        "description": "Upfront Commission",
        "total_loan_amount": 83794.51,
        "comm_rate": 1.8,
        "upfront": 1508.3,
        "upfront_incl_gst": 1659.13,
        "id": 565,
        "tier": 2
    }
}
```
## 4. Generate Report
<li>Endpoint: `/reports/`
<li>Method: `GET`
<li>Description: Generate a report for a specific broker and period (default is daily).
<li>Example Request:

```bash
curl -X GET \
  "http://localhost:8000/reports/?broker=your_broker&period=monthly"
```
<li>Example Response:

```bash
{
    "monthly": [
        {
            "2023-10-01": {
                "max_total_loan_amount": 77590.87,
                "min_total_loan_amount": 23244.74,
                "sum_total_loan_amount": 752158.3099999999
            }
        }
    ],
    "weekly": [
        {
            "2023-10-09": {
                "max_total_loan_amount": 77590.87,
                "min_total_loan_amount": 30490.0,
                "sum_total_loan_amount": 207237.12
            }
        },
        {
            "2023-10-16": {
                "max_total_loan_amount": 23244.74,
                "min_total_loan_amount": 23244.74,
                "sum_total_loan_amount": 23244.74
            }
        },
        {
            "2023-10-02": {
                "max_total_loan_amount": 76193.0,
                "min_total_loan_amount": 36390.0,
                "sum_total_loan_amount": 148973.0
            }
        },
        {
            "2023-10-23": {
                "max_total_loan_amount": 67535.7,
                "min_total_loan_amount": 34490.0,
                "sum_total_loan_amount": 372703.44999999995
            }
        }
    ],
    "daily": [
        {
            "2023-10-10": {
                "max_total_loan_amount": 43890.0,
                "min_total_loan_amount": 43890.0,
                "sum_total_loan_amount": 43890.0
            }
        },
        {
            "2023-10-04": {
                "max_total_loan_amount": 36390.0,
                "min_total_loan_amount": 36390.0,
                "sum_total_loan_amount": 36390.0
            }
        },
        {
            "2023-10-27": {
                "max_total_loan_amount": 67535.7,
                "min_total_loan_amount": 47022.46,
                "sum_total_loan_amount": 235049.1
            }
        },
        {
            "2023-10-12": {
                "max_total_loan_amount": 77590.87,
                "min_total_loan_amount": 77590.87,
                "sum_total_loan_amount": 77590.87
            }
        },
        {
            "2023-10-03": {
                "max_total_loan_amount": 36390.0,
                "min_total_loan_amount": 36390.0,
                "sum_total_loan_amount": 36390.0
            }
        },
        {
            "2023-10-05": {
                "max_total_loan_amount": 76193.0,
                "min_total_loan_amount": 76193.0,
                "sum_total_loan_amount": 76193.0
            }
        },
        {
            "2023-10-25": {
                "max_total_loan_amount": 51774.35,
                "min_total_loan_amount": 34490.0,
                "sum_total_loan_amount": 86264.35
            }
        },
        {
            "2023-10-11": {
                "max_total_loan_amount": 55266.25,
                "min_total_loan_amount": 30490.0,
                "sum_total_loan_amount": 85756.25
            }
        },
        {
            "2023-10-24": {
                "max_total_loan_amount": 51390.0,
                "min_total_loan_amount": 51390.0,
                "sum_total_loan_amount": 51390.0
            }
        },
        {
            "2023-10-17": {
                "max_total_loan_amount": 23244.74,
                "min_total_loan_amount": 23244.74,
                "sum_total_loan_amount": 23244.74
            }
        }
    ]
}
```