const client = filestack.init(FILESTACK_APP_KEY);
const options = {
    maxFiles: FILESTACK_MAX_FILES,
    fromSources: FILESTACK_SOURCES,
    onUploadDone: function(data) {
        for (file of data.filesUploaded) {
            let input = document.createElement("input");
            input.setAttribute("type", "hidden");
            input.setAttribute("name", "file-upload");
            input.setAttribute("value", JSON.stringify(file));
            document.getElementById("filestack-handles").appendChild(input);

            let li = document.createElement("li");
            li.innerText = file.filename;
            document.getElementById("uploaded-filenames").appendChild(li);
        }
    }
}

document.getElementById("upload-btn").addEventListener("click", function(event) {
    event.preventDefault();
    client.picker(options).open();
})

