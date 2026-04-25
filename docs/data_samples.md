## campaigns.csv

|    |   campaign_id | channel     | objective    | start_date   | end_date   | target_segment   |   expected_uplift |
|---:|--------------:|:------------|:-------------|:-------------|:-----------|:-----------------|------------------:|
|  0 |             1 | Paid Search | Cross-sell   | 2021-10-25   | 2021-11-26 | Deal Seekers     |             0.022 |
|  1 |             2 | Email       | Retention    | 2021-10-24   | 2021-12-24 | Deal Seekers     |             0.116 |
|  2 |             3 | Email       | Reactivation | 2023-10-08   | 2023-11-30 | Churn Risk       |             0.1   |
|  3 |             4 | Display     | Reactivation | 2022-07-25   | 2022-10-07 | Deal Seekers     |             0.111 |
|  4 |             5 | Social      | Acquisition  | 2022-07-09   | 2022-09-29 | New Customers    |             0.144 |

## customers.csv

|    |   customer_id | signup_date   | country   |   age | gender   | loyalty_tier   | acquisition_channel   |
|---:|--------------:|:--------------|:----------|------:|:---------|:---------------|:----------------------|
|  0 |             1 | 2021-04-08    | BR        |    48 | Male     | Bronze         | Referral              |
|  1 |             2 | 2023-04-28    | IN        |    36 | Female   | Silver         | Organic               |
|  2 |             3 | 2022-12-18    | UK        |    35 | Female   | Silver         | Organic               |
|  3 |             4 | 2022-04-26    | US        |    45 | Male     | Silver         | Paid Search           |
|  4 |             5 | 2022-04-20    | IN        |    53 | Male     | Silver         | Organic               |

## events.csv

|    |   event_id | timestamp           |   customer_id |   session_id | event_type   |   product_id | device_type   | traffic_source   |   campaign_id | page_category   |   session_duration_sec | experiment_group   |
|---:|-----------:|:--------------------|--------------:|-------------:|:-------------|-------------:|:--------------|:-----------------|--------------:|:----------------|-----------------------:|:-------------------|
|  0 |          1 | 2021-01-14 13:35:43 |         43812 |       535101 | view         |         1004 | desktop       | Email            |            43 | PLP             |                  115.1 | Control            |
|  1 |          2 | 2021-12-03 21:36:50 |         71340 |        96426 | add_to_cart  |          986 | desktop       | Email            |            10 | PDP             |                   32.4 | Variant_A          |
|  2 |          3 | 2021-12-27 08:25:15 |         59540 |       220126 | purchase     |         1630 | mobile        | Organic          |             0 | PDP             |                  190.7 | Variant_A          |
|  3 |          4 | 2022-01-22 15:06:54 |          3601 |       484555 | add_to_cart  |         1532 | desktop       | Paid Search      |            30 | Checkout        |                  134.8 | Variant_B          |
|  4 |          5 | 2021-05-10 12:03:09 |         92735 |        60646 | bounce       |          nan | desktop       | Email            |            26 | PLP             |                   53.1 | Variant_A          |

## products.csv

|    |   product_id | category    | brand    |   base_price | launch_date   |   is_premium |
|---:|-------------:|:------------|:---------|-------------:|:--------------|-------------:|
|  0 |            1 | Grocery     | Brand_58 |        14.19 | 2021-08-02    |            0 |
|  1 |            2 | Fashion     | Brand_1  |        25.8  | 2021-09-14    |            0 |
|  2 |            3 | Electronics | Brand_70 |       165.46 | 2021-01-18    |            1 |
|  3 |            4 | Fashion     | Brand_56 |        75.45 | 2023-03-03    |            1 |
|  4 |            5 | Sports      | Brand_1  |        72.5  | 2022-04-19    |            1 |

## transactions.csv

|    |   transaction_id | timestamp           |   customer_id |   product_id |   quantity |   discount_applied |   gross_revenue |   campaign_id |   refund_flag |
|---:|-----------------:|:--------------------|--------------:|-------------:|-----------:|-------------------:|----------------:|--------------:|--------------:|
|  0 |                1 | 2021-12-27 08:25:15 |         59540 |         1630 |          3 |               0    |           43.74 |             0 |             0 |
|  1 |                2 | 2023-06-06 21:14:26 |         54871 |         1901 |          3 |               0    |          174.78 |            21 |             0 |
|  2 |                3 | 2023-08-31 05:29:54 |         51818 |         1884 |          1 |               0    |           40.61 |            37 |             0 |
|  3 |                4 | 2022-06-26 20:33:46 |         18164 |         1114 |          2 |               0.15 |           68.76 |            13 |             0 |
|  4 |                5 | 2023-07-26 18:12:35 |         86915 |          408 |          1 |               0    |           14.64 |             4 |             0 |

