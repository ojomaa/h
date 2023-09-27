document.addEventListener('DOMContentLoaded', function () {
    const edit_button = document.querySelectorAll('.edit');
    edit_button.forEach(button => button.addEventListener('click', edit))
    }
);

function edit(event) {

    // Get the post ID
    const card = event.target.closest('.card')
    const id= card.id

    // Update the HTML to the edit HTML
    fetch(`/post/${id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result)
        card.innerHTML= `
        <p>${result.user}</p>
        <textarea></textarea>
        <button class="save">Save</button>
        `
        // Save the new body
        const saveButton = card.querySelector('.save');
            saveButton.addEventListener('click', () => {
                const updatedBody = card.querySelector('textarea').value;

                fetch(`/post/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        body:updatedBody
                    })
                })
                .then(response => {
                    console.log(response)
                    return response.json()
                })
                .then(update => {
                    console.log(update)
                    card.innerHTML = `
                    <h6 class="card-subtitle mb-2 text-muted"> ${update.user} </h6>
                    <p class="card-text"> ${update.body} </p>
                    {% if request.user == p.user %}
                        <button id="edit" type="button" class="btn btn-light"> Edit Post </button>
                    {% endif %}
                    `
                })
                .catch(error => {
                    console.error('Error updating post body:', error)});
                
            });
    })
}