
     // Start with first post.
        let counter = 0;
        // Load posts 10 at a time.
        // When DOM loads, render the first 10 posts.
        document.addEventListener('DOMContentLoaded', load);

        // If hide button is clicked, delete the post.
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.className === 'hide') {
                console.log('clicked');
                element.parentElement.style.animationPlayState = 'running';
                element.parentElement.addEventListener('animationend', () =>  {
                    element.parentElement.remove();
                });
            }
        });

        // Load next set of posts.
        function load() {

            // Set start and end post numbers, and update counter.
            const start = counter;
            //const end = start + quantity - 1;
            counter+= 10;

            // Open new request to get new posts.
            const request = new XMLHttpRequest();
            request.open('POST', '/pastposts');
            request.onload = () => {
                const data = JSON.parse(request.responseText);
                console.log(data);
                data.forEach(add_post);
            };

            // Add start and end points to request data.
            const data = new FormData();
            data.append('start', start);
            console.log(start);

            // Send request.
            request.send(data);
        };

        // Add a new post with given contents to DOM.
        const post_template = Handlebars.compile(document.querySelector('#post').innerHTML);
        function add_post(contents) {
            // Create new post.
            const post = post_template({'name': contents.name,'contents': contents.text,'extra': contents.timestamp,});
            
            // Add post to DOM.
            document.querySelector('#pastPosts').innerHTML+= post;
        }
