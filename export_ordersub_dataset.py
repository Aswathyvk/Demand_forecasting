import csv
import os
import django
import sys

# Add the project directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Demand_forcasting.settings')
django.setup()

from forcasting.models import ordersub


def create_ordersub_dataset():
    """Export ordersub data with all related information"""
    combined_data = []
    
    # Get all ordersub records with related data
    ordersub_records = ordersub.objects.all().select_related('PRODUCT', 'ORDER', 'ORDER__CUSTOMER', 'ORDER__RETAILER')
    
    for i in ordersub_records:
        combined_data.append({
            # ordersub fields
            'id': i.id,
            'quantity': i.quantity,
            
            # product fields
            'title': i.PRODUCT.title,
            'pid': i.PRODUCT.id,
            'type': i.PRODUCT.type,
            'description': i.PRODUCT.description,
            'image': i.PRODUCT.image,
            'brand_name': i.PRODUCT.brand_name,
            'amount': i.PRODUCT.amount,
            
            # order fields
            'date': i.ORDER.date,
            'status': i.ORDER.status,
            'payment_mode': i.ORDER.payment_mode,
            
            # customer fields
            'cid': i.ORDER.CUSTOMER.id,
            'pname': i.ORDER.CUSTOMER.name,
            'pemail': i.ORDER.CUSTOMER.email,
            'pphone': i.ORDER.CUSTOMER.phone,
            'pplace': i.ORDER.CUSTOMER.place,
            'ppost': i.ORDER.CUSTOMER.post,
            'ppin': i.ORDER.CUSTOMER.pin,
            'pcustomer_type': i.ORDER.CUSTOMER.type,
            
            # retailer fields
            'retailer_name': i.ORDER.RETAILER.name,
            'retailer_email': i.ORDER.RETAILER.email,
            'retailer_phone': i.ORDER.RETAILER.phone,
            'retailer_place': i.ORDER.RETAILER.place,
            'retailer_post': i.ORDER.RETAILER.post,
            'retailer_pin': i.ORDER.RETAILER.pin,
        })
    
    if combined_data:
        # Define column order
        columns = [
            'id', 'quantity',
            'title', 'pid', 'type', 'description', 'image', 'brand_name', 'amount',
            'date', 'status', 'payment_mode',
            'cid', 'pname', 'pemail', 'pphone', 'pplace', 'ppost', 'ppin', 'pcustomer_type',
            'retailer_name', 'retailer_email', 'retailer_phone', 'retailer_place', 'retailer_post', 'retailer_pin'
        ]
        
        filepath = 'dataset.csv'
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(combined_data)
        
        print(f'✓ Data exported successfully!')
        print(f'✓ Total records: {len(combined_data)}')
        print(f'✓ Dataset saved as: {filepath}')
    else:
        print('⚠ No ordersub data found')


if __name__ == '__main__':
    create_ordersub_dataset()
