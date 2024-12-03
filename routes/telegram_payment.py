from flask import Flask, render_template, jsonify, request
from datetime import datetime
import urllib.parse
import requests  # Use requests to send HTTP requests
from app import app

@app.route('/payment', methods=['POST'])
def payment():
    data = request.json
    cart_items = data['cart']

    total_price = sum(item['qty'] * float(item['price']) for item in cart_items)

    formatted_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    # replace your telegram bot token and chat id
    telegram_bot_token = ''
    telegram_chat_id = ''

    message = f"""
🛎 *New Order Confirmation* 🛎
📅 *Booking Date*: {formatted_date}
📦 *Items*: {', '.join([f'{item["name"]} x{item["qty"]}' for item in cart_items])}
💵 *Total Price*: ${total_price:.2f}
🎉 Thank you for your support! 🎉
"""

    # Encode the message for the URL
    encoded_message = urllib.parse.quote(message)

    # Build the Telegram API URL
    telegram_url = f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={encoded_message}&parse_mode=Markdown'

    # Send the message to Telegram using requests.get
    telegram_response = requests.get(telegram_url)

    # Check if the Telegram response was successful
    if telegram_response.status_code != 200:
        return jsonify({"error": f"Failed to send message to Telegram: {telegram_response.status_code}"}), 500

    print(f"Date: {formatted_date}, Items: {cart_items}, Total Price: ${total_price:.2f}")

    # Return a success message status 201
    return jsonify({"message": "Order placed successfully"}), 201
