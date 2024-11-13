const loanAmountInput = document.getElementById('loan_amount');
const loanTermInput = document.getElementById('loan_term');
const interestRateInput = document.getElementById('interest_rate');
const fixedRateInput = document.getElementById('fixed_rate');
const variableRateInput = document.getElementById('variable_rate');

function sendDataToServer() {

    if (loanAmountInput.value && loanTermInput.value && interestRateInput.value && fixedRateInput.checked || variableRateInput.checked) {
        const data = {
            loan_amount: loanAmountInput.value,
            loan_term: loanTermInput.value,
            interest_rate: interestRateInput.value,
            interest_option: fixedRateInput.checked ? 'fixed_rate' : 'variable_rate',
        };

        fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(result => {
                const message = result.message !== undefined ? result.message : "Please fill out all fields.";
                document.getElementById('result').innerHTML = result.message;

                if (result.detailed_fees) {
                    renderTable(result.detailed_fees);
                }
        })
        .catch(error => console.error('Error:', error));
        document.getElementById('result').innerHTML = "An error occurred. Please try again.";
    }
}

function renderTable(detailedFees) {
    const table = `
        <table>
            <caption>Loan Results</caption>
            <thead>
                <tr>
                    <th scope="col">Month</th>
                    <th scope="col">Monthly Payment</th>
                    <th scope="col">Interests</th>
                    <th scope="col">Principal</th>
                    <th scope="col">Left to pay</th>
                </tr>
            </thead>
            <tbody>
                ${detailedFees.map(fee => `
                    <tr>
                        <td>${fee.month}</td>
                        <td>$${fee.monthly_payment}</td>
                        <td>$${fee.interest}</td>
                        <td>$${fee.principal}</td>
                        <td>$${fee.left_to_pay}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    document.getElementById('table_result').innerHTML = table;
}


loanAmountInput.addEventListener('input', sendDataToServer);
loanTermInput.addEventListener('input', sendDataToServer);
interestRateInput.addEventListener('input', sendDataToServer)
fixedRateInput.addEventListener('change', sendDataToServer);
variableRateInput.addEventListener('change', sendDataToServer);