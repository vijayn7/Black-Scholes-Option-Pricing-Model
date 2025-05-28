// JavaScript for improved interactivity in the Black-Scholes Option Pricing Model web app

document.addEventListener('DOMContentLoaded', function() {
    // This will run when DOM is fully loaded
    
    // For real-time updates implementation (future enhancement)
    const realTimeUpdateForm = document.getElementById('real-time-form');
    
    if (realTimeUpdateForm) {
        const inputs = realTimeUpdateForm.querySelectorAll('input');
        
        inputs.forEach(input => {
            input.addEventListener('input', debounce(updateResults, 300));
        });
        
        function updateResults() {
            const formData = {
                stock_price: parseFloat(document.getElementById('stock_price').value),
                strike_price: parseFloat(document.getElementById('strike_price').value),
                interest_rate: parseFloat(document.getElementById('interest_rate').value),
                maturity: parseFloat(document.getElementById('maturity').value),
                volatility: parseFloat(document.getElementById('volatility').value)
            };
            
            // Make sure all inputs are valid before sending
            for (const key in formData) {
                if (isNaN(formData[key]) || formData[key] <= 0) {
                    return; // Don't send invalid data
                }
            }
            
            fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                // Update the option price displays
                document.getElementById('call-price').textContent = '$' + data.call_price.toFixed(2);
                document.getElementById('put-price').textContent = '$' + data.put_price.toFixed(2);
                
                // Update Greeks if they exist in the UI
                if (document.getElementById('delta-call')) {
                    document.getElementById('delta-call').textContent = data.delta_call.toFixed(4);
                    document.getElementById('delta-put').textContent = data.delta_put.toFixed(4);
                    document.getElementById('gamma').textContent = data.gamma.toFixed(4);
                    document.getElementById('vega').textContent = data.vega.toFixed(4);
                    document.getElementById('theta-call').textContent = data.theta_call.toFixed(4);
                    document.getElementById('theta-put').textContent = data.theta_put.toFixed(4);
                    document.getElementById('rho-call').textContent = data.rho_call.toFixed(4);
                    document.getElementById('rho-put').textContent = data.rho_put.toFixed(4);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }
    
    // Helper function to limit the rate at which a function can fire
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
});
