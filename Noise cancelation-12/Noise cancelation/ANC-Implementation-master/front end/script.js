document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('https://stackoverflow.com/questions/38344129/php-file-upload-to-localhost', { // Change port/endpoint as needed
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        document.getElementById('message').innerText = result.message;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').innerText = 'Error processing the file.';
    }
});
