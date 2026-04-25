# Project Log

# Goal
Explore an e-commerce marketing dataset with statistical methods. At minimum, I want to conduct an A/B testing analysis, evaluate campaign effectiveness, and practice applying machine learning methods to a business-style dataset.

A secondary goal of this project is to practice building a more industry-style analytics project. My previous academic and class projects were often organized around a single notebook or script. 

## 2026-04-24

### Work completed

- Set up an industry-style project structure, including separate folders for raw data, processed data, source code, and documentation.
- Inspected the raw datasets to understand their shapes, columns, and basic quality issues.
- Built and saved an initial rough preprocessed analysis table: `customer_campaign_analysis.csv`. Distinct id is `customer_id`, `campaign_id` pair. `converted` is defined as whether a transaction has been made for this distinct_id. 
- Prepared the project for version control and excluded large data files from GitHub using `.gitignore`. 

## 2026-04-25 

### Issues
- The dataset contains both `experiment_group` and `campaign_id`, which represent different concepts. `experiment_group` has values as Control, Variant_A, or Variant_B, while `campaign_id` identifies the marketing campaign context. 

Same `customer_id` can appear under multiple experiment groups across different events or campaigns. Therefore, the customer is not a clean unit of random assignment. If we aggregate only at the customer level, we may mix different treatments and outcomes for the same customer. 

Distinct `customer_id`, `experiment_group` pair also contains different `converted` values. 

This suggests that we should consider `converted` (transaction made within the event time) for each distinct `event_id`. 

The processed .csv I created yesterday cannot be used. I need a new .csv with event_id, timestamp. 

But how do I define if each tx(transaction) is caused by treatment? The events table contains `campaign_id`, `time_stamp`, `experiment_group`, should I filter those transactions made within a period after `time_stamp` in event? 

### Work completed
- AB testing conducted on conversion rate of 2 days after each event timestamp. 
- With z-stats being 11.78 and 34.50, p-value being 4e-32 and 7e-261, both Variant_A and Variant_B are statistically significant compared to control group. 