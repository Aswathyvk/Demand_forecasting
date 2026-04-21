"""
Next Season Demand Forecasting
Predicts the most demanded products for the upcoming season based on historical patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from seasonal_demand_forecast import SeasonalDemandForecaster
import json


def get_next_season_products(dataset_path='dataset.csv', current_date=None, top_n=10, save_report=True):
    """
    Predict most demanded products for the next season
    
    Args:
        dataset_path (str): Path to the dataset CSV
        current_date (str): Current date in 'YYYY-MM-DD' format. If None, uses today's date
        top_n (int): Number of top products to return
        save_report (bool): Whether to save results to JSON file
    
    Returns:
        dict: Contains forecast results and metadata
    """
    
    print("\n" + "="*100)
    print("NEXT SEASON DEMAND FORECAST")
    print("="*100)
    
    if current_date is None:
        current_date = datetime.now()
    else:
        current_date = pd.to_datetime(current_date)
    
    # Initialize forecaster
    print("\n[1/5] Loading and processing data...")
    forecaster = SeasonalDemandForecaster(dataset_path)
    
    df = forecaster.load_data()
    df = forecaster.extract_temporal_features(df)
    
    # Aggregate and analyze
    print("[2/5] Analyzing seasonal patterns...")
    product_demand = forecaster.aggregate_product_demand(df)
    seasonal_analysis = forecaster.analyze_seasonal_patterns(product_demand)
    
    # Prepare and train model
    print("[3/5] Training predictive model...")
    X, y, df_model, feature_columns = forecaster.prepare_features_for_modeling(df, product_demand)
    model_results = forecaster.train_seasonal_model(X, y)
    
    # Forecast next season
    print("[4/5] Forecasting next season's demand...")
    next_season_forecast, next_season_name = forecaster.forecast_next_season_demand(
        df_model,
        current_date=current_date,
        top_n=top_n
    )
    
    # Prepare results
    print("[5/5] Preparing forecast report...")
    
    current_month = current_date.month
    
    # Determine season
    if current_month in [12, 1, 2]:
        current_season = 'Winter'
    elif current_month in [3, 4, 5]:
        current_season = 'Summer'
    elif current_month in [6, 7, 8, 9]:
        current_season = 'Monsoon'
    else:
        current_season = 'Post-monsoon'
    
    results = {
        'forecast_date': current_date.strftime('%Y-%m-%d'),
        'current_season': current_season,
        'next_season': next_season_name,
        'forecast_generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_products_analyzed': len(seasonal_analysis),
        'top_products_count': len(next_season_forecast),
        'top_products': [
            {
                'rank': item['rank'],
                'product_id': item['product_id'],
                'product_name': item['product_name'],
                'forecast_score': f"{item['forecast_score']:.2%}",
                'forecasted_quantity': int(item['forecasted_quantity']),
                'forecasted_orders': int(item['forecasted_orders']),
                'seasonal_share': f"{item['seasonal_share']:.2%}",
                'historical_total_quantity': int(item['historical_total_quantity']),
                'seasonality_strength': f"{item['seasonality_strength']:.2%}",
                'confidence': classify_confidence(item['seasonality_strength'], item['seasonal_share'])
            }
            for item in next_season_forecast
        ]
    }
    
    # Print summary
    print("\n" + "="*100)
    print("FORECAST SUMMARY")
    print("="*100)
    print(f"\nForecast Date: {results['forecast_date']}")
    print(f"Current Season: {results['current_season']}")
    print(f"Next Season: {results['next_season']}")
    print(f"Total Products Analyzed: {results['total_products_analyzed']}")
    print(f"\nTop {len(results['top_products'])} Most Demanded Products for {results['next_season']}:\n")
    
    print(f"{'Rank':<6} {'Product Name':<30} {'Forecast Score':<16} {'Est. Quantity':<15} {'Confidence':<12}")
    print("-" * 90)
    
    for item in results['top_products']:
        print(f"{item['rank']:<6} {item['product_name']:<30} {item['forecast_score']:<16} "
              f"{item['forecasted_quantity']:<15} {item['confidence']:<12}")
    
    # Save report to JSON
    if save_report:
        report_filename = f"next_season_forecast_{current_date.strftime('%Y%m%d')}.json"
        with open(report_filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n✓ Report saved to '{report_filename}'")
    
    print("\n" + "="*100)
    
    return results


def classify_confidence(seasonality_strength, seasonal_share):
    """Classify forecast confidence level"""
    if seasonality_strength > 0.5 and seasonal_share > 0.3:
        return "High"
    elif seasonality_strength > 0.2 and seasonal_share > 0.15:
        return "Medium"
    else:
        return "Low"


def get_product_supply_recommendations(forecast_results, safety_margin=1.2):
    """
    Generate supply chain recommendations based on forecast
    
    Args:
        forecast_results (dict): Results from get_next_season_products()
        safety_margin (float): Safety factor for stocking (default: 1.2 = 20% extra)
    
    Returns:
        dict: Supply recommendations for each product
    """
    print("\n" + "="*100)
    print("SUPPLY CHAIN RECOMMENDATIONS")
    print("="*100 + "\n")
    
    recommendations = []
    
    for item in forecast_results['top_products']:
        forecasted_qty = int(item['forecasted_quantity'])
        recommended_qty = int(forecasted_qty * safety_margin)
        safety_stock = recommended_qty - forecasted_qty
        
        priority = "URGENT" if item['confidence'] == "High" else "NORMAL" if item['confidence'] == "Medium" else "LOW"
        
        recommendation = {
            'product_id': item['product_id'],
            'product_name': item['product_name'],
            'forecasted_quantity': forecasted_qty,
            'recommended_stock': recommended_qty,
            'safety_stock': safety_stock,
            'priority': priority,
            'reason': f"Expected {forecasted_qty} units for {forecast_results['next_season']} with {item['confidence']} confidence"
        }
        recommendations.append(recommendation)
        
        print(f"Product: {item['product_name']}")
        print(f"  Forecast: {forecasted_qty} units")
        print(f"  Recommended Stock: {recommended_qty} units (with {int((safety_margin-1)*100)}% safety margin)")
        print(f"  Safety Stock: {safety_stock} units")
        print(f"  Priority: {priority}")
        print()
    
    return recommendations


if __name__ == "__main__":
    # Get forecast for next season (as of April 4, 2026)
    forecast_results = get_next_season_products(
        dataset_path='dataset.csv',
        current_date='2026-04-04',
        top_n=15,
        save_report=True
    )
    
    # Get supply chain recommendations
    supply_recommendations = get_product_supply_recommendations(forecast_results, safety_margin=1.2)
    
    print("\n✓ Forecast completed successfully!")
