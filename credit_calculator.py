# credit_calculator.py
# Contains the logic for the simulated credit score calculation.

def calculate_credit_score(income, expenses, savings, debt_payments, 
                           credit_history_years, payment_history, credit_utilization):
    """
    Calculates a simulated credit score based on user-provided financial inputs.
    This is a simplified model for educational purposes.
    """
    try:
        # Convert inputs to float, handle None or invalid values
        income = float(income or 0)
        expenses = float(expenses or 0)
        savings = float(savings or 0)
        debt_payments = float(debt_payments or 0)
        credit_history_years = int(credit_history_years or 0)
        credit_utilization = float(credit_utilization or 0)

        score = 300  # Base score

        # 1. Payment History (35% weight)
        if payment_history == "Excellent": score += 175
        elif payment_history == "Good": score += 150
        elif payment_history == "Fair": score += 100
        else: score += 50

        # 2. Credit Utilization (30% weight)
        if credit_utilization < 0.1: score += 150
        elif credit_utilization < 0.3: score += 125
        elif credit_utilization < 0.5: score += 75
        elif credit_utilization < 0.8: score += 40
        else: score += 10

        # 3. Credit History Length (15% weight)
        if credit_history_years > 10: score += 100
        elif credit_history_years > 5: score += 75
        elif credit_history_years > 2: score += 50
        else: score += 25
        
        # 4. Debt-to-Income Ratio (10% weight)
        dti_ratio = (expenses + debt_payments) / income if income > 0 else 1
        if dti_ratio < 0.3: score += 75
        elif dti_ratio < 0.43: score += 50
        elif dti_ratio < 0.6: score += 25

        # 5. Savings Rate (10% weight)
        savings_rate = savings / income if income > 0 else 0
        if savings_rate > 0.2: score += 75
        elif savings_rate > 0.1: score += 50
        else: score += 25
        
        score = max(300, min(850, score))
        
        if score >= 800: rating, color = "Exceptional", "🟢"
        elif score >= 740: rating, color = "Very Good", "🟢"
        elif score >= 670: rating, color = "Good", "🟡"
        elif score >= 580: rating, color = "Fair", "🟠"
        else: rating, color = "Poor", "🔴"
        
        result = f"""
{color} **Credit Score Analysis (Simulation)**

- 📊 **Your Simulated Score**: {score}
- 🏆 **Rating**: {rating}

---
#### **Factors Analyzed**:
- **Debt-to-Income Ratio**: `{dti_ratio:.1%}`
- **Savings Rate**: `{savings_rate:.1%}`
- **Payment History**: `{payment_history}`
- **Credit Utilization**: `{credit_utilization:.1%}`
- **Credit History**: `{credit_history_years} years`

---
#### **💡 Recommendations**:\n
"""
        recommendations = []
        if dti_ratio > 0.43: recommendations.append("• **Reduce your debt-to-income ratio.** A ratio below 36-43% is generally considered healthy.")
        if savings_rate < 0.1: recommendations.append("• **Increase your savings rate.** Aiming for 15-20% is a great goal for financial security.")
        if credit_utilization > 0.3: recommendations.append("• **Lower your credit utilization.** Keeping your used credit below 30% of your total limit is ideal.")
        if not recommendations: result += "• **Keep up the great work!** Your financial habits are strong. Continue to monitor your finances regularly."
        else: result += "\n".join(recommendations)
            
        return result
        
    except (ValueError, TypeError) as e:
        return f"❌ Error: Please ensure all inputs are valid numbers. Details: {e}"
    except Exception as e:
        return f"❌ An unexpected error occurred during calculation: {str(e)}"
