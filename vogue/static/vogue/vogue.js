document.addEventListener('DOMContentLoaded', function() {

    // Call function
    loadBtn();
});

// Load like and edit buttons
function loadBtn() {
            
    // Get div elements
    const like_btns = document.getElementsByClassName('like-btn');

    // Iterate through div elements
    for (var i = 0; i < like_btns.length; i++) {

        // Save post id
        const id = like_btns[i].value;

        // Call functions
        loadLikeContent(id);

        // Like post on click
        like_btns[i].addEventListener('click', () => {
            like(id);
        })
    }
};

// Load like content
function loadLikeContent(id) {

    const liked = `<svg fill="#ed4956" height="16" viewBox="0 0 48 48" width="16"><path d="M34.6 3.1c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5s1.1-.2 1.6-.5c1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>`;
    const unliked = `<svg fill="#262626" height="16" viewBox="0 0 48 48" width="16"><path d="M34.6 6.1c5.7 0 10.4 5.2 10.4 11.5 0 6.8-5.9 11-11.5 16S25 41.3 24 41.9c-1.1-.7-4.7-4-9.5-8.3-5.7-5-11.5-9.2-11.5-16C3 11.3 7.7 6.1 13.4 6.1c4.2 0 6.5 2 8.1 4.3 1.9 2.6 2.2 3.9 2.5 3.9.3 0 .6-1.3 2.5-3.9 1.6-2.3 3.9-4.3 8.1-4.3m0-3c-4.5 0-7.9 1.8-10.6 5.6-2.7-3.7-6.1-5.5-10.6-5.5C6 3.1 0 9.6 0 17.6c0 7.3 5.4 12 10.6 16.5.6.5 1.3 1.1 1.9 1.7l2.3 2c4.4 3.9 6.6 5.9 7.6 6.5.5.3 1.1.5 1.6.5.6 0 1.1-.2 1.6-.5 1-.6 2.8-2.2 7.8-6.8l2-1.8c.7-.6 1.3-1.2 2-1.7C42.7 29.6 48 25 48 17.6c0-8-6-14.5-13.4-14.5z"></path></svg>`;
    
    // Fetch likes from API route
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(like => {
        // Update like count
        document.querySelector(`#c${id}`).innerHTML = `${like.count}`;
        // Update like button
        document.querySelector(`#l${id}`).innerHTML = (like.user_liked) ? liked : unliked;
    })
};

// Like or Unlike post
function like(id) {

    fetch(`/like/${id}`, {
        method: 'POST'
    })
    .then(result => {
        if (result.status == 200) {
            loadLikeContent(id);
        }
    })
};
