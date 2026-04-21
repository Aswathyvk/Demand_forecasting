import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')


def load_and_preprocess_data():
    """Load and preprocess dataset"""
    df = pd.read_csv('dataset.csv')
    print("Dataset shape:", df.shape)
    print("\nFirst few rows:")
    print(df.head())
    return df


def prepare_features_targets(df):
    """Prepare features and targets for model training"""
    
    # Find most recommended products (top products by quantity purchased)
    product_purchases = df.groupby('pid')['quantity'].sum().reset_index()
    product_purchases.columns = ['pid', 'total_quantity']
    product_purchases = product_purchases.sort_values('total_quantity', ascending=False)
    
    print("\n=== TOP 10 MOST RECOMMENDED PRODUCTS ===")
    print(product_purchases.head(10))
    
    # Get top 5 products for binary classification (recommended vs not recommended)
    top_products = product_purchases.head(5)['pid'].values
    
    # Create target: 1 if product is in top 5, 0 otherwise
    df['is_recommended'] = df['pid'].isin(top_products).astype(int)
    
    # Prepare features
    # Encode categorical variables
    le_type = LabelEncoder()
    le_customer_type = LabelEncoder()
    le_status = LabelEncoder()
    le_payment = LabelEncoder()
    
    df['type_encoded'] = le_type.fit_transform(df['type'].fillna('unknown'))
    df['customer_type_encoded'] = le_customer_type.fit_transform(df['pcustomer_type'].fillna('unknown'))
    df['status_encoded'] = le_status.fit_transform(df['status'].fillna('unknown'))
    df['payment_mode_encoded'] = le_payment.fit_transform(df['payment_mode'].fillna('unknown'))
    
    # Select features for prediction
    feature_columns = [
        'quantity',
        'type_encoded',
        'customer_type_encoded',
        'amount',
        'status_encoded',
        'payment_mode_encoded'
    ]
    
    # Handle missing values
    for col in feature_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    X = df[feature_columns]
    y = df['is_recommended']
    
    print(f"\n=== FEATURES & TARGET ===")
    print(f"Features shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts()}")
    print(f"\nRecommended products: {top_products}")
    
    return X, y, df, top_products


def train_model(X, y):
    """Train Random Forest model"""
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n=== TRAINING DATA ===")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    return model, X_train, X_test, y_train, y_test, y_train_pred, y_test_pred


def evaluate_model(y_train, y_test, y_train_pred, y_test_pred):
    """Evaluate model performance"""
    
    print("\n" + "="*60)
    print("MODEL EVALUATION METRICS")
    print("="*60)
    
    # Training metrics
    train_accuracy = accuracy_score(y_train, y_train_pred)
    train_precision = precision_score(y_train, y_train_pred, zero_division=0)
    train_recall = recall_score(y_train, y_train_pred, zero_division=0)
    
    print("\n--- TRAINING METRICS ---")
    print(f"Accuracy:  {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"Precision: {train_precision:.4f}")
    print(f"Recall:    {train_recall:.4f}")
    
    # Testing metrics
    test_accuracy = accuracy_score(y_test, y_test_pred)
    test_precision = precision_score(y_test, y_test_pred, zero_division=0)
    test_recall = recall_score(y_test, y_test_pred, zero_division=0)
    
    print("\n--- TESTING METRICS ---")
    print(f"Accuracy:  {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"Precision: {test_precision:.4f}")
    print(f"Recall:    {test_recall:.4f}")
    
    # Confusion Matrix
    cm_train = confusion_matrix(y_train, y_train_pred)
    cm_test = confusion_matrix(y_test, y_test_pred)
    
    print("\n--- CONFUSION MATRIX (TRAINING) ---")
    print(cm_train)
    print(f"TN: {cm_train[0,0]}, FP: {cm_train[0,1]}")
    print(f"FN: {cm_train[1,0]}, TP: {cm_train[1,1]}")
    
    print("\n--- CONFUSION MATRIX (TESTING) ---")
    print(cm_test)
    print(f"TN: {cm_test[0,0]}, FP: {cm_test[0,1]}")
    print(f"FN: {cm_test[1,0]}, TP: {cm_test[1,1]}")
    
    print("\n--- CLASSIFICATION REPORT (TESTING) ---")
    print(classification_report(y_test, y_test_pred, target_names=['Not Recommended', 'Recommended']))
    
    return cm_train, cm_test


def plot_confusion_matrices(cm_train, cm_test):
    """Plot confusion matrices"""
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Training confusion matrix
    sns.heatmap(cm_train, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Not Recommended', 'Recommended'],
                yticklabels=['Not Recommended', 'Recommended'])
    axes[0].set_title('Confusion Matrix - Training Data')
    axes[0].set_ylabel('True Label')
    axes[0].set_xlabel('Predicted Label')
    
    # Testing confusion matrix
    sns.heatmap(cm_test, annot=True, fmt='d', cmap='Greens', ax=axes[1],
                xticklabels=['Not Recommended', 'Recommended'],
                yticklabels=['Not Recommended', 'Recommended'])
    axes[1].set_title('Confusion Matrix - Testing Data')
    axes[1].set_ylabel('True Label')
    axes[1].set_xlabel('Predicted Label')
    
    plt.tight_layout()
    plt.savefig('confusion_matrices.png', dpi=100, bbox_inches='tight')
    print("\n✓ Confusion matrices saved as 'confusion_matrices.png'")
    plt.close()


def plot_feature_importance(model, feature_columns):
    """Plot feature importance"""
    
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n--- FEATURE IMPORTANCE ---")
    print(feature_importance)
    
    plt.figure(figsize=(10, 6))
    plt.barh(feature_importance['feature'], feature_importance['importance'], color='steelblue')
    plt.xlabel('Importance')
    plt.title('Feature Importance in Product Recommendation Model')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=100, bbox_inches='tight')
    print("\n✓ Feature importance plot saved as 'feature_importance.png'")
    plt.close()


def predict_recommendations(model, X, df, top_products, feature_columns):
    """Get product recommendations based on model"""
    
    predictions = model.predict_proba(X)[:, 1]  # Probability of being recommended
    
    df_with_predictions = df[['id', 'pid', 'title', 'cid', 'pname']].copy()
    df_with_predictions['recommendation_score'] = predictions
    df_with_predictions['is_recommended'] = (predictions > 0.5).astype(int)
    
    # Top recommended products
    top_recommended = df_with_predictions[df_with_predictions['is_recommended'] == 1].groupby('pid').size().sort_values(ascending=False).head(10)
    
    print("\n=== TOP 10 RECOMMENDED PRODUCTS (By Model) ===")
    print(top_recommended)
    
    return df_with_predictions


def main():
    """Main execution"""
    
    print("="*60)
    print("PRODUCT RECOMMENDATION SYSTEM")
    print("="*60)
    
    # Load data
    df = load_and_preprocess_data()
    
    # Prepare features and targets
    X, y, df, top_products = prepare_features_targets(df)
    
    # Train model
    model, X_train, X_test, y_train, y_test, y_train_pred, y_test_pred = train_model(X, y)
    
    # Evaluate model
    cm_train, cm_test = evaluate_model(y_train, y_test, y_train_pred, y_test_pred)
    
    # Visualizations
    feature_columns = [
        'quantity', 'type_encoded', 'customer_type_encoded',
        'amount', 'status_encoded', 'payment_mode_encoded'
    ]
    plot_confusion_matrices(cm_train, cm_test)
    plot_feature_importance(model, feature_columns)
    
    # Get recommendations
    recommendations = predict_recommendations(model, X, df, top_products, feature_columns)
    
    print("\n" + "="*60)
    print("✓ ANALYSIS COMPLETE!")
    print("="*60)
    print("Files generated:")
    print("  - confusion_matrices.png")
    print("  - feature_importance.png")


if __name__ == '__main__':
    main()
