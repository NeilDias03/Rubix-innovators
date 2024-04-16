from flask import Flask, render_template, request
import time

app = Flask(__name__)

# Define responses for the chatbot
responses = {
    "hi": "Hello!",
    "123of65":  "Your order has been dispatched.",
    "are any coupons available": "OK, here's your coupon: 15001 Free",
    "123of66": "Your order has been cancelled"
}

# Variable to store the order status
order_status = {
    "processing": False,
    "dispatched": False
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    global order_status  # Declare global variable to update it within the function
    user_message = request.args.get('msg').lower()  # Get user's message and convert to lowercase
    bot_response = responses.get(user_message, "I'm sorry, I didn't understand that.")
    
    # Check if the user is asking about their order
    if "order" in user_message:
        if order_status["processing"]:
            bot_response = "Your order is currently being processed."
        elif order_status["dispatched"]:
            bot_response = "Your order has been dispatched."
        elif "123of65" in user_message:  # Check if the order ID is provided
            order_status["processing"] = True
            time.sleep(3)  # Simulate processing time (3 seconds)
            order_status["processing"] = False
            order_status["dispatched"] = True
            bot_response = "Your order has been dispatched."
        else:
            bot_response = "Sure, please provide your order ID."
    
    # Check if the user wants to cancel the order
    elif "cancel" in user_message:
        if "123of65" in user_message:  # Check if the order ID is provided
            bot_response = "Your order can be canceled. Are you sure you want to cancel it?"
        elif order_status["dispatched"]:
            bot_response = "Your order has already been dispatched. It cannot be canceled."
        else:
            bot_response = "Please provide your order ID first."
    
    # Check if the user confirms the cancellation
    elif "yes" in user_message and "cancel" in user_message:
        if "123of66" in user_message:  # Check if the order ID is provided
            bot_response = "Your order has been canceled."
        else:
            bot_response = "Please provide your order ID first."
    
    return bot_response

if __name__ == "__main__":
    app.run(debug=True)


