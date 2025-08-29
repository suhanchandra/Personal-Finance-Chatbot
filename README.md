# Personal Finance Chatbot 💰

A sophisticated AI-powered financial assistant that helps users manage their finances, make investment decisions, and plan their savings. Built with Python and Gradio, this chatbot provides personalized financial advice and real-time stock market analysis.

## Features 🌟

### 1. Profile Management 👤
- Personalized financial profile setup
- Risk tolerance assessment
- Income and family size considerations

### 2. Financial Data Management 📊
- Income tracking
- Expense monitoring
- Savings management
- Bulk data entry support

### 3. Investment Advice 📈
- Personalized portfolio allocation
- Age-based investment strategies
- Risk-profile based recommendations
- Tax-saving investment suggestions
- Real-time stock market data analysis

### 4. Savings Planning 💎
- Emergency fund calculations
- Goal-based savings recommendations
- Retirement planning
- Insurance coverage suggestions

### 5. Credit Score Analysis 🏆
- Credit score simulation
- Personalized credit improvement tips
- Debt management advice

### 6. Interactive Chat Interface 💬
- Natural language interaction
- Context-aware responses
- Financial education and guidance

## Getting Started 🚀

### Prerequisites
- Python 3.x
- Required packages:
  ```
  gradio
  requests
  ```

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/suhanchandra/Personal-Finance-Chatbot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Personal-Finance-Chatbot
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Usage Guide 📖

1. **Profile Setup**
   - Set your age, income, location, and risk tolerance
   - Input family size and financial goals

2. **Financial Data Entry**
   - Add regular income sources
   - Track daily/monthly expenses
   - Record savings and investments

3. **Investment Analysis**
   - Get personalized investment advice
   - Check real-time stock data
   - Receive portfolio allocation suggestions

4. **Budget Analysis**
   - View comprehensive budget summaries
   - Get spending insights
   - Track savings progress

5. **Credit Score Management**
   - Input financial parameters
   - Receive credit score estimates
   - Get improvement recommendations

## Architecture 🏗️

The application is structured into several key components:

- `app.py`: Main entry point and application initialization
- `chatbot.py`: Core chatbot logic and financial calculations
- `ui.py`: Gradio interface components
- `api_handler.py`: External API integrations
- `credit_calculator.py`: Credit score simulation logic

## Security Note 🔒

- The application uses demo API keys
- For production use, secure your API keys using environment variables
- Personal financial data is stored locally and not transmitted

## Contributing 🤝

Contributions are welcome! Please feel free to submit pull requests.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Built with [Gradio](https://gradio.app/)
- Stock data provided by [Alpha Vantage](https://www.alphavantage.co/)
