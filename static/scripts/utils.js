const shareButton = document.querySelector('#shareButton');

shareButton.addEventListener('click', () => {
    const shareInput = document.querySelector('#shareInput');
    let value = shareInput.value;
    shareInput.select();
    shareInput.setSelectionRange(0,99999);

    navigator.clipboard.writeText(value);
    alert('Link copied.')
})