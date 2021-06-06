document.addEventListener('DOMContentLoaded', function() {
    
    var attach_remove_event = [];
    
    var exists;
    if (document.querySelector('#star') === null) return;
    if (document.querySelector('#star').dataset.star != "None") exists = true;
    else exists = false;
    
    if (!exists) {
        var attach_enter = [];
        var attach_leave = [];
        for (var i = 1; i <= 5; i++)  {
            let star = document.querySelector(`#star${i}`);
            attach_enter.push(() => enter(star.dataset.star));
            star.addEventListener('mouseenter', attach_enter[i-1]);
            attach_leave.push(() => leave(star.dataset.star));
            star.addEventListener('mouseleave', attach_leave[i-1]);
            attach_remove_event.push(() => remove_event(attach_enter, attach_leave, exists));
            star.addEventListener('click', attach_remove_event[i-1]);
        }
    } else {
        rate(document.querySelector('#star').dataset.star);
    }

    for (var i = 1; i <= 5; i++) {
        let star = document.querySelector(`#star${i}`);
        star.addEventListener('click', () => rate(star.dataset.star));
    }

    function remove_event(attach_enter, attach_leave, exists) {
        // console.log('clicked');
        for (var i = 1; i <= 5; i++) {
            let star = document.querySelector(`#star${i}`);
            star.removeEventListener('mouseenter', attach_enter[i-1]);
            star.removeEventListener('mouseleave', attach_leave[i-1]);
            star.removeEventListener('click', attach_remove_event[i-1]);
        }
        exists = true;
    }
    
    document.querySelector('#new').onsubmit = function() {
        console.log(123);
        bookid = document.querySelector('#container').dataset.bookid;
        let csrftoken = getCookie('csrftoken');
        id = document.querySelector('#star').dataset.star;
        details = document.querySelector('textarea').value;
        if (id == 'None' || !details) return false;
        fetch(`/review/${bookid}`, {
            method: 'POST',
            body: JSON.stringify({
                id: id,
                details: details
            }),
            headers: { "X-CSRFToken": csrftoken },
        })
        .then(setTimeout(() => { location.reload(); }, 50));
        return false;              
    }
});

function enter(id) {
    // console.log('enter ' + id);
    for (var i = 1; i <= id; i++) {
        let star = document.querySelector(`#star${i}`).querySelector('img');
        setTimeout(() => { star.setAttribute('src', '/static/library/yellow-star.jpg'); }, 50);
    }
}

function leave(id) {
    // console.log('leave ' + id);
    for (var i = 1; i <= 5; i++) {
        let star = document.querySelector(`#star${i}`).querySelector('img');
        setTimeout(() => { star.setAttribute('src', '/static/library/white-star.jpg'); }, 50);
    }
}

function rate(id) {
    // console.log('rate ' + id);
    for (var i = 1; i <= id; i++)
        document.querySelector(`#star${i}`).querySelector('img').setAttribute('src', '/static/library/yellow-star.jpg');
    for (var i = parseInt(id) + 1; i <= 5; i++)
        document.querySelector(`#star${i}`).querySelector('img').setAttribute('src', '/static/library/white-star.jpg');
    document.querySelector('#star').dataset.star = id;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}