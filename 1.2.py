import pandas as pd

# Load production data
product_df = pd.read_csv('/Users/vishalravikumar/Desktop/DS_Final_Prod/data/production_planning.product.csv')
resource_df = pd.read_csv('/Users/vishalravikumar/Desktop/DS_Final_Prod/data/production_planning.resource.csv')

# Display product data
print("Product Data:")
print(product_df)

# Display resource data
print("\nResource Data:")
print(resource_df)
