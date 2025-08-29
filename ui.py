# ui.py
# This file defines the Gradio user interface for the application.

import gradio as gr
from api_handler import get_stock_data
from credit_calculator import calculate_credit_score

def create_interface(chatbot):
    """
    Builds the entire Gradio UI with all tabs and components.

    Args:
        chatbot (FinanceChatbot): An instance of the chatbot to link UI actions to backend logic.

    Returns:
        gr.Blocks: The Gradio interface object.
    """
    with gr.Blocks(title="Simple Working Finance Chatbot", theme=gr.themes.Soft()) as demo:
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>💰 Simple Working Finance Chatbot</h1>
            <p>Your AI-powered personal finance assistant with Live Stock Analysis & Credit Score Checking</p>
        </div>
        """)

        with gr.Tabs():
            # Profile Setup Tab
            with gr.Tab("👤 Profile Setup"):
                gr.Markdown("### Setup Your Financial Profile")
                with gr.Row():
                    age_input = gr.Slider(18, 80, value=30, label="Age", step=1)
                    income_input = gr.Number(value=50000, label="Monthly Income (₹)")
                with gr.Row():
                    location_input = gr.Textbox(value="India", label="Location")
                    family_size_input = gr.Slider(1, 10, value=2, label="Family Size", step=1)
                risk_tolerance = gr.Radio(["Conservative", "Moderate", "Aggressive"], value="Moderate", label="Investment Risk Tolerance")
                profile_btn = gr.Button("Save Profile", variant="primary")
                profile_status = gr.Textbox(label="Status", interactive=False)
                profile_btn.click(chatbot.set_user_profile, inputs=[age_input, income_input, location_input, family_size_input, risk_tolerance], outputs=[profile_status])

            # Data Entry Tab
            with gr.Tab("💰 Financial Data"):
                gr.Markdown("### Add Your Financial Information")
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.Markdown("#### 📝 Add Multiple Income")
                        gr.Markdown("**Format**: `amount, description` (one per line)")
                        multiple_income_input = gr.Textbox(label="Bulk Income Entry", placeholder="50000, Monthly Salary\n10000, Freelance Project", lines=5)
                        add_multiple_income_btn = gr.Button("Add Multiple Income", variant="secondary")
                        multiple_income_status = gr.Textbox(label="Status", interactive=False)
                        add_multiple_income_btn.click(lambda x: chatbot.add_multiple_entries(x, 'income'), inputs=[multiple_income_input], outputs=[multiple_income_status])

                    with gr.Column(scale=2):
                        gr.Markdown("#### 📝 Add Multiple Expenses")
                        gr.Markdown("**Format**: `amount, description, category` (category is optional)")
                        multiple_expenses_input = gr.Textbox(label="Bulk Expense Entry", placeholder="15000, Rent, Housing\n5000, Groceries, Food", lines=5)
                        add_multiple_btn = gr.Button("Add Multiple Expenses", variant="secondary")
                        multiple_expense_status = gr.Textbox(label="Status", interactive=False)
                        add_multiple_btn.click(lambda x: chatbot.add_multiple_entries(x, 'expenses'), inputs=[multiple_expenses_input], outputs=[multiple_expense_status])

                    with gr.Column(scale=1):
                        gr.Markdown("#### Add Single Saving")
                        savings_amount = gr.Number(label="Amount (₹)")
                        savings_desc = gr.Textbox(label="Description", placeholder="Emergency fund...")
                        add_savings_btn = gr.Button("Add Saving")
                        savings_status = gr.Textbox(label="Status", interactive=False)
                        add_savings_btn.click(lambda amt, desc: chatbot.add_financial_data('savings', amt, desc), inputs=[savings_amount, savings_desc], outputs=[savings_status])
            
            # Stock Analysis Tab
            with gr.Tab("📈 Stock Analysis"):
                gr.Markdown("### Live Stock Market Analysis")
                gr.Markdown("Get real-time stock data from Alpha Vantage. Examples: `IBM`, `AAPL`, `RELIANCE.BSE`")
                with gr.Row():
                    stock_symbol = gr.Textbox(label="Stock Symbol", placeholder="Enter stock symbol (e.g., AAPL)", value="IBM")
                    analyze_btn = gr.Button("Analyze Stock", variant="primary")
                stock_analysis_output = gr.Markdown(label="Stock Analysis")
                analyze_btn.click(get_stock_data, inputs=[stock_symbol], outputs=[stock_analysis_output])

            # Credit Score Tab
            with gr.Tab("🏆 Credit Score"):
                gr.Markdown("### Credit Score Calculator (Simulation)")
                gr.Markdown("Get a simulated credit score analysis based on your financial profile.")
                with gr.Row():
                    with gr.Column():
                        credit_income = gr.Number(value=50000, label="Monthly Income (₹)")
                        credit_expenses = gr.Number(value=25000, label="Monthly Expenses (₹)")
                        credit_savings = gr.Number(value=10000, label="Monthly Savings (₹)")
                        credit_debt = gr.Number(value=5000, label="Monthly Debt Payments (₹)")
                    with gr.Column():
                        credit_history = gr.Slider(0, 30, value=5, label="Credit History (Years)", step=1)
                        payment_history = gr.Dropdown(["Excellent", "Good", "Fair", "Poor"], value="Good", label="Payment History")
                        credit_utilization = gr.Slider(0, 1, value=0.3, label="Credit Utilization Ratio", step=0.01)
                credit_calc_btn = gr.Button("Calculate Credit Score", variant="primary")
                credit_score_output = gr.Markdown(label="Credit Score Analysis")
                credit_calc_btn.click(calculate_credit_score, inputs=[credit_income, credit_expenses, credit_savings, credit_debt, credit_history, payment_history, credit_utilization], outputs=[credit_score_output])

            # Analysis Tab
            with gr.Tab("📊 Analysis & Insights"):
                gr.Markdown("### Your Financial Snapshot")
                budget_btn = gr.Button("Generate Budget Summary", variant="primary")
                budget_output = gr.Markdown(label="Budget Summary")
                budget_btn.click(chatbot.generate_budget_summary, outputs=[budget_output])

            # Chat Tab
            with gr.Tab("💬 Chat"):
                gr.Markdown("### Chat with Your Finance Assistant")
                gr.Markdown("Ask questions about stocks, credit scores, budgeting, saving, investing, or any financial topic!")
                chatbot_interface = gr.Chatbot(label="Finance Chat", height=500)
                with gr.Row():
                    msg_input = gr.Textbox(label="Your Message", placeholder="Ask me about personal finance...", lines=2, scale=9)
                    send_btn = gr.Button("Send 📤", variant="primary", scale=1)
                clear_btn = gr.Button("Clear Chat 🗑️")
                
                def respond(message, history):
                    if not message or not message.strip():
                        return history
                    bot_response = chatbot.chat_response(message, history)
                    history.append((message, bot_response))
                    return history

                def clear_chat():
                    return [], ""  # Clear both chat history and input box

                # Handle send button and enter key
                msg_input.submit(respond, [msg_input, chatbot_interface], [chatbot_interface])
                msg_input.submit(lambda: "", None, msg_input)  # Clear input on submit
                send_btn.click(respond, [msg_input, chatbot_interface], [chatbot_interface])
                send_btn.click(lambda: "", None, msg_input)  # Clear input after sending

                # Handle clear button
                clear_btn.click(clear_chat, None, [chatbot_interface, msg_input])

        gr.HTML("""
        <div style="text-align: center; padding: 20px; margin-top: 20px; border-top: 1px solid #ddd;">
            <p><strong>Simple Working Finance Chatbot</strong> - Your AI Financial Assistant</p>
            <p><em>This is for educational purposes. Consult qualified professionals for financial decisions. Stock data may have delays.</em></p>
        </div>
        """)
        return demo
