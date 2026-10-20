# ADK Evaluation Workflow

This demo uses:

- 'Eval' folder as the project root.
- evalset created in ADK Web UI and saved under `finance_assistant/`
- eval config saved under `finance_assistant/`

## 1. Setup Environment

Create virtual env and install necessary dependencies.
pip install google-adk[eval]

Ensure credentials are set in:

- `finance_assistant/.env`

## 2. (Optional) Create/Update Evalset in ADK Web UI

From project root `Eval`:

```
adk web
```

In the Web UI:

1. Select app `finance_assistant`.
2. Create/update your evalset.
3. Save evalset file in `finance_assistant/`.

## 2.1 Web UI Prompt Script (for building evalset)

Use these prompts to build `metrics_demo_evalset_v1` in ADK Web UI.

| Tool                          | Scenario Type | Eval Case ID                 | Prompt                                                                                                              |
| ----------------------------- | ------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `calculate_compound_interest` | Happy         | `ci_happy_annual_10y`        | If I invest $15,000 at 0.07 annual interest for 10 years, how much will I have and how much interest will I earn?   |
| `calculate_compound_interest` | Negative      | `ci_negative_invalid_rate`   | If I invest $10,000 at an annual rate of 1.2 (120%) for 5 years, what will I get?                                   |
| `calculate_loan_payment`      | Happy         | `lp_happy_mortgage_30y`      | For a $300,000 loan at 0.045 annual rate over 30 years, what is my monthly payment, total paid, and total interest? |
| `calculate_loan_payment`      | Negative      | `lp_negative_invalid_term`   | For a $120,000 loan at 0.06 annual rate over 0 years, what is the payment?                                          |
| `calculate_monthly_savings`   | Happy         | `ms_happy_goal_50k_3y`       | How much should I save monthly to reach $50,000 in 3 years at 0.05 annual return?                                   |
| `calculate_monthly_savings`   | Negative      | `ms_negative_invalid_target` | How much should I save monthly to reach $0 in 4 years at 0.05 annual return?                                        |

## 3. Create custom test config

Check the sample `test_config.json` file provided under `finance_assistant`

## 4. Run ADK Eval CLI on Evalset

From your project root 'Eval' run the ADK evaluation

### adk eval finance_assistant ./finance_assistant/metrics_demo_evalset_v1.evalset.json --config_file_path ./finance_assistant/test_config.json --print_detailed_results

## 5. Render HTML Report

From `Eval` folder run the Python reporting script

### python ./scripts/render_eval_results_html.py ./finance_assistant/.adk/eval_history/\*.evalset_result.json --config ./finance_assistant/test_config.json --output ./reports/eval_results_report.html

Open in the web browser:

`reports/eval_results_report.html`

Note: You can verify the EvalSet Pydantic class from the official documentation of ADK from the following source:
https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py
