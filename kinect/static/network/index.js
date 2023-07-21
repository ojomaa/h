document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#submit-post').addEventListener('click', newpost)
});

function newpost() {
    fetch('/new_post', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#compose-body').value,
        })
      })
    .then(response => {
        console.log(response)
        return response.json()
    })
    .then(result => {
        console.log('Response Body:', result);
    })
}