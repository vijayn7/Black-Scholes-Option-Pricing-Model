import numpy as np
import matplotlib.pyplot as plt
from black_scholes import BlackScholes

class OptionVisualizer:
    """
    A class for visualizing option prices and Greeks using the Black-Scholes model.
    """
    
    def __init__(self, S0=100, K=100, r=0.05, T=1.0, sigma=0.2):
        """
        Initialize the visualizer with default option parameters.
        
        Parameters:
        S0 (float): Initial stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.sigma = sigma
        
    def calculate_option_prices(self):
        """Calculate and display option prices with current parameters."""
        call = BlackScholes.call_price(self.S0, self.K, self.r, self.T, self.sigma)
        put = BlackScholes.put_price(self.S0, self.K, self.r, self.T, self.sigma)
        
        print(f"Option Parameters:")
        print(f"  Stock Price (S0): {self.S0}")
        print(f"  Strike Price (K): {self.K}")
        print(f"  Risk-free Rate (r): {self.r:.2%}")
        print(f"  Time to Maturity (T): {self.T} years")
        print(f"  Volatility (σ): {self.sigma:.2%}")
        print(f"\nOption Prices:")
        print(f"  Call option price: ${call:.2f}")
        print(f"  Put option price: ${put:.2f}")
        
    def plot_price_vs_stock_price(self):
        """Plot option price vs stock price."""
        S_values = np.linspace(self.K/2, self.K*1.5, 100)
        call_prices = [BlackScholes.call_price(S, self.K, self.r, self.T, self.sigma) for S in S_values]
        put_prices = [BlackScholes.put_price(S, self.K, self.r, self.T, self.sigma) for S in S_values]
        
        plt.figure(figsize=(12, 6))
        plt.plot(S_values, call_prices, 'b-', label='Call Option Price')
        plt.plot(S_values, put_prices, 'r-', label='Put Option Price')
        plt.axvline(x=self.K, color='k', linestyle='--', alpha=0.5, label='Strike Price')
        plt.title('Option Prices vs Stock Price')
        plt.xlabel('Stock Price ($)')
        plt.ylabel('Option Price ($)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def plot_price_vs_volatility(self):
        """Plot option price vs volatility."""
        sigma_values = np.linspace(0.01, 0.5, 100)
        call_prices = [BlackScholes.call_price(self.S0, self.K, self.r, self.T, vol) for vol in sigma_values]
        put_prices = [BlackScholes.put_price(self.S0, self.K, self.r, self.T, vol) for vol in sigma_values]
        
        plt.figure(figsize=(12, 6))
        plt.plot(sigma_values, call_prices, 'b-', label='Call Option Price')
        plt.plot(sigma_values, put_prices, 'r-', label='Put Option Price')
        plt.axvline(x=self.sigma, color='k', linestyle='--', alpha=0.5, label='Current Volatility')
        plt.title('Option Prices vs Volatility')
        plt.xlabel('Volatility (σ)')
        plt.ylabel('Option Price ($)')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def plot_greeks_vs_stock_price(self):
        """Plot option Greeks vs stock price."""
        S_values = np.linspace(self.K*0.5, self.K*1.5, 100)
        
        # Calculate Greeks for call options
        delta_call = [BlackScholes.delta_call(S, self.K, self.r, self.T, self.sigma) for S in S_values]
        gamma = [BlackScholes.gamma(S, self.K, self.r, self.T, self.sigma) for S in S_values]
        vega = [BlackScholes.vega(S, self.K, self.r, self.T, self.sigma) / 100 for S in S_values]  # Scaled for better visibility
        theta_call = [BlackScholes.theta_call(S, self.K, self.r, self.T, self.sigma) / 365 for S in S_values]  # Daily theta
        rho_call = [BlackScholes.rho_call(S, self.K, self.r, self.T, self.sigma) / 100 for S in S_values]  # Scaled for better visibility
        
        plt.figure(figsize=(14, 8))
        plt.plot(S_values, delta_call, 'b-', label='Delta')
        plt.plot(S_values, gamma, 'g-', label='Gamma')
        plt.plot(S_values, vega, 'r-', label='Vega (scaled ÷100)')
        plt.plot(S_values, theta_call, 'c-', label='Theta (daily)')
        plt.plot(S_values, rho_call, 'm-', label='Rho (scaled ÷100)')
        plt.axvline(x=self.K, color='k', linestyle='--', alpha=0.5, label='Strike Price')
        plt.axvline(x=self.S0, color='y', linestyle='--', alpha=0.5, label='Current Stock Price')
        plt.title('Option Greeks vs Stock Price')
        plt.xlabel('Stock Price ($)')
        plt.ylabel('Greek Value')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def plot_greeks_vs_volatility(self):
        """Plot option Greeks vs volatility."""
        sigma_values = np.linspace(0.05, 0.5, 100)
        
        # Calculate Greeks for different volatilities
        delta_vol = [BlackScholes.delta_call(self.S0, self.K, self.r, self.T, vol) for vol in sigma_values]
        gamma_vol = [BlackScholes.gamma(self.S0, self.K, self.r, self.T, vol) for vol in sigma_values]
        vega_vol = [BlackScholes.vega(self.S0, self.K, self.r, self.T, vol) / 100 for vol in sigma_values]  # Scaled
        theta_vol = [BlackScholes.theta_call(self.S0, self.K, self.r, self.T, vol) / 365 for vol in sigma_values]  # Daily
        rho_vol = [BlackScholes.rho_call(self.S0, self.K, self.r, self.T, vol) / 100 for vol in sigma_values]  # Scaled
        
        plt.figure(figsize=(14, 8))
        plt.plot(sigma_values, delta_vol, 'b-', label='Delta')
        plt.plot(sigma_values, gamma_vol, 'g-', label='Gamma')
        plt.plot(sigma_values, vega_vol, 'r-', label='Vega (scaled ÷100)')
        plt.plot(sigma_values, theta_vol, 'c-', label='Theta (daily)')
        plt.plot(sigma_values, rho_vol, 'm-', label='Rho (scaled ÷100)')
        plt.axvline(x=self.sigma, color='k', linestyle='--', alpha=0.5, label='Current Volatility')
        plt.title('Option Greeks vs Volatility')
        plt.xlabel('Volatility (σ)')
        plt.ylabel('Greek Value')
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def plot_all(self):
        """Generate all plots."""
        self.calculate_option_prices()
        self.plot_price_vs_stock_price()
        self.plot_price_vs_volatility()
        self.plot_greeks_vs_stock_price()
        self.plot_greeks_vs_volatility()


def main():
    """Main function to demonstrate the Black-Scholes model visualization."""
    visualizer = OptionVisualizer(
        S0=100,    # Current stock price
        K=100,     # Strike price
        r=0.05,    # Risk-free interest rate (5%)
        T=1.0,     # Time to maturity (1 year)
        sigma=0.2  # Volatility (20%)
    )
    
    visualizer.plot_all()


if __name__ == "__main__":
    main()