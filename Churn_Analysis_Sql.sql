-- 04_business_insights.sql
USE customer_churn;

-- 1. Revenue at risk: monthly charges associated with customers who churned.
SELECT ROUND(SUM(Monthly_Charges), 2) AS churned_customer_monthly_revenue
FROM churn_customers
WHERE Churn = 'Yes';

-- 2. Churn rate by tenure band
SELECT
    Tenure_Group,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * SUM(Churn_Flag) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM churn_customers
GROUP BY Tenure_Group
ORDER BY MIN(Tenure_Months);

-- 3. High monthly charge customers (top quartile) and churn
WITH charge_threshold AS (
    SELECT
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Monthly_Charges) AS p75_charge
    FROM churn_customers
    WHERE Monthly_Charges IS NOT NULL
)
SELECT
    CASE WHEN c.Monthly_Charges >= t.p75_charge THEN 'Top quartile charges'
         ELSE 'Below top quartile' END AS charge_segment,
    COUNT(*) AS customers,
    SUM(c.Churn_Flag) AS churned_customers,
    ROUND(100.0 * SUM(c.Churn_Flag) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM churn_customers c
CROSS JOIN charge_threshold t
GROUP BY charge_segment;

-- 4. Churn and support availability (association, not causation)
SELECT
    Tech_Support,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * SUM(Churn_Flag) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM churn_customers
GROUP BY Tech_Support;
-- 4. Churn and support availability (association, not causation)
SELECT
    Tech_Support,
    COUNT(*) AS customers,
    SUM(Churn_Flag) AS churned_customers,
    ROUND(100.0 * SUM(Churn_Flag) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM churn_customers
GROUP BY Tech_Support;
