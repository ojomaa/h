document.addEventListener('DOMContentLoaded', function () {
    console.log('Script is running!');
    document.querySelector('#follow-toggle').addEventListener('click', follow);
    }
);

function follow(request) {
    const user=  document.querySelector('#username').textContent;
    fetch(`/follow/${user}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        // Update the button text based on whether the user followed or unfollowed
        const followButton = document.querySelector('#follow-toggle');
        if (result.followed) {
            followButton.textContent = 'Unfollow';
        } else {
            followButton.textContent = 'Follow';
        }
        // Update the follower count in JavaScript
        const followerCount = document.querySelector('#follower-count');
        followerCount.textContent = result.followers;
    })
}