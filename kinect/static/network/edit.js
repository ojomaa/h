document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('posts').addEventListener('click', (event) => {
        const target = event.target;
        if (target.classList.contains('like-toggle')) {
            like(event);
        } else if (target.classList.contains('edit')) {
            edit(event);
        }
    });
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
                console.log(updatedBody)

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
                    if (update && update.user && update.body) {
                        card.innerHTML = `
                            <a class="nav-link" href="/profile/${result.user}"> ${result.user} </a>
                            <p class="card-text">${update.body}</p>
                            <p class= "likes"> ${update.likes} Likes</p>
                            ${update.liked ? '<button class="like-toggle">Unlike</button>' : '<button class="like-toggle">Like</button>'}
                            <button class="edit" type="button"> Edit Post </button>`
                    }     
                })
                .catch(error => {
                    console.error('Error updating post body:', error)});
                
            });
    })
}

function like(event) {
    const card = event.target.closest('.card')
    const id= card.id
    fetch(`/like/${id}`, {
        method: 'POST'
    })
    .then(response => {
        console.log(response)
        return response.json()
    })
    .then(result => {
        console.log(result);
        // Update the button text based on whether the user liked or unliked
        const likeButton = card.querySelector(`.like-toggle`);
        if (result.liked) {
            likeButton.textContent = 'Unlike';
        } else {
            likeButton.textContent = 'Like';
        }
        // Update the likes in HTML
        const likes = card.querySelector('.likes');
        likes.textContent = `${result.likes} Likes`

    })
}