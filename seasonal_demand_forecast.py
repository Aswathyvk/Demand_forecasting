"""
Seasonal Demand Forecasting System
Incorporates seasonal patterns for product-level demand prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


class SeasonalDemandForecaster:
    """
    Advanced demand forecasting with seasonal analysis and product recommendations
    """
    
    def __init__(self, dataset_path='dataset.csv'):
        """Initialize forecaster with dataset"""
        self.df = None
        self.df_processed = None
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.le_dict = {}
        self.dataset_path = dataset_path
        self.seasonal_peaks = {}
        self.product_seasonal_demand = {}
        
    def load_data(self):
        """Load the dataset"""
        print("Loading dataset...")
        self.df = pd.read_csv(self.dataset_path)
        print(f"Dataset loaded with shape: {self.df.shape}")
        return self.df
    
    def extract_temporal_features(self, df):
        """Extract temporal and seasonal features from date column"""
        print("\n=== EXTRACTING TEMPORAL FEATURES ===")
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Extract temporal components
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['quarter'] = df['date'].dt.quarter
        df['day_of_week'] = df['date'].dt.dayofweek  # 0=Monday, 6=Sunday
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['day_of_year'] = df['date'].dt.dayofyear
        
        # Define seasons (India context: Northern Hemisphere)
        def get_season(month):
            if month in [12, 1, 2]:
                return 0  # Winter
            elif month in [3, 4, 5]:
                return 1  # Summer
            elif month in [6, 7, 8, 9]:
                return 2  # Monsoon
            else:
                return 3  # Post-monsoon
        
        df['season'] = df['month'].apply(get_season)
        season_map = {0: 'Winter', 1: 'Summer', 2: 'Monsoon', 3: 'Post-monsoon'}
        df['season_name'] = df['season'].map(season_map)
        
        # Create cyclic features for month (to capture seasonality)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        print("✓ Temporal features extracted:")
        print(f"  - Month, Quarter, Season (Winter/Summer/Monsoon/Post-monsoon)")
        print(f"  - Day of week, Week of year")
        print(f"  - Cyclic month features (sin/cos)")
        
        return df
    
    def aggregate_product_demand(self, df):
        """Aggregate demand by product and temporal period"""
        print("\n=== AGGREGATING PRODUCT DEMAND ===")
        
        # Group by product and temporal features
        product_demand = df.groupby(['pid', 'pname', 'type', 'month', 'season', 'season_name']).agg({
            'quantity': ['sum', 'mean', 'count'],
            'amount': 'sum',
            'date': 'count'
        }).reset_index()
        
        # Flatten column names
        product_demand.columns = ['product_id', 'product_name', 'product_type', 'month', 
                                   'season', 'season_name', 'total_quantity', 'avg_quantity', 
                                   'order_count', 'total_amount', 'frequency']
        
        return product_demand
    
    def analyze_seasonal_patterns(self, product_demand):
        """Analyze which products have seasonal demand patterns"""
        print("\n=== ANALYZING SEASONAL PATTERNS ===")
        
        seasonal_analysis = {}
        
        for product_id in product_demand['product_id'].unique():
            product_data = product_demand[product_demand['product_id'] == product_id]
            
            # Calculate demand by season
            seasonal_demand = product_data.groupby('season_name')['total_quantity'].sum()
            
            if len(seasonal_demand) > 0:
                peak_season = seasonal_demand.idxmax()
                peak_demand = seasonal_demand.max()
                avg_demand = seasonal_demand.mean()
                
                seasonal_analysis[product_id] = {
                    'product_name': product_data['product_name'].iloc[0],
                    'peak_season': peak_season,
                    'peak_demand': peak_demand,
                    'avg_demand': avg_demand,
                    'seasonal_variation': seasonal_demand.to_dict(),
                    'seasonality_strength': (peak_demand - avg_demand) / avg_demand if avg_demand > 0 else 0
                }
        
        self.seasonal_peaks = seasonal_analysis
        
        print("\n✓ Top 10 products with strongest seasonal patterns:")
        sorted_by_seasonality = sorted(seasonal_analysis.items(), 
                                       key=lambda x: x[1]['seasonality_strength'], 
                                       reverse=True)[:10]
        
        for idx, (prod_id, info) in enumerate(sorted_by_seasonality, 1):
            print(f"{idx}. {info['product_name']} (ID: {prod_id})")
            print(f"   Peak Season: {info['peak_season']} | Peak Demand: {info['peak_demand']:.0f} units")
            print(f"   Seasonality Strength: {info['seasonality_strength']:.2%}")
        
        return seasonal_analysis
    
    def prepare_features_for_modeling(self, df, product_demand):
        """Prepare features for seasonal demand regression model"""
        print("\n=== PREPARING FEATURES FOR MODELING ===")
        
        # Use aggregated product demand data
        df_model = product_demand.copy()
        
        # Encode categorical features
        le_type = LabelEncoder()
        le_season = LabelEncoder()
        
        df_model['type_encoded'] = le_type.fit_transform(df_model['product_type'].fillna('unknown'))
        df_model['season_encoded'] = le_season.fit_transform(df_model['season_name'])
        
        # Additional features
        df_model['month_sin'] = np.sin(2 * np.pi * df_model['month'] / 12)
        df_model['month_cos'] = np.cos(2 * np.pi * df_model['month'] / 12)
        
        # Store encoders
        self.le_dict['type'] = le_type
        self.le_dict['season'] = le_season
        
        # Select features
        feature_columns = [
            'type_encoded', 'month', 'season', 'season_encoded',
            'month_sin', 'month_cos', 'order_count', 'frequency'
        ]
        
        X = df_model[feature_columns].fillna(0)
        y = df_model['total_quantity']
        
        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        print(f"Feature columns: {feature_columns}")
        
        return X, y, df_model, feature_columns
    
    def train_seasonal_model(self, X, y):
        """Train Random Forest and Gradient Boosting models for demand forecasting"""
        print("\n=== TRAINING SEASONAL DEMAND MODELS ===")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print(f"Training set size: {X_train.shape[0]}")
        print(f"Test set size: {X_test.shape[0]}")
        
        # Train Random Forest Regressor
        print("\nTraining Random Forest Regressor...")
        rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=12,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        rf_model.fit(X_train, y_train)
        
        # Train Gradient Boosting Regressor
        print("Training Gradient Boosting Regressor...")
        gb_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=5,
            random_state=42
        )
        gb_model.fit(X_train, y_train)
        
        # Predictions
        rf_train_pred = rf_model.predict(X_train)
        rf_test_pred = rf_model.predict(X_test)
        gb_train_pred = gb_model.predict(X_train)
        gb_test_pred = gb_model.predict(X_test)
        
        # Evaluate Random Forest
        print("\n--- RANDOM FOREST PERFORMANCE ---")
        rf_train_rmse = np.sqrt(mean_squared_error(y_train, rf_train_pred))
        rf_test_rmse = np.sqrt(mean_squared_error(y_test, rf_test_pred))
        rf_train_r2 = r2_score(y_train, rf_train_pred)
        rf_test_r2 = r2_score(y_test, rf_test_pred)
        rf_test_mae = mean_absolute_error(y_test, rf_test_pred)
        
        print(f"Train RMSE: {rf_train_rmse:.2f} | Test RMSE: {rf_test_rmse:.2f}")
        print(f"Train R²: {rf_train_r2:.4f} | Test R²: {rf_test_r2:.4f}")
        print(f"Test MAE: {rf_test_mae:.2f}")
        
        # Evaluate Gradient Boosting
        print("\n--- GRADIENT BOOSTING PERFORMANCE ---")
        gb_train_rmse = np.sqrt(mean_squared_error(y_train, gb_train_pred))
        gb_test_rmse = np.sqrt(mean_squared_error(y_test, gb_test_pred))
        gb_train_r2 = r2_score(y_train, gb_train_pred)
        gb_test_r2 = r2_score(y_test, gb_test_pred)
        gb_test_mae = mean_absolute_error(y_test, gb_test_pred)
        
        print(f"Train RMSE: {gb_train_rmse:.2f} | Test RMSE: {gb_test_rmse:.2f}")
        print(f"Train R²: {gb_train_r2:.4f} | Test R²: {gb_test_r2:.4f}")
        print(f"Test MAE: {gb_test_mae:.2f}")
        
        # Select best model
        if rf_test_r2 > gb_test_r2:
            self.model = rf_model
            print("\n✓ Selected: Random Forest (Better R² score)")
        else:
            self.model = gb_model
            print("\n✓ Selected: Gradient Boosting (Better R² score)")
        
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
        return {
            'rf_test_rmse': rf_test_rmse,
            'rf_test_r2': rf_test_r2,
            'gb_test_rmse': gb_test_rmse,
            'gb_test_r2': gb_test_r2,
            'rf_model': rf_model,
            'gb_model': gb_model
        }
    
    def get_top_recommendations(self, df_model, top_n=10):
        """Get top recommended products based on total purchasing and seasonal demand"""
        print("\n=== TOP PRODUCT RECOMMENDATIONS ===\n")
        
        # Calculate total demand by product
        product_totals = df_model.groupby(['product_id', 'product_name']).agg({
            'total_quantity': 'sum',
            'order_count': 'sum',
            'total_amount': 'sum'
        }).reset_index()
        
        product_totals.columns = ['product_id', 'product_name', 'total_quantity', 
                                  'total_orders', 'total_revenue']
        
        # Sort by total quantity and revenue
        product_totals['demand_score'] = (
            product_totals['total_quantity'] / product_totals['total_quantity'].max() * 0.5 +
            product_totals['total_revenue'] / product_totals['total_revenue'].max() * 0.5
        )
        
        top_products = product_totals.nlargest(top_n, 'demand_score')
        
        print(f"{'Rank':<5} {'Product Name':<30} {'Total Qty':<12} {'Orders':<10} {'Revenue':<12} {'Score':<8}")
        print("=" * 80)
        
        recommendations = []
        for idx, (_, row) in enumerate(top_products.iterrows(), 1):
            print(f"{idx:<5} {row['product_name']:<30} {row['total_quantity']:<12.0f} "
                  f"{row['total_orders']:<10.0f} {row['total_revenue']:<12.0f} {row['demand_score']:<8.2%}")
            
            prod_id = row['product_id']
            if prod_id in self.seasonal_peaks:
                seasonal_info = self.seasonal_peaks[prod_id]
                recommendations.append({
                    'product_id': prod_id,
                    'product_name': row['product_name'],
                    'total_quantity': row['total_quantity'],
                    'total_orders': row['total_orders'],
                    'total_revenue': row['total_revenue'],
                    'demand_score': row['demand_score'],
                    'peak_season': seasonal_info['peak_season'],
                    'peak_demand': seasonal_info['peak_demand'],
                    'seasonality_strength': seasonal_info['seasonality_strength']
                })
        
        return recommendations, product_totals
    
    def forecast_next_season_demand(self, df_model, current_date=None, top_n=10):
        """
        Predict most demanded products for the next season
        Based on historical seasonal patterns and current date
        """
        print("\n=== FORECASTING NEXT SEASON'S MOST DEMANDED PRODUCTS ===\n")
        
        if current_date is None:
            current_date = datetime.now()
        else:
            current_date = pd.to_datetime(current_date)
        
        current_month = current_date.month
        
        # Define seasons
        def get_season_number(month):
            if month in [12, 1, 2]:
                return 0  # Winter
            elif month in [3, 4, 5]:
                return 1  # Summer
            elif month in [6, 7, 8, 9]:
                return 2  # Monsoon
            else:
                return 3  # Post-monsoon
        
        season_names = {0: 'Winter', 1: 'Summer', 2: 'Monsoon', 3: 'Post-monsoon'}
        current_season = get_season_number(current_month)
        next_season = (current_season + 1) % 4
        next_season_name = season_names[next_season]
        
        print(f"Current Date: {current_date.strftime('%B %d, %Y')}")
        print(f"Current Season: {season_names[current_season]}")
        print(f"Next Season: {next_season_name}\n")
        
        # Get products with data for the next season
        next_season_data = df_model[df_model['season'] == next_season]
        
        if len(next_season_data) == 0:
            print(f"⚠️  No historical data for {next_season_name} season found.")
            print("Using overall demand patterns instead...\n")
            next_season_data = df_model
        
        # Calculate seasonal demand score for products
        product_next_season = next_season_data.groupby(['product_id', 'product_name']).agg({
            'total_quantity': 'sum',
            'order_count': 'sum',
            'total_amount': 'sum'
        }).reset_index()
        
        product_next_season.columns = ['product_id', 'product_name', 'seasonal_quantity',
                                       'seasonal_orders', 'seasonal_revenue']
        
        # Get historical seasonal patterns
        overall_stats = df_model.groupby('product_id').agg({
            'total_quantity': 'sum',
            'order_count': 'sum',
            'total_amount': 'sum'
        }).reset_index()
        overall_stats.columns = ['product_id', 'total_quantity', 'total_orders', 'total_revenue']
        
        # Merge with seasonal data
        product_next_season = product_next_season.merge(overall_stats, on='product_id', how='left')
        
        # Calculate next season demand score
        # Combines seasonal demand, historical total demand, and seasonal share
        product_next_season['seasonal_share'] = (
            product_next_season['seasonal_quantity'] / product_next_season['total_quantity'] 
        ).fillna(0)
        
        product_next_season['forecast_score'] = (
            product_next_season['seasonal_quantity'] / product_next_season['seasonal_quantity'].max() * 0.5 +
            product_next_season['seasonal_share'] * 0.3 +
            product_next_season['total_quantity'] / product_next_season['total_quantity'].max() * 0.2
        )
        
        # Get top products for next season
        top_next_season = product_next_season.nlargest(top_n, 'forecast_score')
        
        print(f"{'Rank':<5} {'Product Name':<30} {'Next Season Qty':<18} {'Historical Total':<16} {'Forecast Score':<15}")
        print("=" * 90)
        
        forecast_results = []
        for idx, (_, row) in enumerate(top_next_season.iterrows(), 1):
            print(f"{idx:<5} {row['product_name']:<30} {row['seasonal_quantity']:<18.0f} "
                  f"{row['total_quantity']:<16.0f} {row['forecast_score']:<15.2%}")
            
            # Get seasonal information
            prod_id = row['product_id']
            seasonal_info = self.seasonal_peaks.get(
                prod_id, 
                {'peak_season': next_season_name, 'seasonality_strength': 0}
            )
            
            forecast_results.append({
                'rank': idx,
                'product_id': int(prod_id),
                'product_name': row['product_name'],
                'next_season': next_season_name,
                'forecasted_quantity': row['seasonal_quantity'],
                'historical_total_quantity': row['total_quantity'],
                'forecasted_orders': row['seasonal_orders'],
                'forecast_score': row['forecast_score'],
                'seasonal_share': row['seasonal_share'],
                'peak_season': seasonal_info.get('peak_season', next_season_name),
                'seasonality_strength': seasonal_info.get('seasonality_strength', 0)
            })
        
        return forecast_results, next_season_name
    
    def plot_seasonal_demand_analysis(self, df_model, top_n=5):
        """Visualize seasonal demand patterns for top products"""
        print("\n=== GENERATING SEASONAL DEMAND VISUALIZATIONS ===")
        
        # Get top products
        top_products = df_model.groupby('product_name')['total_quantity'].sum().nlargest(top_n).index
        df_top = df_model[df_model['product_name'].isin(top_products)]
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Seasonal demand by season
        seasonal_data = df_top.groupby(['season_name', 'product_name'])['total_quantity'].sum().unstack()
        seasonal_data.plot(kind='bar', ax=axes[0, 0], color='steelblue')
        axes[0, 0].set_title('Product Demand by Season', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Total Quantity')
        axes[0, 0].set_xlabel('Season')
        axes[0, 0].legend(title='Product', fontsize=8)
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Plot 2: Monthly demand patterns
        monthly_data = df_top.groupby(['month', 'product_name'])['total_quantity'].sum().unstack()
        monthly_data.plot(kind='line', ax=axes[0, 1], marker='o')
        axes[0, 1].set_title('Product Demand by Month', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Total Quantity')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].legend(title='Product', fontsize=8)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Total demand by product
        product_totals = df_top.groupby('product_name')['total_quantity'].sum().sort_values(ascending=False)
        axes[1, 0].barh(product_totals.index, product_totals.values, color='coral')
        axes[1, 0].set_title('Total Demand by Product', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Total Quantity')
        
        # Plot 4: Order count by season
        order_data = df_top.groupby(['season_name', 'product_name'])['order_count'].sum().unstack()
        order_data.plot(kind='bar', ax=axes[1, 1], color='lightgreen')
        axes[1, 1].set_title('Order Count by Season', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Order Count')
        axes[1, 1].set_xlabel('Season')
        axes[1, 1].legend(title='Product', fontsize=8)
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('seasonal_demand_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Seasonal demand analysis saved to 'seasonal_demand_analysis.png'")
        plt.close()
    
    def plot_feature_importance(self, feature_columns):
        """Plot feature importance from trained model"""
        if self.model is None:
            print("Model not trained yet!")
            return
        
        print("\nGenerating feature importance plot...")
        
        importances = self.model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'feature': feature_columns,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        print("\n--- FEATURE IMPORTANCE ---")
        print(feature_importance_df.to_string(index=False))
        
        plt.figure(figsize=(10, 6))
        plt.barh(feature_importance_df['feature'], feature_importance_df['importance'], color='steelblue')
        plt.xlabel('Importance Score')
        plt.title('Feature Importance in Seasonal Demand Forecasting Model')
        plt.tight_layout()
        plt.savefig('feature_importance_seasonal.png', dpi=300, bbox_inches='tight')
        print("\n✓ Feature importance plot saved to 'feature_importance_seasonal.png'")
        plt.close()
    
    def generate_forecast_report(self):
        """Generate comprehensive forecasting report"""
        print("\n" + "="*80)
        print("SEASONAL DEMAND FORECASTING REPORT")
        print("="*80)
        
        report = {
            'total_products': len(self.seasonal_peaks),
            'seasonal_peaks': self.seasonal_peaks,
            'model_type': type(self.model).__name__,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        print(f"Report Generated: {report['timestamp']}")
        print(f"Total Products Analyzed: {report['total_products']}")
        print(f"Model Type: {report['model_type']}")
        
        return report


def main():
    """Main execution pipeline"""
    print("\n" + "="*80)
    print("SEASONAL DEMAND FORECASTING SYSTEM")
    print("="*80)
    
    # Initialize forecaster
    forecaster = SeasonalDemandForecaster('dataset.csv')
    
    # Load and preprocess data
    df = forecaster.load_data()
    df = forecaster.extract_temporal_features(df)
    
    # Aggregate and analyze
    product_demand = forecaster.aggregate_product_demand(df)
    seasonal_analysis = forecaster.analyze_seasonal_patterns(product_demand)
    
    # Prepare and train model
    X, y, df_model, feature_columns = forecaster.prepare_features_for_modeling(df, product_demand)
    model_results = forecaster.train_seasonal_model(X, y)
    
    # Get recommendations for current analysis
    recommendations, product_totals = forecaster.get_top_recommendations(df_model, top_n=15)
    
    # Forecast next season's demand (April 4, 2026 → predicts Summer 2026)
    next_season_forecast, next_season_name = forecaster.forecast_next_season_demand(
        df_model, 
        current_date='2026-04-04', 
        top_n=15
    )
    
    # Generate visualizations
    forecaster.plot_seasonal_demand_analysis(df_model, top_n=5)
    forecaster.plot_feature_importance(feature_columns)
    
    # Generate report
    report = forecaster.generate_forecast_report()
    
    print("\n" + "="*80)
    print("✓ FORECASTING COMPLETE")
    print("="*80)
    print("\nGenerated Files:")
    print("  - seasonal_demand_analysis.png")
    print("  - feature_importance_seasonal.png")
    
    return forecaster, recommendations, next_season_forecast, report


if __name__ == "__main__":
    forecaster, recommendations, next_season_forecast, report = main()
