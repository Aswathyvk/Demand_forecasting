# Seasonal Demand Forecasting - Quick Start Guide

## What It Does
Predicts product demand considering **seasonal patterns** and **purchasing history** to optimize inventory planning.

## Quick Start (2 minutes)

### 1. Run the Forecaster
```bash
# Navigate to project folder
cd c:\Users\User\PycharmProjects\Demand_forcasting

# Run using virtual environment
venv\Scripts\python.exe seasonal_demand_forecast.py
```

### 2. View Results

**Console Output Shows:**
- ✓ Top 10 products with strongest seasonal patterns
- ✓ Top 15 recommended products (by demand score)
- ✓ Model performance metrics (RMSE, R², MAE)
- ✓ Feature importance ranking

**Generated Files:**
- `seasonal_demand_analysis.png` - 4-panel visualization
- `feature_importance_seasonal.png` - Feature ranking chart

---

## Key Metrics Explained

### Top Product Recommendations (Sorted by Demand Score)

| Column | Meaning |
|--------|---------|
| Product Name | Customer/Product identifier |
| Total Qty | Total units sold |
| Orders | Number of transactions |
| Revenue | Total sales amount |
| Score | 50% quantity + 50% revenue (normalized) |

**Example:** Product "sandra" scored 73.57% based on 66 units sold in 60 orders worth 10,800.

### Model Performance

| Metric | Value | Meaning |
|--------|-------|---------|
| Train RMSE | 14.47 | Training prediction error ~14 units |
| Test RMSE | 13.43 | Test prediction error ~13 units |
| Train R² | 0.6624 | Explains 66.24% of training variance |
| Test R² | 0.5533 | Explains 55.33% of test variance |
| Test MAE | 10.81 | Average error magnitude ~11 units |

**Good if:** Test RMSE lower than train RMSE ✓ (no overfitting)
**Better if:** Test R² > 0.7 (need more data)

---

## Seasonal Patterns in Your Data

### Current Seasons (March 2026 = Summer)
- **Winter** (Dec-Feb): Not in data yet
- **Summer** (Mar-May): ← Current month
- **Monsoon** (Jun-Sep): Not in data yet
- **Post-Monsoon** (Oct-Nov): Not in data yet

### What You'll See
- All products show **Summer** as peak season (because that's when data was collected)
- **Seasonality Strength**: 0% for all products (need multi-month data)

### How to Get Real Seasonal Insights
1. **Wait until December 2026** - You'll have full year of data
2. **Re-run the script** - It will detect true seasonal patterns
3. **Expected results**: Different products peak in different seasons

---

## Using Recommendations for Inventory

### Action Items

**High-Demand Products (Top 5):**
- Keep extra stock during peak seasons
- Maintain higher safety inventory
- Prioritize shelf space

**Example:**
```
Product: sandra
- Demand Score: 73.57% (second highest)
- Average Orders: 60/month
- Action: Keep 120-150 units in stock (considering replenishment lead time)
```

### Seasonal Planning

**When you have 12 months of data:**
1. Identify peak season for each product
2. Increase purchase orders 2-3 months before peak
3. Reduce inventory during off-seasons
4. Plan promotions during shoulder seasons

---

## Understanding the Visualizations

### seasonal_demand_analysis.png

**Panel 1: Product Demand by Season**
- Shows which seasons drive demand for top products
- Taller bars = higher demand in that season
- Use: Plan seasonal promotions

**Panel 2: Monthly Demand Patterns**
- Line chart showing demand trends month-by-month
- Peaks and valleys indicate busy/slow months
- Use: Plan staffing and procurement

**Panel 3: Total Demand by Product**
- Horizontal bar chart ranking products
- Longer bars = more total sales
- Use: Focus on high-demand products

**Panel 4: Order Count by Season**
- How many times products are ordered per season
- Different from Panel 1 (which shows quantities)
- Use: Understand purchase frequency

### feature_importance_seasonal.png

**What it shows:**
- Which input variables most influence demand prediction
- Longer bars = more important

**Current Importance Ranking:**
1. **Frequency** (38.09%) - How often purchased ← Most important
2. **Order Count** (31.90%) - Number of transactions
3. **Type** (30.01%) - Product category
4. **Month/Season** (0%) - Not important yet (need multi-season data)

---

## Data Requirements

### For Better Results

**Current Data:**
- ✓ 939 records (March 2026)
- ✓ 21 unique products
- ✗ Only 1 month (no seasonality yet)

**Improvements Needed:**
- [ ] Collect data for **12+ months**
- [ ] Include all 4 seasons
- [ ] Ensure consistent product naming
- [ ] Validate dates are accurate

### Recommended Collection Period
- **Minimum**: 12 months (1 full year)
- **Better**: 24 months (2 years, capture variations)
- **Best**: 36+ months (3+ years, robust patterns)

---

## Troubleshooting

### Problem: "No module named 'pandas'"
**Solution:** Install packages in venv
```bash
venv\Scripts\python.exe -m pip install pandas numpy scikit-learn matplotlib seaborn
```

### Problem: All seasonal features show 0% importance
**Expected:** With only March data, seasonal features aren't useful
**Solution:** Rerun after collecting 12 months of data

### Problem: Recommendation scores seem wrong
**Check:** 
- Review top 15 products output
- Scores = (normalized quantity × 0.5) + (normalized revenue × 0.5)
- Each product scored relative to others in dataset

---

## Integration with Your App

### Option 1: Command Line
```bash
# Generate report monthly
venv\Scripts\python.exe seasonal_demand_forecast.py
```

### Option 2: Django View
```python
# In forcasting/views.py
from seasonal_demand_forecast import SeasonalDemandForecaster

def seasonal_recommendations(request):
    forecaster = SeasonalDemandForecaster('dataset.csv')
    df = forecaster.load_data()
    df = forecaster.extract_temporal_features(df)
    product_demand = forecaster.aggregate_product_demand(df)
    recommendations, _ = forecaster.get_top_recommendations(product_demand, top_n=10)
    return JsonResponse({'recommendations': recommendations})
```

### Option 3: Scheduled Task
```bash
# Monthly forecast update (Windows Task Scheduler)
Task: Run seasonal_demand_forecast.py every 1st of month
```

---

## Next Steps

1. **Document Current Process**
   - Note when you run forecasts
   - Track which recommendations you implement

2. **Identify Peak Products**
   - Focus inventory investment on top 5 products
   - Monitor if recommendations change monthly

3. **Wait for Seasonal Data**
   - Collect data through December 2026
   - Re-run script to detect seasonal patterns

4. **Optimize Model**
   - If recommendations don't match reality, validate data
   - Consider adding external factors (holidays, weather, promos)

---

## Support

**Documentation:**
- Full guide: `SEASONAL_FORECASTING_README.md`
- Code comments: `seasonal_demand_forecast.py`

**Key Classes:**
```python
SeasonalDemandForecaster(dataset_path)
  ├─ load_data()
  ├─ extract_temporal_features(df)
  ├─ aggregate_product_demand(df)
  ├─ analyze_seasonal_patterns(product_demand)
  ├─ prepare_features_for_modeling(df, product_demand)
  ├─ train_seasonal_model(X, y)
  ├─ get_top_recommendations(df_model, top_n)
  ├─ plot_seasonal_demand_analysis(df_model, top_n)
  └─ generate_forecast_report()
```

---

**Last Updated:** April 4, 2026
