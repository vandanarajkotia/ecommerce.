from flask import Flask, render_template, redirect, url_for
import stripe

app = Flask(__name__)

stripe.api_key = "your_secret_key"

products = [
    {"id": 1, "name": "T-Shirt", "price": 500},
    {"id": 2, "name": "Shoes", "price": 1500},
]

@app.route("/")
def home():
    return render_template("shop.html")  # 👈 changed here

@app.route("/checkout/<int:product_id>")
def checkout(product_id):
    product = next(p for p in products if p["id"] == product_id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "inr",
                "product_data": {"name": product["name"]},
                "unit_amount": product["price"] * 100,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:5000/success",
        cancel_url="http://localhost:5000/",
    )

    return redirect(session.url)

@app.route("/success")
def success():
    return "<h1>Payment Successful 🎉</h1>"

if __name__ == "__main__":
    app.run(debug=True)