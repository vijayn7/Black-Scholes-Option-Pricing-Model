from flask import Flask, render_template, request, jsonify
import numpy as np
import plotly
import plotly.graph_objects as go
import json
from black_scholes import BlackScholes

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page with the input form."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate option prices and Greeks based on user input."""
    # Get user inputs
    S0 = float(request.form.get('stock_price', 100))
    K = float(request.form.get('strike_price', 100))
    r = float(request.form.get('interest_rate', 0.05)) / 100  # Convert from percent
    T = float(request.form.get('maturity', 1.0))
    sigma = float(request.form.get('volatility', 0.2)) / 100  # Convert from percent

    # Calculate option prices
    call_price = BlackScholes.call_price(S0, K, r, T, sigma)
    put_price = BlackScholes.put_price(S0, K, r, T, sigma)
    
    # Calculate Greeks
    delta_call = BlackScholes.delta_call(S0, K, r, T, sigma)
    delta_put = BlackScholes.delta_put(S0, K, r, T, sigma)
    gamma = BlackScholes.gamma(S0, K, r, T, sigma)
    vega = BlackScholes.vega(S0, K, r, T, sigma)
    theta_call = BlackScholes.theta_call(S0, K, r, T, sigma)
    theta_put = BlackScholes.theta_put(S0, K, r, T, sigma)
    rho_call = BlackScholes.rho_call(S0, K, r, T, sigma)
    rho_put = BlackScholes.rho_put(S0, K, r, T, sigma)
    
    # Generate chart data
    stock_price_chart = generate_price_vs_stock_chart(S0, K, r, T, sigma)
    volatility_chart = generate_price_vs_volatility_chart(S0, K, r, T, sigma)
    greeks_chart = generate_greeks_chart(S0, K, r, T, sigma)
    
    return render_template('results.html',
                          stock_price=S0,
                          strike_price=K,
                          interest_rate=r*100,  # Convert to percentage
                          maturity=T,
                          volatility=sigma*100,  # Convert to percentage
                          call_price=call_price,
                          put_price=put_price,
                          delta_call=delta_call,
                          delta_put=delta_put,
                          gamma=gamma,
                          vega=vega,
                          theta_call=theta_call,
                          theta_put=theta_put,
                          rho_call=rho_call,
                          rho_put=rho_put,
                          stock_price_chart=stock_price_chart,
                          volatility_chart=volatility_chart,
                          greeks_chart=greeks_chart)

def generate_price_vs_stock_chart(S0, K, r, T, sigma):
    """Generate JSON for stock price vs option price chart."""
    S_values = np.linspace(K/2, K*1.5, 100)
    call_prices = [BlackScholes.call_price(S, K, r, T, sigma) for S in S_values]
    put_prices = [BlackScholes.put_price(S, K, r, T, sigma) for S in S_values]
    
    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_values, y=call_prices, mode='lines', name='Call Option', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=S_values, y=put_prices, mode='lines', name='Put Option', line=dict(color='red')))
    
    fig.add_shape(
        type="line",
        x0=K, y0=0, x1=K, y1=max(np.max(call_prices), np.max(put_prices)),
        line=dict(color="black", width=1, dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=S0, y0=0, x1=S0, y1=max(np.max(call_prices), np.max(put_prices)),
        line=dict(color="orange", width=1, dash="dash")
    )
    
    fig.update_layout(
        title='Option Prices vs Stock Price',
        xaxis_title='Stock Price ($)',
        yaxis_title='Option Price ($)',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        hovermode="x unified"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def generate_price_vs_volatility_chart(S0, K, r, T, sigma):
    """Generate JSON for volatility vs option price chart."""
    sigma_values = np.linspace(0.01, 0.5, 100)
    call_prices = [BlackScholes.call_price(S0, K, r, T, vol) for vol in sigma_values]
    put_prices = [BlackScholes.put_price(S0, K, r, T, vol) for vol in sigma_values]
    
    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sigma_values*100, y=call_prices, mode='lines', name='Call Option', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=sigma_values*100, y=put_prices, mode='lines', name='Put Option', line=dict(color='red')))
    
    fig.add_shape(
        type="line",
        x0=sigma*100, y0=0, x1=sigma*100, y1=max(np.max(call_prices), np.max(put_prices)),
        line=dict(color="black", width=1, dash="dash")
    )
    
    fig.update_layout(
        title='Option Prices vs Volatility',
        xaxis_title='Volatility (%)',
        yaxis_title='Option Price ($)',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        hovermode="x unified"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def generate_greeks_chart(S0, K, r, T, sigma):
    """Generate JSON for stock price vs Greeks chart."""
    S_values = np.linspace(K*0.5, K*1.5, 100)
    
    # Calculate Greeks for call options
    delta_call = [BlackScholes.delta_call(S, K, r, T, sigma) for S in S_values]
    gamma = [BlackScholes.gamma(S, K, r, T, sigma) for S in S_values]
    vega = [BlackScholes.vega(S, K, r, T, sigma) / 100 for S in S_values]  # Scaled for better visibility
    theta_call = [BlackScholes.theta_call(S, K, r, T, sigma) / 365 for S in S_values]  # Daily theta
    
    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=S_values, y=delta_call, mode='lines', name='Delta', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=S_values, y=gamma, mode='lines', name='Gamma', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=S_values, y=vega, mode='lines', name='Vega (÷100)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=S_values, y=theta_call, mode='lines', name='Theta (daily)', line=dict(color='cyan')))
    
    fig.add_shape(
        type="line",
        x0=K, y0=np.min(theta_call), x1=K, y1=np.max(delta_call),
        line=dict(color="black", width=1, dash="dash")
    )
    
    fig.add_shape(
        type="line",
        x0=S0, y0=np.min(theta_call), x1=S0, y1=np.max(delta_call),
        line=dict(color="orange", width=1, dash="dash")
    )
    
    fig.update_layout(
        title='Option Greeks vs Stock Price',
        xaxis_title='Stock Price ($)',
        yaxis_title='Greek Value',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        hovermode="x unified"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for AJAX calculations."""
    data = request.json
    S0 = float(data.get('stock_price', 100))
    K = float(data.get('strike_price', 100))
    r = float(data.get('interest_rate', 0.05)) / 100  # Convert from percent
    T = float(data.get('maturity', 1.0))
    sigma = float(data.get('volatility', 0.2)) / 100  # Convert from percent
    
    # Calculate option prices
    call_price = BlackScholes.call_price(S0, K, r, T, sigma)
    put_price = BlackScholes.put_price(S0, K, r, T, sigma)
    
    # Calculate Greeks
    delta_call = BlackScholes.delta_call(S0, K, r, T, sigma)
    delta_put = BlackScholes.delta_put(S0, K, r, T, sigma)
    gamma = BlackScholes.gamma(S0, K, r, T, sigma)
    vega = BlackScholes.vega(S0, K, r, T, sigma)
    theta_call = BlackScholes.theta_call(S0, K, r, T, sigma) / 365  # Daily
    theta_put = BlackScholes.theta_put(S0, K, r, T, sigma) / 365  # Daily
    rho_call = BlackScholes.rho_call(S0, K, r, T, sigma) / 100  # Scaled
    rho_put = BlackScholes.rho_put(S0, K, r, T, sigma) / 100  # Scaled
    
    return jsonify({
        'call_price': call_price,
        'put_price': put_price,
        'delta_call': delta_call,
        'delta_put': delta_put,
        'gamma': gamma,
        'vega': vega,
        'theta_call': theta_call,
        'theta_put': theta_put,
        'rho_call': rho_call,
        'rho_put': rho_put
    })

if __name__ == '__main__':
    app.run(debug=True)
