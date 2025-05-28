import numpy as np
import matplotlib.pyplot as plt
from black_scholes import BlackScholes

def main(): 
    S0 = 100    # Current stock price
    K = 100     # Strike price
    r = 0.05    # Risk-free interest rate (5%)
    T = 1.0     # Time to maturity (1 year)
    sigma = 0.2 # Volatility (20%)

    call = BlackScholes.call_price(S0, K, r, T, sigma)
    put = BlackScholes.put_price(S0, K, r, T, sigma)

    print(f"Call option price: {call:.2f}")
    print(f"Put option price: {put:.2f}")

    S_values = np.linspace(50, 150, 100)  # Stock prices from $50 to $150
    call_prices = [BlackScholes.call_price(S, K, r, T, sigma) for S in S_values]

    plt.figure(figsize=(10,6))
    plt.plot(S_values, call_prices, label='Call Option Price')
    plt.axhline(y=BlackScholes.call_price(K, K, r, T, sigma), color='r', linestyle='--', label='At-the-money')
    plt.title('Black-Scholes Call Option Price vs Stock Price')
    plt.xlabel('Stock Price ($)')
    plt.ylabel('Call Option Price ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

    sigma_values = np.linspace(0.01, 0.5, 100)  # Volatility from 1% to 50%
    call_prices_vol = [BlackScholes.call_price(S0, K, r, T, vol) for vol in sigma_values]

    plt.figure(figsize=(10,6))
    plt.plot(sigma_values, call_prices_vol, label='Call Option Price')
    plt.title('Black-Scholes Call Option Price vs Volatility')
    plt.xlabel('Volatility (σ)')
    plt.ylabel('Call Option Price ($)')
    plt.legend()
    plt.grid(True)
    plt.show()

    S_values = np.linspace(50, 150, 100)
    delta_values = [BlackScholes.delta_call(S, K, r, T, sigma) for S in S_values]
    gamma_values = [BlackScholes.gamma(S, K, r, T, sigma) for S in S_values]
    vega_values = [BlackScholes.vega(S, K, r, T, sigma) for S in S_values]
    theta_values = [BlackScholes.theta_call(S, K, r, T, sigma) for S in S_values]
    rho_values = [BlackScholes.rho_call(S, K, r, T, sigma) for S in S_values]

    plt.figure(figsize=(12,8))
    plt.plot(S_values, delta_values, label='Delta')
    plt.plot(S_values, gamma_values, label='Gamma')
    plt.plot(S_values, vega_values, label='Vega')
    plt.plot(S_values, theta_values, label='Theta')
    plt.plot(S_values, rho_values, label='Rho')
    plt.title('Greeks vs Stock Price')
    plt.xlabel('Stock Price ($)')
    plt.ylabel('Greek Value')
    plt.legend()
    plt.grid(True)
    plt.show()

    sigma_values = np.linspace(0.01, 0.5, 100)
    delta_vol = [BlackScholes.delta_call(S0, K, r, T, vol) for vol in sigma_values]
    gamma_vol = [BlackScholes.gamma(S0, K, r, T, vol) for vol in sigma_values]
    vega_vol = [BlackScholes.vega(S0, K, r, T, vol) for vol in sigma_values]
    theta_vol = [BlackScholes.theta_call(S0, K, r, T, vol) for vol in sigma_values]
    rho_vol = [BlackScholes.rho_call(S0, K, r, T, vol) for vol in sigma_values]

    plt.figure(figsize=(12,8))
    plt.plot(sigma_values, delta_vol, label='Delta')
    plt.plot(sigma_values, gamma_vol, label='Gamma')
    plt.plot(sigma_values, vega_vol, label='Vega')
    plt.plot(sigma_values, theta_vol, label='Theta')
    plt.plot(sigma_values, rho_vol, label='Rho')
    plt.title('Greeks vs Volatility')
    plt.xlabel('Volatility (σ)')
    plt.ylabel('Greek Value')
    plt.legend()
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    main()