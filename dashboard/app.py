import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# 🟢 Load Data
DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/processed/cleaned_diwali_sales_processed.csv')
print(f"🟢 Looking for file at: {DATA_PATH}")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    print("✅ File loaded successfully!")
else:
    raise FileNotFoundError(f"❌ File not found at: {DATA_PATH}")

# 🧹 Data cleaning
df.columns = df.columns.str.strip()
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df.dropna(subset=['amount'], inplace=True)

# 🧮 KPIs
total_sales = df['amount'].sum()
total_customers = df['user_id'].nunique()
total_orders = df['orders'].astype(float).sum()

# 🏗️ App setup
app = Dash(__name__)
server=app.server
app.title = "Indian E-Commerce Dashboard"

# 📊 Layout
app.layout = html.Div([
    html.H1("🇮🇳 Indian E-Commerce Dashboard (Diwali Sales)"),

    html.Div(className="dropdown-container", children=[
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': s, 'value': s} for s in sorted(df['state'].unique())],
            placeholder="Select a State",
            style={'width': '60%', 'margin': 'auto'}
        )
    ]),

    # KPI Cards
    html.Div(className="KPI-container", children=[
        html.Div(className="card", children=[
            html.H3("💰 Total Sales"),
            html.P(f"₹{total_sales:,.0f}")
        ]),
        html.Div(className="card", children=[
            html.H3("👥 Total Customers"),
            html.P(f"{total_customers:,}")
        ]),
        html.Div(className="card", children=[
            html.H3("🛒 Total Orders"),
            html.P(f"{int(total_orders):,}")
        ]),
    ]),

    # Graphs Section
    html.Div([
        dcc.Graph(id='sales-category-graph'),
        dcc.Graph(id='sales-age-graph'),
        dcc.Graph(id='sales-zone-graph'),
    ])
])

# 🎯 Callbacks for interactive charts
# 🎯 Callbacks for interactive charts + KPIs
@app.callback(
    [Output('total-sales', 'children'),
     Output('total-customers', 'children'),
     Output('total-orders', 'children'),
     Output('sales-category-graph', 'figure'),
     Output('sales-age-graph', 'figure'),
     Output('sales-zone-graph', 'figure')],
    [Input('state-dropdown', 'value')]
)
def update_dashboard(selected_state):
    # ✅ Filter data based on dropdown selection
    filtered_df = df[df['state'] == selected_state] if selected_state else df

    # ✅ Update KPI values dynamically
    total_sales = filtered_df['amount'].sum()
    total_customers = filtered_df['customer_id'].nunique()
    total_orders = len(filtered_df)

    # ✅ 1️⃣ Total Sales by Product Category
    category_sales = filtered_df.groupby('product_category')['amount'].sum().sort_values(ascending=False).head(10)
    fig_category = px.bar(
        category_sales,
        x=category_sales.index,
        y=category_sales.values,
        labels={'x': 'Product Category', 'y': 'Total Sales'},
        title=f"Top 10 Product Categories {'in ' + selected_state if selected_state else ''}",
        color=category_sales.values,
        color_continuous_scale='Blues'
    )

    # ✅ 2️⃣ Sales by Age Group
    age_sales = filtered_df.groupby('age_group')['amount'].sum().sort_values(ascending=False)
    fig_age = px.bar(
        age_sales,
        x=age_sales.index,
        y=age_sales.values,
        labels={'x': 'Age Group', 'y': 'Total Sales'},
        title=f"Sales by Age Group {'in ' + selected_state if selected_state else ''}",
        color=age_sales.values,
        color_continuous_scale='Greens'
    )

    # ✅ 3️⃣ Sales by Zone
    zone_sales = filtered_df.groupby('zone')['amount'].sum().sort_values(ascending=False)
    fig_zone = px.bar(
        zone_sales,
        x=zone_sales.index,
        y=zone_sales.values,
        labels={'x': 'Zone', 'y': 'Total Sales'},
        title=f"Sales by Zone {'in ' + selected_state if selected_state else ''}",
        color=zone_sales.values,
        color_continuous_scale='Oranges'
    )

    return total_sales, total_customers, total_orders, fig_category, fig_age, fig_zone

if __name__ == '__main__':
    app.run(debug=True)










      


