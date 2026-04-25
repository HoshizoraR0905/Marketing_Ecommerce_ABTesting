# E-Commerce Marketing A/B Testing and Customer Segment Analysis

## Project Overview

This project analyzes an e-commerce marketing dataset to evaluate the effectiveness of experimental campaign variants. The goal is to build an industry-style analytics workflow rather than a simple notebook-based assignment.

The project currently focuses on three main questions:

1. How should the A/B testing sample unit be defined from event-level data?
2. Do Variant_A and Variant_B improve conversion compared with Control?
3. Do treatment effects differ across customer loyalty tiers and acquisition channels?

## Dataset Structure

The raw data contains multiple related tables: 

A preview of each table can be found in docs/data_samples.md. 

- `customers.csv`: customer profile information, including country, age, gender, loyalty tier, and acquisition channel.
- `events.csv`: event-level customer behavior, including session ID, timestamp, event type, campaign ID, and experiment group.
- `transactions.csv`: purchase transaction records, including revenue, discount, campaign ID, and refund flag.
- `campaigns.csv`: campaign metadata, including channel, objective, target segment, and expected uplift.
- `products.csv`: product catalog information.

The most important table for A/B testing is `events.csv`, because it contains both the experimental assignment variable, `experiment_group`, and behavioral outcomes such as `view`, `click`, `add_to_cart`, `purchase`, and `bounce`.

## Key Data Challenge

A direct customer-level A/B test is not appropriate because the same customer can appear under multiple experiment groups across different sessions or campaigns.

Also, a session may contain multiple event records, and in some cases may include multiple experiment group labels. Therefore, treating raw event rows as independent observations would overcount user activity and bias the analysis.

To address this, I firstly conducted a general A/B test on the dataset before diving into details.

## A/B Testing Definition

For the main A/B test:

- **Treatment variable**: `experiment_group`
  - Control
  - Variant_A
  - Variant_B

- **Sample unit**: one session, assigned by the first eligible treatment exposure.

- **Conversion outcome**: a session is counted as converted if a purchase event occurs within the same session.

## General A/B Test Results

The first-touch A/B test produced the following summary:

| Experiment Group | Sample Size | Conversions | Conversion Rate |
|---|---:|---:|---:|
| Control | 379,714 | 55,882 | 14.72% |
| Variant_A | 127,051 | 19,307 | 15.20% |
| Variant_B | 126,697 | 20,350 | 16.06% |

Both variants improve conversion compared with Control, but Variant_B has the stronger effect.

Approximate lift:

| Comparison | Absolute Lift | Relative Lift |
|---|---:|---:|
| Variant_A vs Control | +0.48 percentage points | +3.3% |
| Variant_B vs Control | +1.34 percentage points | +9.1% |

## Customer Segment Analysis

I also analyzed whether treatment effects differ by customer loyalty tier and acquisition channel.

### Loyalty Tier Findings

Variant_B consistently outperformed Control across all loyalty tiers:

| Loyalty Tier | Variant_B Absolute Lift |
|---|---:|
| Bronze | +1.57 percentage points |
| Silver | +1.56 percentage points |
| Gold | +1.50 percentage points |
| Platinum | +1.62 percentage points |

Variant_A also showed positive lift for Bronze, Silver, and Gold customers, but the effect was smaller. For Platinum customers, Variant_A was not statistically significant.

### Acquisition Channel Findings

Variant_B also showed consistent improvement across acquisition channels:

| Acquisition Channel | Variant_B Absolute Lift |
|---|---:|
| Email | +1.54 percentage points |
| Organic | +1.54 percentage points |
| Paid Search | +1.62 percentage points |
| Referral | +1.53 percentage points |
| Social | +1.53 percentage points |

Variant_A produced smaller improvements across most acquisition channels. Its effect was statistically significant in several channels, but the practical lift was weaker than Variant_B.

## Current Interpretation

The main conclusion so far is:

- Variant_B is the strongest candidate for broader rollout.
- Variant_A improves conversion in many segments, but the effect is modest.
- Variant_B is both statistically significant and practically meaningful across customer loyalty tiers and acquisition channels.
- The treatment effect appears stable across customer-side segments, which supports the robustness of Variant_B.

## Project Structure

```text
Marketing_ECommerce_ABtest/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── data_samples.md
│   ├── null_value_counts.md
│   └── project_Log.md
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── src/
│   ├── inspect_data.py
│   ├── AB_test.py
│   ├── run_AB_general.py
│   ├── run_AB_segments.py
│   └── ...
│
├── README.md
├── requirements.txt
└── .gitignore