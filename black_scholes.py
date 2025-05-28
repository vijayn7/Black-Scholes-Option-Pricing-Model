import numpy as np
from scipy.stats import norm

class BlackScholes:
    """
    A class for calculating Black-Scholes option prices and Greeks.
    """
    
    @staticmethod
    def d1(S, K, r, T, sigma):
        """
        Calculate the d1 component of the Black-Scholes formula.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The d1 component
        """
        return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    
    @staticmethod
    def d2(S, K, r, T, sigma):
        """
        Calculate the d2 component of the Black-Scholes formula.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The d2 component
        """
        return BlackScholes.d1(S, K, r, T, sigma) - sigma * np.sqrt(T)
    
    @staticmethod
    def call_price(S, K, r, T, sigma):
        """
        Calculate the price of a European call option.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The call option price
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        D2 = BlackScholes.d2(S, K, r, T, sigma)
        return S * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)
    
    @staticmethod
    def put_price(S, K, r, T, sigma):
        """
        Calculate the price of a European put option.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The put option price
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        D2 = BlackScholes.d2(S, K, r, T, sigma)
        return K * np.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)
    
    @staticmethod
    def delta_call(S, K, r, T, sigma):
        """
        Calculate the delta of a European call option.
        Delta measures the rate of change of option price with respect to the underlying asset price.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The call option delta
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        return norm.cdf(D1)
    
    @staticmethod
    def delta_put(S, K, r, T, sigma):
        """
        Calculate the delta of a European put option.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The put option delta
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        return norm.cdf(D1) - 1
    
    @staticmethod
    def gamma(S, K, r, T, sigma):
        """
        Calculate the gamma of an option.
        Gamma measures the rate of change of delta with respect to the underlying asset price.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The option gamma (same for call and put)
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        return norm.pdf(D1) / (S * sigma * np.sqrt(T))
    
    @staticmethod
    def vega(S, K, r, T, sigma):
        """
        Calculate the vega of an option.
        Vega measures the rate of change of option price with respect to volatility.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The option vega (same for call and put)
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        return S * np.sqrt(T) * norm.pdf(D1)
    
    @staticmethod
    def theta_call(S, K, r, T, sigma):
        """
        Calculate the theta of a European call option.
        Theta measures the rate of change of option price with respect to time.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The call option theta
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        D2 = BlackScholes.d2(S, K, r, T, sigma)
        term1 = -(S * norm.pdf(D1) * sigma) / (2 * np.sqrt(T))
        term2 = -r * K * np.exp(-r * T) * norm.cdf(D2)
        return term1 + term2
    
    @staticmethod
    def theta_put(S, K, r, T, sigma):
        """
        Calculate the theta of a European put option.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The put option theta
        """
        D1 = BlackScholes.d1(S, K, r, T, sigma)
        D2 = BlackScholes.d2(S, K, r, T, sigma)
        term1 = -(S * norm.pdf(D1) * sigma) / (2 * np.sqrt(T))
        term2 = r * K * np.exp(-r * T) * norm.cdf(-D2)
        return term1 + term2
    
    @staticmethod
    def rho_call(S, K, r, T, sigma):
        """
        Calculate the rho of a European call option.
        Rho measures the rate of change of option price with respect to interest rate.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The call option rho
        """
        D2 = BlackScholes.d2(S, K, r, T, sigma)
        return K * T * np.exp(-r * T) * norm.cdf(D2)
    
    @staticmethod
    def rho_put(S, K, r, T, sigma):
        """
        Calculate the rho of a European put option.
        
        Parameters:
        S (float): Current stock price
        K (float): Strike price
        r (float): Risk-free interest rate
        T (float): Time to maturity in years
        sigma (float): Volatility of the underlying asset
        
        Returns:
        float: The put option rho
        """
        D2 = BlackScholes.d2(S, K, r, T, sigma)
        return -K * T * np.exp(-r * T) * norm.cdf(-D2)
