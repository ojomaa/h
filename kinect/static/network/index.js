document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#submit-post').addEventListener('click', newpost)
    }
);

function newpost(event) {
    event.preventDefault();

    // Capture the current value of the compose-body textarea
    const composeBodyValue = document.querySelector('#compose-body').value;

    // Make the fetch request
    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            body: composeBodyValue,
        })
    })
    .then(response => {
        console.log(response);
        return response.json();
    })
    .then(result => {
        console.log('Response Body:', result);
        document.querySelector('#compose-body').value = '';
    });
}

function allposts() {
    fetch('')
}