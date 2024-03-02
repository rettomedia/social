// Like Event
document.addEventListener('DOMContentLoaded', function() {
    var likeButtons = document.querySelectorAll('.like-button-main')
    likeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var postSlug = this.getAttribute('data-post-slug')
            var xhr = new XMLHttpRequest()

            xhr.open('POST', '/posts/like-post/' + postSlug + '/');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded')
            xhr.onload = function() {
                if (xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText)
                    if (response.message == "Post liked successfully.") {
                        var likesCountElement = document.getElementById('likes-count-' + postSlug)
                        likesCountElement.textContent = response.likes_count
                    } else {
                        alert(response.message)
                    }
                } else {
                    console.error(xhr.responseText)
                }
            }
            
            
            xhr.send()
        })
    })
})