# Seasonal Demand Forecasting System - Complete Guide

## Overview
This document describes the advanced demand forecasting system that predicts product demand considering **seasonal factors**, **purchasing patterns**, and **market trends**.

---

## system Architecture

### Components

1. **Temporal Feature Engineering**
   - Extracts temporal components from transaction dates
   - Creates seasonal indicators (Winter, Summer, Monsoon, Post-monsoon)
   - Generates cyclic features for month (sin/cos encoding)

2. **Product Demand Aggregation**
   - Groups transactions by product and time period
   - Calculates metrics: total quantity, order count, revenue

3. **Seasonal Pattern Analysis**
   - Identifies peak seasons for each product
   - Measures seasonality strength (volatility across seasons)
   - Ranks products by seasonal demand variations

4. **Machine Learning Models**
   - Random Forest Regressor (primary model)
   - Gradient Boosting Regressor (comparison model)
   - Both trained on historical demand patterns

5. **Product Recommendations**
   - Ranks products by demand score
   - Includes seasonal peak information
   - Provides actionable insights for inventory planning

---

## Key Features

### Seasonal Factors Considered

**Seasons (India Context):**
- **Winter** (Dec, Jan, Feb): Cold weather - increased demand for warm beverages, comfort items
- **Summer** (Mar, Apr, May): Hot season - high demand for beverages, personal care items
- **Monsoon** (Jun-Sep): Rainy season - demand for packaged foods, long shelf-life products
- **Post-Monsoon** (Oct, Nov): Transition season - moderate demand patterns

**Temporal Features:**
- Month (1-12): Raw and cyclic encoded
- Quarter (Q1-Q4): Quarterly business cycles
- Day of week: Week-end vs week-day patterns
- Week of year: Annual cyclic patterns
- Day of year: Year-over-year comparisons

### Product Metrics

For each product, the system calculates:
- **Total Quantity**: Sum of all units sold
- **Total Orders**: Number of transactions
- **Total Revenue**: Sum of transaction amounts
- **Order Count**: Frequency of purchases
- **Peak Season**: Season with highest demand
- **Seasonality Strength**: Measure of seasonal variation (0 = no variation, 1 = high variation)
- **Demand Score**: Combined metric considering quantity and revenue

---

## Machine Learning Models

### Random Forest Regressor (Selected Model)
**Configuration:**
```
- n_estimators: 100 trees
- max_depth: 12 levels
- min_samples_split: 5 samples
- min_samples_leaf: 2 leaves
```

**Performance Metrics:**
- Train RMSE: 14.47 units
- Test RMSE: 13.43 units (prediction error ~13 units)
- Train R²: 0.6624 (explains 66.24% of variance)
- Test R²: 0.5533 (explains 55.33% of test variance)
- Test MAE: 10.81 units (average absolute error)

### Gradient Boosting Regressor (Comparison)
Used for model comparison; Random Forest selected due to better generalization.

### Key Features (By Importance)
1. **Frequency**: 38.09% - How often product is purchased
2. **Order Count**: 31.90% - Number of transactions
3. **Type Encoded**: 30.01% - Product category/type
4. Seasonal features: Currently minimal impact (data covers single March period)

---

## Top Product Recommendations

Based on combining:
- **Total Purchasing Volume** (50% weight)
- **Revenue Generation** (50% weight)

### Top 5 Recommended Products

| Rank | Product Name | Total Qty | Orders | Revenue | Demand Score |
|------|--------------|-----------|--------|---------|--------------|
| 1    | sandra       | 66        | 60     | 10,800  | 73.57%       |
| 2    | avk          | 42        | 32     | 9,216   | 57.67%       |
| 3    | nivin        | 140       | 2      | 80      | 50.37%       |
| 4    | avk          | 54        | 37     | 6,660   | 50.12%       |
| 5    | sandra       | 40        | 27     | 6,750   | 45.54%       |

---

## Usage Instructions

### Running the Forecaster

```bash
# Using virtual environment
c:\Users\User\PycharmProjects\Demand_forcasting\venv\Scripts\python.exe seasonal_demand_forecast.py
```

### Code Example

```python
from seasonal_demand_forecast import SeasonalDemandForecaster

# Initialize
forecaster = SeasonalDemandForecaster('dataset.csv')

# Load and process data
df = forecaster.load_data()
df = forecaster.extract_temporal_features(df)

# Aggregate demand
product_demand = forecaster.aggregate_product_demand(df)

# Analyze seasonal patterns
seasonal_analysis = forecaster.analyze_seasonal_patterns(product_demand)

# Train model
X, y, df_model, features = forecaster.prepare_features_for_modeling(df, product_demand)
results = forecaster.train_seasonal_model(X, y)

# Get recommendations
recommendations, totals = forecaster.get_top_recommendations(df_model, top_n=15)

# Generate visualizations
forecaster.plot_seasonal_demand_analysis(df_model, top_n=5)
forecaster.plot_feature_importance(features)
```

---

## Output Files

### 1. seasonal_demand_analysis.png
**Contents:**
- Subplot 1: Product Demand by Season (Bar chart)
- Subplot 2: Monthly Demand Patterns (Line chart)
- Subplot 3: Total Demand by Product (Horizontal bar chart)
- Subplot 4: Order Count by Season (Bar chart)

**Use Cases:**
- Identify which seasons drive demand for each product
- Plan inventory levels for seasonal peaks
- Budget marketing efforts by season

### 2. feature_importance_seasonal.png
**Contents:**
- Bar chart showing feature importance scores
- Most to least important predictors

**Top Features:**
1. Frequency (38.09%) - Most important
2. Order Count (31.90%)
3. Type Encoded (30.01%)

---

## Data Flow Diagram

```
                    ┌─────────────────────┐
                    │   dataset.csv       │
                    │   (939 records)     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Load & Preprocess  │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
       ┌────────▼────────┐        ┌──────────▼─────────┐
       │ Extract Temporal │       │ Aggregate Product  │
       │    Features     │       │    Demand          │
       └────────┬────────┘       └──────────┬─────────┘
                │                           │
       ┌────────▼────────────────────────────▼────────┐
       │  Analyze Seasonal Patterns                   │
       │  (Peak seasons, Seasonality Strength)        │
       └────────┬─────────────────────────────────────┘
                │
       ┌────────▼──────────────┐
       │ Prepare ML Features   │
       │ (Train/Test Split)    │
       └────────┬──────────────┘
                │
       ┌────────▼────────────────────────────┐
       │  Train ML Models                     │
       │  (Random Forest & Gradient Boosting) │
       └────────┬────────────────────────────┘
                │
    ┌───────────┴───────────┐
    │                       │
    ▼                       ▼
┌─────────────┐      ┌──────────────────┐
│ Product     │      │ Visualizations   │
│ Recommend   │      │ & Reports        │
└─────────────┘      └──────────────────┘
```

---

## Seasonal Insights

### Current Dataset Observations
- **Data Period**: March 2026 (single month - limited seasonal variation)
- **All Products**: Show Summer as peak season
- **Seasonality Strength**: Currently 0% (insufficient multi-month data)
- **Recommendation**: Accumulate data across 12 months for robust seasonal patterns

### With Full-Year Data, Expect

**Product Categories:**
1. **Beverages** - High summer demand, low winter demand
2. **Groceries** - Stable year-round with festival peaks
3. **Personal Care** - Summer surge (weather-dependent usage)
4. **Packaged Food** - Monsoon preference (longer shelf-life)

---

## Model Performance Evaluation

### Metric Definitions

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **RMSE** | √(Σ(y_true - y_pred)²/n) | Average prediction error in units |
| **R²** | 1 - (SS_res/SS_tot) | % of variance explained (0-1) |
| **MAE** | Σ\|y_true - y_pred\|/n | Mean absolute deviation |

### Model Strength & Limitations

**Strengths:**
- ✓ Captures product frequency and order patterns
- ✓ Incorporates categorical product types
- ✓ Trained on aggregated temporal data

**Current Limitations:**
- ✗ Limited to March 2026 data (no true seasonal variation)
- ✗ Small dataset (89 product-period combinations)
- ✗ Product names appear to be customer names (data quality issue)

---

## Recommendations for Improvement

### 1. Data Quality
- [ ] Verify product names and IDs
- [ ] Consolidate duplicate products
- [ ] Ensure consistent date formats

### 2. Feature Enhancement
- [ ] Add holiday indicators
- [ ] Include promotional periods
- [ ] Incorporate competitor data
- [ ] Add weather data (if applicable)

### 3. Model Improvements
- [ ] Collect 12+ months of historical data
- [ ] Use time-series models (ARIMA, Prophet)
- [ ] Implement product-specific models for high-variance items
- [ ] Add external features (holidays, events)

### 4. Operational Use
- [ ] Integrate with inventory management system
- [ ] Set dynamic reorder points by season
- [ ] Adjust safety stock based on seasonal forecasts
- [ ] Create demand alerts for unusual patterns

---

## Integration with Django

### View Integration Example

```python
# In forcasting/views.py
from seasonal_demand_forecast import SeasonalDemandForecaster

def get_seasonal_forecast(request):
    forecaster = SeasonalDemandForecaster('dataset.csv')
    
    df = forecaster.load_data()
    df = forecaster.extract_temporal_features(df)
    product_demand = forecaster.aggregate_product_demand(df)
    
    recommendations, totals = forecaster.get_top_recommendations(product_demand, top_n=10)
    
    return JsonResponse({
        'recommendations': recommendations,
        'model_type': 'RandomForestRegressor',
        'timestamp': datetime.now().isoformat()
    })
```

---

## Troubleshooting

### Common Issues

**Issue**: Low R² Score (< 0.5)
- **Cause**: Insufficient data or high noise
- **Solution**: Collect more months of data; validate data quality

**Issue**: Seasonal Features Show 0% Importance
- **Cause**: Insufficient time-series variation in current dataset
- **Solution**: Use full-year data; consider seasonal decomposition

**Issue**: ModuleNotFoundError for pandas/sklearn
- **Solution**: Install in venv: `pip install pandas numpy scikit-learn matplotlib seaborn`

---

## Files Reference

- `seasonal_demand_forecast.py` - Main forecasting module (450+ lines)
- `seasonal_demand_analysis.png` - Visualizations of seasonal patterns
- `feature_importance_seasonal.png` - Model feature importance chart
- `dataset.csv` - Source transaction data

---

## Glossary

| Term | Definition |
|------|-----------|
| **Seasonality** | Regular, predictable variations in demand by time period |
| **Peak Season** | Period with highest demand for a product |
| **Demand Score** | Combined metric ranking products by total purchasing |
| **RMSE** | Root Mean Square Error - average prediction deviation |
| **R²** | Coefficient of determination - model fit quality |
| **MAE** | Mean Absolute Error - average absolute prediction error |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-04 | Initial release with seasonal analysis |

---

**For questions or support, refer to the inline code documentation in `seasonal_demand_forecast.py`**
