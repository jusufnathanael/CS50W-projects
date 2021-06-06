document.addEventListener('DOMContentLoaded', function() {
    
    normal_display();

    profile = document.querySelector('#profile');
    if (profile.dataset.enable === 'True') profile.style.display = 'block';
    else profile.style.display = 'none';

    new_post = document.querySelector('#new_post');
    if (new_post !== null) {
        new_post.onsubmit = function() {
            let csrftoken = getCookie('csrftoken');
            fetch('/add_or_edit', {
                method: 'POST',
                body: JSON.stringify({
                    action: 'add',
                    details: document.querySelector('#new_textarea').value,
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
            let delay = 50;
            setTimeout(function() {
                window.location.href = `/profile/${new_post.dataset.user}`;
            }, delay);
            return false;
        };
    }

    document.querySelectorAll('#edit_btn').forEach(btn => {
        btn.addEventListener('click', () => {
            normal_display();
            btn.parentElement.style.display = 'none';   // normal mode
            btn.parentElement.parentElement.querySelector('#edit_mode').style.display = 'block';  // edit mode
        });
    });

    document.querySelectorAll('#edit_post').forEach(form => {
        form.onsubmit = function() {
            normal_display();
            post_id = form.querySelector('#save_btn').value;
            let csrftoken = getCookie('csrftoken');
            fetch('/add_or_edit', {
                method: 'POST',
                body: JSON.stringify({
                    action: 'edit',
                    details: form.querySelector('#edit_textarea').value,
                    post_id: post_id
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
            const modes = form.parentElement.parentElement;
            modes.querySelector('#post_details').innerHTML = form.querySelector('#edit_textarea').value;
            return false;
        }
    });

    document.querySelectorAll('#like').forEach(span => {
        if (span.querySelector('#red') != null) {
            span.like = true;
        } else {
            span.like = false;
        }
        span.addEventListener('click', () => {
            let csrftoken = getCookie('csrftoken');
            fetch(`/like/${span.dataset.id}`, {
                method: 'PUT',
                headers: { "X-CSRFToken": csrftoken },
            })
            .then(response => response.json())
            .then(result => {
                console.log(result);
            });
            const num_likes = span.parentElement.querySelector('#num_likes');
            if (span.like) {
                num_likes.innerHTML = (parseInt(num_likes.innerHTML) - 1).toString();
                span.innerHTML = `<img id="white" src="/static/network/heart_white.png" width=17px>`
                span.like = false;
            } else {
                num_likes.innerHTML = (parseInt(num_likes.innerHTML) + 1).toString();
                span.innerHTML = `<img id="red" src="/static/network/heart_red.png" width=17px>`
                span.like = true;
            }
        })
    });

    form_paginator = document.querySelector('#paginator');
    form_paginator.onsubmit = function() {
        form_paginator.method = 'GET';
        form_paginator.action = form_paginator.dataset.action;
    };

    form_follow = document.querySelector('#follow_form');
    if (form_follow !== null) {
        if (form_follow.querySelector('#follow').innerHTML.includes('Unfollow')){
            form_follow.follows = true;
        } else {
            form_follow.follows = false;
        }
        console.log(form_follow);
        followers = document.querySelector('#followers');
        form_follow.onsubmit = function() {
            let csrftoken = getCookie('csrftoken');
            username = document.querySelector('#follow').value;
            fetch(`/profile/${username}`, {
                method: 'PUT',
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
            });
            if (form_follow.follows) {
                form_follow.querySelector('#follow').innerHTML = 'Follow';
                form_follow.follows = false;
                followers.innerHTML = (parseInt(followers.innerHTML) - 1).toString();
            } else {
                form_follow.querySelector('#follow').innerHTML = 'Unfollow';
                form_follow.follows = true;
                followers.innerHTML = (parseInt(followers.innerHTML) + 1).toString();
            }
            return false;
        };
    }

});

function normal_display() {
    // Hide edit mode
    document.querySelectorAll('#edit_mode').forEach(div => {
        div.style.display = 'none';
    });
    // Show normal mode
    document.querySelectorAll('#normal_mode').forEach(div => {
        div.style.display = 'block';
    });
    //document.querySelector('#profile').style.display = 'none';
}

// Get the cookies
// Alternatively, you can use the js-cookie library (https://github.com/js-cookie/js-cookie/).
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
