document.addEventListener('DOMContentLoaded', function() {
    page('borrowing', 'reservation', 'payment');
    document.querySelector('#borrowing-btn').addEventListener('click', () => page('borrowing', 'reservation', 'payment'));
    document.querySelector('#reservation-btn').addEventListener('click', () => page('reservation', 'borrowing', 'payment'));
    document.querySelector('#payment-btn').addEventListener('click', () => page('payment', 'borrowing', 'reservation'));
    if (document.querySelector("#payment").dataset.exist !== "<QuerySet []>") {
        document.querySelector('#btn-calculate').addEventListener('click', () => calculate());
        document.querySelector('#btn-checkout').addEventListener('click', () => checkout());
    }
});

function page(active, inactive1, inactive2) {
    document.querySelector(`#${active}`).style.display = 'block';
    document.querySelector(`#${active}-btn`).setAttribute('class', 'page-item active');
    document.querySelector(`#${inactive1}`).style.display = 'none';
    document.querySelector(`#${inactive1}-btn`).setAttribute('class', 'page-item');
    document.querySelector(`#${inactive2}`).style.display = 'none';
    document.querySelector(`#${inactive2}-btn`).setAttribute('class', 'page-item');
}

function calculate() {
    let total = 0;
    document.querySelectorAll('#checkbox').forEach(input => {
        if (input.checked) total += parseInt(input.dataset.amount);
    });
    document.querySelector('#value').innerHTML = `Total: $${Number(total).toFixed(2)}`;
    if (total > 0) document.querySelector('#btn-checkout').disabled = false;
    document.querySelector('#btn-checkout').value = total;
    return false;
}

function checkout() {
    let total = document.querySelector('#btn-checkout').value;
    document.querySelector('#amount').innerHTML = `$${Number(total).toFixed(2)}<input name="amount" type="hidden" value="${total}">`;
}