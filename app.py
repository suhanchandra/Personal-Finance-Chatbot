# app.py
# This is the main entry point for the application.
# It initializes the chatbot logic, builds the UI, and launches the Gradio app.

from chatbot import FinanceChatbot
from ui import create_interface

def main():
    """
    Initializes and launches the financial chatbot application.
    """
    # Create an instance of the chatbot to manage the application's state and logic.
    chatbot_instance = FinanceChatbot()

    # Create the Gradio user interface, passing the chatbot instance to connect the UI to the logic.
    demo = create_interface(chatbot_instance)

    # Launch the Gradio application.
    print("🚀 Starting Simple Working Finance Chatbot...")
    print("📱 The app will open in your browser shortly...")
    print("📈 Features: Live Stock Analysis, Credit Score Checking, Budget Management")
    
    demo.launch(
        share=True,
        debug=True,
        server_name="127.0.0.1",  # Use localhost for testing
        server_port=7868
    )

if __name__ == "__main__":
    main()
