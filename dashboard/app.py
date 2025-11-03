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

# 🏗️ App setup
app = Dash(__name__)
server = app.server
app.title = "Indian E-Commerce Dashboard"

# 📊 Layout
app.layout = html.Div([
    html.H1("🇮🇳 Indian E-Commerce Dashboard (Diwali Sales)"),

    # 🔽 Dropdown
    html.Div(className="dropdown-container", children=[
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': s, 'value': s} for s in sorted(df['state'].unique())],
            placeholder="Select a State",
            style={'width': '60%', 'margin': 'auto'}
        )
    ]),

    # 💎 KPI Cards (IDs added)
    html.Div(className="KPI-container", children=[
        html.Div(className="card", children=[
            html.H3("💰 Total Sales"),
            html.P(id='total-sales', children="₹0")
        ]),
        html.Div(className="card", children=[
            html.H3("👥 Total Customers"),
            html.P(id='total-customers', children="0")
        ]),
        html.Div(className="card", children=[
            html.H3("🛒 Total Orders"),
            html.P(id='total-orders', children="0")
        ]),
    ]),

    # 📈 Graphs
    html.Div([
        dcc.Graph(id='sales-category-graph'),
        dcc.Graph(id='sales-age-graph'),
        dcc.Graph(id='sales-zone-graph'),
    ])
])

# 🎯 Callback for KPIs + Graphs
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
    # ✅ Filter data
    filtered_df = df[df['state'] == selected_state] if selected_state else df

    # ✅ KPIs (fixed user_id column)
    total_sales = filtered_df['amount'].sum()
    total_customers = filtered_df['user_id'].nunique()
    total_orders = len(filtered_df)

    # ✅ 1️⃣ Category Sales
    category_sales = filtered_df.groupby('product_category')['amount'].sum().reset_index()
    fig_category = px.bar(
        category_sales,
        x='product_category',
        y='amount',
        title="Top Product Categories",
        color='amount',
        color_continuous_scale='Blues'
    )

    # ✅ 2️⃣ Age Sales
    age_sales = filtered_df.groupby('age_group')['amount'].sum().reset_index()
    fig_age = px.bar(
        age_sales,
        x='age_group',
        y='amount',
        title="Sales by Age Group",
        color='amount',
        color_continuous_scale='Greens'
    )

    # ✅ 3️⃣ Zone Sales
    zone_sales = filtered_df.groupby('zone')['amount'].sum().reset_index()
    fig_zone = px.bar(
        zone_sales,
        x='zone',
        y='amount',
        title="Sales by Zone",
        color='amount',
        color_continuous_scale='Oranges'
    )

    # 🪄 Format KPI display values
    return (
        f"₹{total_sales:,.0f}",
        f"{total_customers:,}",
        f"{total_orders:,}",
        fig_category,
        fig_age,
        fig_zone
    )

if __name__ == '__main__':
    app.run(debug=True)











      


