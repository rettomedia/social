// Like Event
document.addEventListener('DOMContentLoaded', function () {
    var likeButtons = document.querySelectorAll('.like-button-main');

    likeButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var postSlug = this.getAttribute('data-post-slug');
            var xhr = new XMLHttpRequest();

            xhr.open('POST', '/posts/like-post/' + postSlug + '/');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

            xhr.onload = function () {
                if (xhr.status == 200) {
                    var response = JSON.parse(xhr.responseText);
                    var likesCountElement = document.getElementById('likes-count-' + postSlug);

                    if (response.message === "Post liked successfully.") {
                        likesCountElement.textContent = response.likes_count;
                        button.classList.add('liked'); // Beğenildiğini göstermek için sınıf ekleyelim
                    } else if (response.message === "Post unliked successfully.") {
                        likesCountElement.textContent = response.likes_count;
                        button.classList.remove('liked'); // Beğeni kaldırıldığında sınıfı kaldıralım
                    }
                } else {
                    console.error(xhr.responseText);
                }
            };

            xhr.send();
        });
    });
});
