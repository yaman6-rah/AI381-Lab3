# Model Selection

## The question

The model predicts whether a telecom customer is likely to churn (leave the service). A false negative may cause the company to miss an opportunity to retain a customer, while a false positive may waste retention resources on a customer who was not going to leave.

## Candidates

| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---:|---:|---:|---:|---:|---|
| Logistic Regression | Simple, fast, and provides a baseline | 0.7982 | 0.4948 | 0.2500 | 3.2676 | 3.5479 | `bf3dad072cdd48e2b6899fc657f5eb18` |
| Random Forest | To capture nonlinear patterns and feature interactions | 0.7589 | 0.4536 | 0.2222 | 9.2573 | 3160.1270 | `eb210c7754ec4d73a439f231bef3f0ac` |
| Gradient Boosting | To test a boosting-based alternative | 0.7476 | 0.4167 | 0.2222 | 2.7423 | 141.6758 | `e0ccae843a6947ccbb7fc263095507ca` |

## The champion

I selected **Logistic Regression** as the champion.

It achieved the highest AUC (0.7982) and F1 score (0.4948) among the three candidates. Its p95 latency was only 3.2676 ms, well below the 20 ms latency budget, and its model size was very small (3.5479 KB).

I accepted its weak performance on some customer slices. Its lowest slice F1 was 0.2500, particularly for customers with one-year and two-year contracts. Random Forest and Gradient Boosting did not provide better overall results.

## My promotion rules

- **Latency budget (p95): 20 ms**, because the prediction API should respond quickly enough for practical use. This is a project target, and latency should be measured again on the actual deployment hardware.
- **Minimum gain to replace the champion (F1 points): 0.02**, meaning a candidate must improve F1 by at least two absolute percentage points. This avoids replacing the champion for a very small improvement.

## What I would check next

I would investigate performance across customer segments, especially one-year and two-year contract customers. Their low F1 scores may indicate that the model does not identify churn patterns equally well across all groups. I would also monitor changes in customer behavior and data over time.

