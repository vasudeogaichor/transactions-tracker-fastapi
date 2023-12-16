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
                "max_total_loan_amount": 89199.0,
                "min_total_loan_amount": 15530.0,
                "sum_total_loan_amount": 4158581.1400000006,
                "tier_1_count": 1,
                "tier_2_count": 34,
                "tier_3_count": 55
            }
        }
    ],
    "weekly": [
        {
            "2023-10-02": {
                "max_total_loan_amount": 89199.0,
                "min_total_loan_amount": 26390.0,
                "sum_total_loan_amount": 995943.2599999999,
                "tier_1_count": 0,
                "tier_2_count": 7,
                "tier_3_count": 14
            }
        },
        {
            "2023-10-16": {
                "max_total_loan_amount": 54588.07,
                "min_total_loan_amount": 17168.11,
                "sum_total_loan_amount": 643938.8999999999,
                "tier_1_count": 1,
                "tier_2_count": 3,
                "tier_3_count": 12
            }
        },
        {
            "2023-10-23": {
                "max_total_loan_amount": 83794.51,
                "min_total_loan_amount": 17628.34,
                "sum_total_loan_amount": 1389404.69,
                "tier_1_count": 0,
                "tier_2_count": 11,
                "tier_3_count": 19
            }
        },
        {
            "2023-10-09": {
                "max_total_loan_amount": 81620.0,
                "min_total_loan_amount": 15530.0,
                "sum_total_loan_amount": 1069360.48,
                "tier_1_count": 0,
                "tier_2_count": 12,
                "tier_3_count": 10
            }
        },
        {
            "2023-10-30": {
                "max_total_loan_amount": 59933.81,
                "min_total_loan_amount": 59933.81,
                "sum_total_loan_amount": 59933.81,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 0
            }
        }
    ],
    "daily": [
        {
            "2023-10-24": {
                "max_total_loan_amount": 83794.51,
                "min_total_loan_amount": 17845.41,
                "sum_total_loan_amount": 273312.12,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 4
            }
        },
        {
            "2023-10-17": {
                "max_total_loan_amount": 54588.07,
                "min_total_loan_amount": 17168.11,
                "sum_total_loan_amount": 496482.92,
                "tier_1_count": 1,
                "tier_2_count": 1,
                "tier_3_count": 11
            }
        },
        {
            "2023-10-18": {
                "max_total_loan_amount": 54342.99,
                "min_total_loan_amount": 54342.99,
                "sum_total_loan_amount": 108685.98,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 0
            }
        },
        {
            "2023-10-10": {
                "max_total_loan_amount": 73400.07,
                "min_total_loan_amount": 15530.0,
                "sum_total_loan_amount": 295420.05000000005,
                "tier_1_count": 0,
                "tier_2_count": 4,
                "tier_3_count": 2
            }
        },
        {
            "2023-10-04": {
                "max_total_loan_amount": 57610.0,
                "min_total_loan_amount": 36390.0,
                "sum_total_loan_amount": 172510.0,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 3
            }
        },
        {
            "2023-10-27": {
                "max_total_loan_amount": 67535.7,
                "min_total_loan_amount": 25527.81,
                "sum_total_loan_amount": 405743.01,
                "tier_1_count": 0,
                "tier_2_count": 4,
                "tier_3_count": 4
            }
        },
        {
            "2023-10-26": {
                "max_total_loan_amount": 56886.19,
                "min_total_loan_amount": 28390.0,
                "sum_total_loan_amount": 161656.19,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 3
            }
        },
        {
            "2023-10-06": {
                "max_total_loan_amount": 59060.2,
                "min_total_loan_amount": 35380.0,
                "sum_total_loan_amount": 130150.2,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 2
            }
        },
        {
            "2023-10-09": {
                "max_total_loan_amount": 81620.0,
                "min_total_loan_amount": 24171.58,
                "sum_total_loan_amount": 274484.56,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 4
            }
        },
        {
            "2023-10-30": {
                "max_total_loan_amount": 59933.81,
                "min_total_loan_amount": 59933.81,
                "sum_total_loan_amount": 59933.81,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 0
            }
        },
        {
            "2023-10-23": {
                "max_total_loan_amount": 70744.0,
                "min_total_loan_amount": 17628.34,
                "sum_total_loan_amount": 136091.49,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 2
            }
        },
        {
            "2023-10-05": {
                "max_total_loan_amount": 81600.0,
                "min_total_loan_amount": 26390.0,
                "sum_total_loan_amount": 304373.0,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 4
            }
        },
        {
            "2023-10-25": {
                "max_total_loan_amount": 67085.07,
                "min_total_loan_amount": 34490.0,
                "sum_total_loan_amount": 412601.88,
                "tier_1_count": 0,
                "tier_2_count": 3,
                "tier_3_count": 6
            }
        },
        {
            "2023-10-11": {
                "max_total_loan_amount": 55266.25,
                "min_total_loan_amount": 30490.0,
                "sum_total_loan_amount": 189056.25,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 2
            }
        },
        {
            "2023-10-02": {
                "max_total_loan_amount": 68586.46,
                "min_total_loan_amount": 27160.0,
                "sum_total_loan_amount": 235696.06,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 3
            }
        },
        {
            "2023-10-12": {
                "max_total_loan_amount": 77590.87,
                "min_total_loan_amount": 19170.0,
                "sum_total_loan_amount": 150537.37,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 1
            }
        },
        {
            "2023-10-03": {
                "max_total_loan_amount": 89199.0,
                "min_total_loan_amount": 27625.0,
                "sum_total_loan_amount": 153214.0,
                "tier_1_count": 0,
                "tier_2_count": 1,
                "tier_3_count": 2
            }
        },
        {
            "2023-10-16": {
                "max_total_loan_amount": 38770.0,
                "min_total_loan_amount": 38770.0,
                "sum_total_loan_amount": 38770.0,
                "tier_1_count": 0,
                "tier_2_count": 0,
                "tier_3_count": 1
            }
        },
        {
            "2023-10-13": {
                "max_total_loan_amount": 73184.25,
                "min_total_loan_amount": 20093.0,
                "sum_total_loan_amount": 159862.25,
                "tier_1_count": 0,
                "tier_2_count": 2,
                "tier_3_count": 1
            }
        }
    ]
}
```