# Project Log

# Goal
Explore an e-commerce marketing dataset with statistical methods. At minimum, I want to conduct an A/B testing analysis, evaluate campaign effectiveness, and practice applying machine learning methods to a business-style dataset.

A secondary goal of this project is to practice building a more industry-style analytics project. My previous academic and class projects were often organized around a single notebook or script. 

## 2026-04-24

### Work completed

- Set up an industry-style project structure, including separate folders for raw data, processed data, source code, and documentation.
- Inspected the raw datasets to understand their shapes, columns, and basic quality issues.
- Built and saved an initial rough preprocessed analysis table: `customer_campaign_analysis.csv`. 
- `converted` is defined as whether a purchase has been made for the `session_id`. 
- Prepared the project for version control and excluded large data files from GitHub using `.gitignore`. 

## 2026-04-25 

### Issues
- The dataset contains both `experiment_group` and `campaign_id`, which represent different concepts. `experiment_group` has values as Control, Variant_A, or Variant_B, while `campaign_id` identifies the marketing campaign context. 

Same `customer_id` can appear under multiple experiment groups across different events or campaigns. Therefore, the customer is not a clean unit of random assignment. If we aggregate only at the customer level, we may mix different treatments and outcomes for the same customer. 

Distinct `customer_id`, `experiment_group` pair also contains different `converted` values. 

This suggests that we should consider `converted` (transaction made within the event time) for each distinct `event_id`. 

The processed .csv I created yesterday cannot be used. I need a new .csv with event_id, timestamp. 

But how do I define if each tx(transaction) is caused by treatment? The events table contains `campaign_id`, `time_stamp`, `experiment_group`, should I filter those transactions made within a period after `time_stamp` in event? 

- AB testing conducted on conversion rate of 2 days after each event timestamp. 
- With z-stats being 11.78 and 34.50, p-value being 4e-32 and 7e-261, both Variant_A and Variant_B are statistically significant compared to control group. 

### Continue on project
- Re-defined `converted` using `event_type` = `purchase` for each distinct pair of `session_id`, `experiment_group`. 
- It is so confused how to define sample size, treatment group size, and control group size. Each `user_id` in each `session_id` can even be exposed to different `experiment_group`. 
- Latest version group by `session_id`, and leave the first `experiment_group`. 

### A/B test results:
          comparison  n_control  n_treatment  x_control  x_treatment  p_control  p_treatment  absolute_lift  relative_lift    z_stat      p_value   ci_low  ci_high
Variant_A vs Control     379714       127051      55882        19307   0.147169     0.151963       0.004794       0.032574  4.161093 3.167287e-05 0.002521 0.007067
Variant_B vs Control     379714       126697      55882        20350   0.147169     0.160619       0.013451       0.091397 11.593565 4.442506e-31 0.011136 0.015765

### Continue on segment A/B testing
- Now I want to see if user loyalty and acquisition level are related to conversion rates. 
- `session_id` doesn't match to a unique `customer_id`. 
- Run AB testing on each segment, variant vs control. In most cases treatment group do have statistical significant improvement in coversion rate compared to control group. 