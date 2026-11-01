# Data Quality Report

**Shape:** 9,994 rows × 21 columns

**Column data types:**
- Row ID: int64
- Order ID: str
- Order Date: str
- Ship Date: str
- Ship Mode: str
- Customer ID: str
- Customer Name: str
- Segment: str
- Country: str
- City: str
- State: str
- Postal Code: int64
- Region: str
- Product ID: str
- Category: str
- Sub-Category: str
- Product Name: str
- Sales: float64
- Quantity: int64
- Discount: float64
- Profit: float64

**Missing values per column:**


**Duplicate rows:** 0

**Summary statistics (numeric columns):**
|        |   Row ID | Order ID       | Order Date   | Ship Date   | Ship Mode      | Customer ID   | Customer Name   | Segment   | Country       | City          | State      |   Postal Code | Region   | Product ID      | Category        | Sub-Category   | Product Name    |     Sales |   Quantity |    Discount |      Profit |
|:-------|---------:|:---------------|:-------------|:------------|:---------------|:--------------|:----------------|:----------|:--------------|:--------------|:-----------|--------------:|:---------|:----------------|:----------------|:---------------|:----------------|----------:|-----------:|------------:|------------:|
| count  |  9994    | 9994           | 9994         | 9994        | 9994           | 9994          | 9994            | 9994      | 9994          | 9994          | 9994       |        9994   | 9994     | 9994            | 9994            | 9994           | 9994            |  9994     | 9994       | 9994        |  9994       |
| unique |   nan    | 5009           | 1237         | 1334        | 4              | 793           | 793             | 3         | 1             | 531           | 49         |         nan   | 4        | 1862            | 3               | 17             | 1850            |   nan     |  nan       |  nan        |   nan       |
| top    |   nan    | CA-2017-100111 | 5/9/2016     | 16/12/2015  | Standard Class | WB-21850      | William Brown   | Consumer  | United States | New York City | California |         nan   | West     | OFF-PA-10001970 | Office Supplies | Binders        | Staple envelope |   nan     |  nan       |  nan        |   nan       |
| freq   |   nan    | 14             | 38           | 35          | 5968           | 37            | 37              | 5191      | 9994          | 915           | 2001       |         nan   | 3203     | 19              | 6026            | 1523           | 48              |   nan     |  nan       |  nan        |   nan       |
| mean   |  4997.5  | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |       55190.4 | nan      | nan             | nan             | nan            | nan             |   229.858 |    3.78957 |    0.156203 |    28.6569  |
| std    |  2885.16 | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |       32063.7 | nan      | nan             | nan             | nan            | nan             |   623.245 |    2.22511 |    0.206452 |   234.26    |
| min    |     1    | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |        1040   | nan      | nan             | nan             | nan            | nan             |     0.444 |    1       |    0        | -6599.98    |
| 25%    |  2499.25 | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |       23223   | nan      | nan             | nan             | nan            | nan             |    17.28  |    2       |    0        |     1.72875 |
| 50%    |  4997.5  | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |       56430.5 | nan      | nan             | nan             | nan            | nan             |    54.49  |    3       |    0.2      |     8.6665  |
| 75%    |  7495.75 | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |       90008   | nan      | nan             | nan             | nan            | nan             |   209.94  |    5       |    0.2      |    29.364   |
| max    |  9994    | nan            | nan          | nan         | nan            | nan           | nan             | nan       | nan           | nan           | nan        |       99301   | nan      | nan             | nan             | nan            | nan             | 22638.5   |   14       |    0.8      |  8399.98    |


---


*First 5 rows preview (displayed in console when script runs):*