# chatbot.py
# This file contains the core logic and state management for the financial chatbot.

from datetime import datetime
import random

class FinanceChatbot:
    """
    Manages the user's profile, financial data, and conversation history.
    Contains the primary logic for handling data entry and generating summaries.
    """
    def __init__(self):
        """Initializes the chatbot's state."""
        self.user_profile = {}
        self.financial_data = {'income': [], 'expenses': [], 'savings': []}
        self.conversation_history = []

    def set_user_profile(self, age, income, location, family_size, risk_tolerance):
        """Saves the user's profile information."""
        self.user_profile = {
            'age': age, 'income': income, 'location': location,
            'family_size': family_size, 'risk_tolerance': risk_tolerance
        }
        return f"✅ Profile saved! Age: {age}, Income: ₹{income:,.2f}, Location: {location}, Family: {family_size}, Risk: {risk_tolerance}"

    def add_financial_data(self, data_type, amount, description, category=""):
        """Adds a single financial entry (income, expense, or saving)."""
        if amount is None or description is None:
            return "❌ Amount and description are required."
        try:
            entry = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'amount': float(amount),
                'description': description,
                'category': category
            }
            if data_type in self.financial_data:
                self.financial_data[data_type].append(entry)
                return f"✅ Added {data_type}: ₹{amount:,.2f} - {description}"
            return "❌ Invalid data type"
        except (ValueError, TypeError):
            return "❌ Invalid amount provided."

    def add_multiple_entries(self, text_input, data_type):
        """
        Parses a block of text to add multiple financial entries.
        
        Args:
            text_input (str): The multi-line string with financial data.
            data_type (str): The type of data ('expenses' or 'income').
        """
        if not text_input or not text_input.strip():
            return "❌ Input text cannot be empty."
            
        try:
            lines = text_input.strip().split('\n')
            added_count = 0
            total_amount = 0
            results = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                parts = [part.strip() for part in line.split(',')]
                
                if len(parts) >= 2:
                    try:
                        amount = float(parts[0])
                        description = parts[1]
                        
                        if data_type == 'expenses':
                            category = parts[2] if len(parts) > 2 else "Other"
                            self.add_financial_data('expenses', amount, description, category)
                            results.append(f"✅ ₹{amount:,.2f} - {description} ({category})")
                        else: # income
                            self.add_financial_data('income', amount, description, "Income")
                            results.append(f"✅ ₹{amount:,.2f} - {description}")

                        added_count += 1
                        total_amount += amount
                        
                    except ValueError:
                        results.append(f"❌ Invalid amount in line: {line}")
                else:
                    results.append(f"❌ Invalid format in line: {line}")
            
            summary = f"\n📊 **Summary**: Added {added_count} {data_type} totaling ₹{total_amount:,.2f}"
            return "\n".join(results) + summary
            
        except Exception as e:
            return f"❌ Error processing entries: {str(e)}"

    def generate_budget_summary(self):
        """Generates a summary of the user's budget based on stored data."""
        total_income = sum(entry['amount'] for entry in self.financial_data['income'])
        total_expenses = sum(entry['amount'] for entry in self.financial_data['expenses'])
        total_savings = sum(entry['amount'] for entry in self.financial_data['savings'])

        summary = f"""
📊 **Budget Summary**

💰 **Total Income**: ₹{total_income:,.2f}
💸 **Total Expenses**: ₹{total_expenses:,.2f}
💾 **Total Savings**: ₹{total_savings:,.2f}
📈 **Net Cash Flow**: ₹{total_income - total_expenses:,.2f}

🎯 **Recommendations**:
"""
        
        if total_income > 0:
            if total_expenses > total_income * 0.8:
                summary += "• Your expenses are high relative to income. Consider reducing non-essential spending.\n"
            if total_savings < total_income * 0.1:
                summary += "• Aim to save at least 10-20% of your income for emergencies and future goals.\n"
        
        if total_income - total_expenses > 0:
            summary += "• Great job! You have positive cash flow. Consider investing the surplus.\n"
        else:
            summary += "• You're spending more than you earn. Focus on reducing expenses or increasing income.\n"

        return summary

    def get_investment_advice(self):
        """Generates personalized investment advice based on user profile."""
        if not self.user_profile:
            return "Please set up your profile in the '👤 Profile Setup' tab first for personalized investment advice."
        
        age = self.user_profile.get('age', 30)
        risk_tolerance = self.user_profile.get('risk_tolerance', 'Moderate')
        income = self.user_profile.get('income', 0)
        
        # Calculate recommended allocation
        equity_allocation = {
            'Conservative': 40,
            'Moderate': 60,
            'Aggressive': 80
        }.get(risk_tolerance, 60)
        
        # Adjust equity allocation based on age
        if age < 30:
            equity_allocation += 10
        elif age > 50:
            equity_allocation -= 10
        
        debt_allocation = 100 - equity_allocation
        monthly_investment = income * 0.3  # Recommend 30% of income for investments
        
        advice = f"""
💡 **Personalized Investment Strategy**:

Based on your profile:
• Age: {age} years
• Risk Tolerance: {risk_tolerance}
• Monthly Income: ₹{income:,.2f}
• Recommended Monthly Investment: ₹{monthly_investment:,.2f}

**Suggested Portfolio Allocation**:
• 📈 Equity: {equity_allocation}% (₹{monthly_investment * equity_allocation/100:,.2f}/month)
• 🏦 Debt: {debt_allocation}% (₹{monthly_investment * debt_allocation/100:,.2f}/month)

**Investment Options for Your Profile**:
"""
        # Age-based specific recommendations
        if age < 30:
            advice += """
🎯 **Young Investor Focus**:
• Higher equity exposure for long-term growth
• Start SIPs in equity mutual funds
• Consider aggressive growth stocks
• Begin retirement planning early
"""
        elif age < 45:
            advice += """
🎯 **Mid-Career Focus**:
• Balanced portfolio with growth and stability
• Mix of equity and debt mutual funds
• Consider real estate investment
• Maximize tax-saving investments
"""
        else:
            advice += """
🎯 **Pre-Retirement Focus**:
• Focus on capital preservation
• Increase allocation to debt instruments
• Consider dividend-paying stocks
• Look into senior citizen saving schemes
"""

        # Risk tolerance based recommendations
        advice += "\n**Based on Your Risk Profile**:"
        if risk_tolerance == 'Conservative':
            advice += """
• 🏦 Fixed Income (50-60%):
  - Bank Fixed Deposits
  - Government Bonds
  - Corporate Bonds (AAA-rated)
  - Post Office Schemes

• 📊 Equity (30-40%):
  - Large-cap Mutual Funds
  - Blue-chip Stocks
  - Index Funds
  - Balanced Advantage Funds

• 🏰 Alternative (0-10%):
  - Gold ETFs
  - REITs
"""
        elif risk_tolerance == 'Moderate':
            advice += """
• 📊 Equity (50-60%):
  - Large-cap Funds (30%)
  - Mid-cap Funds (20%)
  - Index Funds (10%)
  
• 🏦 Fixed Income (30-40%):
  - Corporate Bonds
  - Government Securities
  - Banking & PSU Debt Funds
  
• 🏰 Alternative (10-20%):
  - REITs
  - Gold Funds
  - International Funds
"""
        else:  # Aggressive
            advice += """
• 📊 Equity (70-80%):
  - Mid-cap Funds (30%)
  - Small-cap Funds (20%)
  - Sectoral Funds (20%)
  - International Funds (10%)
  
• 🏦 Fixed Income (10-20%):
  - Dynamic Bond Funds
  - Credit Risk Funds
  
• 🏰 Alternative (10-20%):
  - Small-cap Direct Stocks
  - Commodity Funds
  - Crypto Funds (if allowed)
"""

        # Tax-saving investment suggestions
        monthly_80c = min(income * 0.15, 12500)  # 1.5L yearly limit
        advice += f"""
\n💰 **Tax-Saving Investment Options**:
• Recommended Monthly Tax-Saving: ₹{monthly_80c:,.2f}
• ELSS Mutual Funds
• PPF (Public Provident Fund)
• NPS (National Pension System)
• Term Insurance Premiums
• Tax-Saving Fixed Deposits
"""

        # Market-specific advice
        advice += """
\n📈 **Current Market Strategy**:
• Do systematic investment planning (SIP)
• Diversify across market caps
• Consider international diversification
• Review and rebalance quarterly
• Keep emergency fund separate
"""
            
        return advice

    def get_savings_advice(self):
        """Generates personalized savings advice based on financial data."""
        total_income = sum(entry['amount'] for entry in self.financial_data['income'])
        total_expenses = sum(entry['amount'] for entry in self.financial_data['expenses'])
        total_savings = sum(entry['amount'] for entry in self.financial_data['savings'])
        
        if total_income == 0:
            return "Please add your income details in the '💰 Financial Data' tab for personalized savings advice."
        
        current_savings_rate = (total_savings / total_income * 100) if total_income > 0 else 0
        monthly_expenses = total_expenses
        age = self.user_profile.get('age', 30) if self.user_profile else 30
        
        advice = f"""
💰 **Comprehensive Savings Plan**:

Current Status:
• Monthly Income: ₹{total_income:,.2f}
• Monthly Expenses: ₹{monthly_expenses:,.2f}
• Current Savings Rate: {current_savings_rate:.1f}%
• Net Monthly Surplus: ₹{total_income - monthly_expenses:,.2f}

🎯 **Essential Financial Goals**:

1. 🚨 **Emergency Fund**
   • Target: {6}-{12} months of expenses
   • Required: ₹{monthly_expenses * 6:,.2f} - ₹{monthly_expenses * 12:,.2f}
   • Keep in high-liquidity options like:
     - Savings Account
     - Short-term Fixed Deposits
     - Liquid Mutual Funds

2. 🏥 **Insurance Coverage**
   • Health Insurance: ₹{max(500000, monthly_expenses * 24):,.0f} minimum coverage
   • Term Life: {max(10, round(total_income * 12 * 10 / 100000) / 10)}Cr coverage suggested
   • Critical Illness Cover: ₹{monthly_expenses * 36:,.0f}

3. 💰 **Monthly Savings Allocation**
   • Minimum Target: 20% (₹{total_income * 0.2:,.2f})
   • Ideal Target: 30% (₹{total_income * 0.3:,.2f})
   • Your Potential: ₹{total_income - monthly_expenses:,.2f}

   Suggested Split:
   • Emergency Fund: 40% until target reached
   • Retirement: 30%
   • Short-term goals: 20%
   • Discretionary: 10%

4. 🎓 **Goal-based Savings**
   Short-term (1-3 years):
   • Build emergency fund
   • Save for large purchases
   • Create a debt repayment plan

   Medium-term (3-7 years):
   • House down payment
   • Higher education
   • Vehicle purchase

   Long-term (7+ years):
   • Retirement corpus
   • Children's education
   • Wealth creation

5. 📈 **Retirement Planning**"""
        
        # Add retirement-specific advice based on age
        if age < 30:
            advice += f"""
   • Start Early Advantage
   • Target Retirement Corpus: ₹{total_income * 12 * 25:,.0f}
   • Required Monthly Saving: ₹{(total_income * 12 * 25)/(35 * 12):,.0f}
   • Focus on equity-heavy portfolio"""
        elif age < 45:
            advice += f"""
   • Mid-Career Planning
   • Target Retirement Corpus: ₹{total_income * 12 * 20:,.0f}
   • Required Monthly Saving: ₹{(total_income * 12 * 20)/(20 * 12):,.0f}
   • Balance between equity and debt"""
        else:
            advice += f"""
   • Pre-Retirement Strategy
   • Target Retirement Corpus: ₹{total_income * 12 * 15:,.0f}
   • Required Monthly Saving: ₹{(total_income * 12 * 15)/(10 * 12):,.0f}
   • Focus on capital preservation"""

        advice += """

💡 **Smart Saving Strategies**:
1. Automate your savings (set up auto-debit)
2. Use the 50-30-20 rule:
   • 50% for needs
   • 30% for wants
   • 20% for savings
3. Track expenses regularly
4. Review and adjust monthly
5. Consider tax-saving investments
6. Build multiple income streams
"""

        # Add specific recommendations based on savings rate
        if current_savings_rate < 10:
            advice += """
🚩 **Priority Actions**:
• Cut non-essential expenses
• Look for additional income sources
• Renegotiate bills and subscriptions
• Create a strict budget
• Focus on building emergency fund first"""
        elif current_savings_rate < 20:
            advice += """
📈 **Next Steps**:
• Increase savings by 5% every 6 months
• Start investment SIPs
• Optimize tax savings
• Build emergency fund
• Review insurance coverage"""
        else:
            advice += """
🌟 **Growth Opportunities**:
• Maximize retirement contributions
• Explore investment opportunities
• Consider real estate investment
• Start tax planning early
• Look into passive income sources"""

        return advice

    def chat_response(self, message, history):
        """Generates a contextual response to a user's chat message."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['invest', 'stock', 'share', 'market', 'portfolio', 'mutual fund']):
            if 'stock' in message_lower and 'analysis' in message_lower:
                response = "I can help with stock analysis! Use the '📈 Stock Analysis' tab to get live data. Just enter a stock symbol like 'RELIANCE.BSE' or 'AAPL'."
            else:
                response = self.get_investment_advice()
        elif any(word in message_lower for word in ['credit', 'score', 'rating']):
            response = "I can help you estimate your credit score! Use the '🏆 Credit Score' tab to input your financial information and get a comprehensive analysis."
        elif any(word in message_lower for word in ['budget', 'spending', 'money']):
            response = "Budgeting is key! Add your income and expenses in the '💰 Financial Data' tab, then click 'Generate Budget Summary' in the '📊 Analysis & Insights' tab."
        elif any(word in message_lower for word in ['save', 'savings', 'emergency fund']):
            response = self.get_savings_advice()
        else:
            responses = [
                "I'm here to help with your financial questions! I can assist with budgeting, stock analysis, credit scores, and more.",
                "I'm your AI financial assistant! Feel free to ask about personal finance, or use the tabs to analyze your budget, stocks, or credit score."
            ]
            response = random.choice(responses)

        self.conversation_history.append({
            'user': message,
            'assistant': response,
            'timestamp': datetime.now().isoformat()
        })
        return response
