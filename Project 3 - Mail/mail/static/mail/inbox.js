document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(undefined));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#display-email').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (email === undefined) {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  } else {
    // Load previous composition fields
    document.querySelector('#compose-recipients').value = email.recipients;
    if (email.subject.substring(0,3) === 'Re:') {
      document.querySelector('#compose-subject').value = email.subject;
    } else {
      document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    }
    let prepend = '\n\n' + '----------------------------------------------------------------' + 
                  '\n' + 'On ' + email.timestamp + ', ' + email.sender + ' wrote:\n';
    document.querySelector('#compose-body').value = prepend + convert_br_to_new_line(email.body);
  }

  // Send the email
  document.querySelector('form').onsubmit = function() {
    let txt = document.querySelector('#compose-body').value;
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: convert_new_line_to_br(txt)
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    let delay = 50; // in milliseconds
    setTimeout(function() {
      //your code to be executed after the delay
      document.querySelector('#sent').click()
    }, delay);
    
    return false;
  }

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#display-email').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    let counter = 0;
    // Loop through the emails
    while (counter < emails.length) {

      // The body of the email
      const div = document.createElement('div');
      div.setAttribute('class', 'card card-modified');
      // Unread emails css
      let style = "bold";
      let color = "white";
      // Read emails css
      if (emails[counter].read) {
        color = "#ddd";
        style = "normal";
        div.style.backgroundColor = color;
      }
      // Create the innerHTML
      let string = get_string(emails[counter], mailbox, style, color);
      div.innerHTML = string;
      // Add an event listener
      let curr_email = emails[counter];
      div.addEventListener('click', () => load_email(curr_email));
      // Append to #emails-view div
      document.querySelector('#emails-view').append(div);

      // The archive button
      if (mailbox !== 'sent') {
        const btn = document.createElement('button');
        btn.setAttribute('class', 'btn btn-info btn-sm btn-modified');
        if (!emails[counter].archived) {
          btn.innerHTML = 'add to archive';
        } else {
          btn.innerHTML = 'remove from archive';
        }
        btn.addEventListener('click', () => change_archive(curr_email));
        document.querySelector("#emails-view").append(btn);
      }
      counter++;
    }
    console.log(emails);
  });

  function get_string(email, mailbox, style, color) {
    let person = `<i>From:</i> ${email.sender}<br>`;
    let tag = 'Received';
    if (mailbox === 'sent') {
      person = `<i>To:</i> ${email.recipients}<br>`;
      tag = 'Sent';
    }
    return `<button id="btn-email" class="card-body card-body-modified" ` +
           `style="font-weight: ${style}; background-color: ${color};>"` +
           `${person}` + `<i>Subject:</i> ${email.subject}<br>` +
           `<i>${tag}:</i> ${email.timestamp}` + `</button>`;
  }
}

function load_email(email) {
  
  // Show the email and hide other views
  document.querySelector('#display-email').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#display-email').innerHTML = '';

  // Mark as read
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // Get the details of the email
  fetch(`/emails/${email.id}`)
  .then(response => response.json())
  .then(email => {
    let details = document.createElement('div');
    details.innerHTML = get_details(email);
    let message = document.createElement('div');
    message.innerHTML = get_message(email);
    let btn = document.createElement('button');
    btn.setAttribute('class', 'btn btn-outline-secondary btn-sm btn-modified');
    btn.innerHTML = 'reply';
    btn.addEventListener('click', () => compose_email(email));
    document.querySelector('#display-email').append(details);
    document.querySelector('#display-email').append(btn);
    document.querySelector('#display-email').append(message);
  });
  
  function get_details(email) {
    return '<table>' +
           '<tr>' + '<td style="width:80px">' + '<strong>From:</strong>' + '</td>' + `<td>${email.sender}</td>` + '</tr>' +
           '<tr>' + '<td>' + '<strong>To:</strong>' + '</td>' + `<td>${email.recipients}</td>` + '</tr>' +
           '<tr>' + '<td>' + '<strong>Subject:</strong>' + '</td>' + `<td>${email.subject}</td>` + '</tr>' +
           '<tr>' + '<td>' + '<strong>Time:</strong>' + '</td>' + `<td>${email.timestamp}</td>` + '</tr>' +
           '</table>' + '<br>';
  }

  function get_message(email) {
    return '<br><strong>Message:</strong><br>' + `<p>${email.body}</p>` + '</div>';
  }
}

function change_archive(email) {
  
  // Change archive status
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  });

  let delay = 50; // in milliseconds
  setTimeout(function() {
    //your code to be executed after the delay
    document.querySelector('#inbox').click();
  }, delay);

}

function convert_new_line_to_br() {
  var txt;
  txt = document.querySelector('#compose-body').value;
  var text = txt.split('\n');
  var str = text.join('</br>');
  document.querySelector('#compose-body').value = str;
}

function convert_new_line_to_br(txt) {
  var text = txt.split('\n');
  var str = text.join('<br>');
  return str;
}

function convert_br_to_new_line(txt) {
  var text = txt.split('<br>');
  var str = text.join('\n');
  return str;
}