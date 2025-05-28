import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def d1(S, K, r, T, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))

def d2(S, K, r, T, sigma):
    return d1(S, K, r, T, sigma) - sigma * np.sqrt(T)

def call_price(S, K, r, T, sigma):
    D1 = d1(S, K, r, T, sigma)
    D2 = d2(S, K, r, T, sigma)
    return S * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)

def put_price(S, K, r, T, sigma):
    D1 = d1(S, K, r, T, sigma)
    D2 = d2(S, K, r, T, sigma)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)

def main(): 
    S0 = 100    # Current stock price
    K = 100     # Strike price
    r = 0.05    # Risk-free interest rate (5%)
    T = 1.0     # Time to maturity (1 year)
    sigma = 0.2 # Volatility (20%)

    call = call_price(S0, K, r, T, sigma)
    put = put_price(S0, K, r, T, sigma)

    print(f"Call option price: {call:.2f}")
    print(f"Put option price: {put:.2f}")

    S_values = np.linspace(50, 150, 100)  # Stock prices from $50 to $150
    call_prices = [call_price(S, K, r, T, sigma) for S in S_values]

    plt.figure(figsize=(10,6))
    plt.plot(S_values, call_prices, label='Call Option Price')
    plt.axhline(y=call_price(K, K, r, T, sigma), color='r', linestyle='--', label='At-the-money')
    plt.title('Black-Scholes Call Option Price vs Stock Price')
    plt.xlabel('Stock Price ($)')
    plt.ylabel('Call Option Price ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

    sigma_values = np.linspace(0.01, 0.5, 100)  # Volatility from 1% to 50%
    call_prices_vol = [call_price(S0, K, r, T, vol) for vol in sigma_values]

    plt.figure(figsize=(10,6))
    plt.plot(sigma_values, call_prices_vol, label='Call Option Price')
    plt.title('Black-Scholes Call Option Price vs Volatility')
    plt.xlabel('Volatility (σ)')
    plt.ylabel('Call Option Price ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()