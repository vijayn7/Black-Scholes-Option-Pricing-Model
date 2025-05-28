# Black-Scholes Option Pricing Model Web Application

This is an interactive web application for calculating and visualizing option prices and Greeks using the Black-Scholes model.

## Features

- Calculate European call and put option prices
- Visualize option prices with respect to changing stock prices and volatility
- Display option Greeks (Delta, Gamma, Vega, Theta, Rho)
- Interactive charts for better understanding of option behavior
- User-friendly interface for parameter inputs

## Prerequisites

- Python 3.7+
- Flask
- NumPy
- SciPy
- Plotly

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/Black-Scholes-Option-Pricing-Model.git
cd Black-Scholes-Option-Pricing-Model
```

2. Install the required packages:
```
pip install -r requirements.txt
```

## Usage

1. Run the application:
```
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

3. Input your option parameters:
   - Current stock price
   - Strike price
   - Risk-free interest rate
   - Time to maturity (in years)
   - Volatility

4. Click "Calculate" to view the option prices, Greeks, and visualizations

## Deployment

To deploy this application to production, you can use platforms like Heroku, AWS, or Google Cloud Platform.

Example deployment to Heroku:

1. Install the Heroku CLI and login:
```
heroku login
```

2. Create a Heroku app:
```
heroku create black-scholes-app
```

3. Create a Procfile in the project root directory:
```
echo "web: gunicorn app:app" > Procfile
```

4. Deploy to Heroku:
```
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Theory

The Black-Scholes model is a mathematical model for pricing European-style options. The model assumes:

- The stock follows a geometric Brownian motion with constant drift and volatility
- No transaction costs or taxes
- No dividends during the option's life
- Risk-free interest rate is constant
- No arbitrage opportunities

## License

This project is licensed under the MIT License - see the LICENSE file for details.
