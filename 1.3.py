import pulp
import pandas as pd

# Load production data
product_df = pd.read_csv('/Users/vishalravikumar/Desktop/DS_Final_Prod/data/production_planning.product.csv')
resource_df = pd.read_csv('/Users/vishalravikumar/Desktop/DS_Final_Prod/data/production_planning.resource.csv')

# Define products based on the columns
products = ['P1', 'P2', 'P3', 'P4', 'P5']

# Extract parameters from the product data
parameter_values = product_df.set_index('parameter').T
D = parameter_values.loc[:, 'Demand'].tolist()
C = parameter_values.loc[:, 'ProductionCost'].tolist()
P = parameter_values.loc[:, 'PurchasePrice'].tolist()
m = parameter_values.loc[:, 'MachiningTime'].tolist()
a = parameter_values.loc[:, 'AssemblyTime'].tolist()
f = parameter_values.loc[:, 'FinishingTime'].tolist()

# Extract resource data
Tm = resource_df.loc[resource_df['Resource'] == 'MachiningTime', 'Available_Hours'].values[0] * 60
Ta = resource_df.loc[resource_df['Resource'] == 'AssemblyTime', 'Available_Hours'].values[0] * 60
Tf = resource_df.loc[resource_df['Resource'] == 'FinishingTime', 'Available_Hours'].values[0] * 60

# Initialize the LP problem
prob = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision variables for in-house and outsourced production
x = pulp.LpVariable.dicts("Inhouse_Production", products, lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("Outsourced", products, lowBound=0, cat='Integer')

# Objective function: Minimize the total cost
prob += pulp.lpSum([C[i] * x[products[i]] + P[i] * y[products[i]] for i in range(len(products))]), "Total Cost"

# Demand constraints: Total production must meet or exceed demand
for i in range(len(products)):
    prob += x[products[i]] + y[products[i]] >= D[i], f"Demand_{products[i]}"

# Resource constraints: Machining, assembly, and finishing time constraints
prob += pulp.lpSum([m[i] * x[products[i]] for i in range(len(products))]) <= Tm, "Machining_Time"
prob += pulp.lpSum([a[i] * x[products[i]] for i in range(len(products))]) <= Ta, "Assembly_Time"
prob += pulp.lpSum([f[i] * x[products[i]] for i in range(len(products))]) <= Tf, "Finishing_Time"

# Solve the LP problem
prob.solve()

# Output results
print(f"Status: {pulp.LpStatus[prob.status]}")

# Minimum cost attainable
min_cost = pulp.value(prob.objective)
print(f"Minimum cost attainable: ${min_cost:.0f}")

# Optimal production plan (in-house and outsourced)
print("\nOptimal production plan (round quantities to the nearest integer):")
print(f"{'Product':<15}{'In-house':<15}{'Outsourced':<15}")
for product in products:
    print(f"{product:<15}{x[product].varValue:<15}{y[product].varValue:<15}")

# Resource usage
used_machining = sum([m[i] * x[products[i]].varValue for i in range(len(products))])
used_assembly = sum([a[i] * x[products[i]].varValue for i in range(len(products))])
used_finishing = sum([f[i] * x[products[i]].varValue for i in range(len(products))])

print("\nResources:")
print(f"{'Resource':<20}{'Used (minutes)':<20}{'Available (minutes)':<20}")
print(f"{'Machining Time':<20}{used_machining:<20}{Tm:<20}")
print(f"{'Assembly Time':<20}{used_assembly:<20}{Ta:<20}")
print(f"{'Finishing Time':<20}{used_finishing:<20}{Tf:<20}")