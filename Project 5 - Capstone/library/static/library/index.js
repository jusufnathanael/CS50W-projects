document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('#status').forEach(div => {
        if (div.querySelector('button') !== null) {
            div.querySelector('button').addEventListener('click', () => submit(div));
        }
    })
});

function submit(div) {
    let action = div.querySelector('button').innerText;
    if (action === "Borrow") {
        fetch(`/borrow/${div.dataset.id}`)
        .then(response => response.json())
        .then(result => {
            if (result.total >= 4) {
                location.reload();
            } else {
                div.innerHTML = '<i>You have borrowed this book.</i>';
            }
        });
    } else if (action === "Reserve") {
        fetch(`/reserve/${div.dataset.id}`);
        div.innerHTML = '<i>You have reserved this book.</i>';
    }
}