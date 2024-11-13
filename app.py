from urllib import request
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    euribor_rate = 3.16
    rate = 'fixed interest'
    result = ''
    data = request.get_json()
    detailed_fees = []

    loan_amount = data.get('loan_amount')
    loan_term = data.get('loan_term')
    interest_rate = data.get('interest_rate')
    interest_option = data.get('interest_option')

    if loan_amount is None or loan_term is None or interest_rate is None or interest_option is None:
        return jsonify({"message": "Please fill out all fields."}), 400

    try:
        loan_amount = float(loan_amount)
        loan_term = int(loan_term)
        interest_rate = float(interest_rate)
    except ValueError:
        return jsonify({"message": "Please enter valid numbers in all fields."}), 400

    if loan_amount > 0 and loan_term > 0 and interest_rate >= 0:
        if interest_option == 'variable_rate':
            interest_rate += euribor_rate
            rate = f'variable interest (based on EURIBOR: {euribor_rate}%)'

        try:
            periodic_rate = (1 + interest_rate / 100) ** (1 / 12) - 1
            n = loan_term * 12
            monthly_payment = (loan_amount * periodic_rate * pow(1 + periodic_rate, n)) / (pow(1 + periodic_rate, n) - 1)
            total_interest = monthly_payment * n - loan_amount
            total_cost = loan_amount + total_interest
            remaining_balance = loan_amount

            result = (
                f"If you need ${loan_amount:,.2f} with a {rate} of {interest_rate:.2f}% and a repayment term of {loan_term} years: <br><br>"
                f"Your <b>monthly payment</b> will be ${monthly_payment:,.2f}. <br> "
                f"The total <b>interest</b> on your loan will be ${total_interest:,.2f}. <br> "
                f"In <b>total</b>, your loan will cost you <span>${total_cost:,.2f}</span>."
            )

            for i in range(1, n + 1):
                interest_payment = remaining_balance * periodic_rate
                principal_payment = monthly_payment - interest_payment
                remaining_balance -= principal_payment

                detailed_fees.append({
                    'month' : i,
                    'monthly_payment' : f'{monthly_payment:,.2f}',
                    'interest' : f'{interest_payment:,.2f}',
                    'principal' : f'{principal_payment:,.2f}',
                    'left_to_pay' : f'{remaining_balance:,.2f}',
                })


        except Exception as e:
            result = "An error occurred during the calculation."
    else:
        result = "Please fill out every field with valid numbers."

    return jsonify({"message": result, "detailed_fees": detailed_fees})



@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
