const record = document.querySelector(".record");
const output = document.querySelector(".output");

if (navigator.mediaDevices.getUserMedia) {
    
    let onMediaSetupSuccess = function (stream) {
        const mediaRecorder = new MediaRecorder(stream);
        let chunks = [];

        record.onclick = function() {
            if (mediaRecorder.state == "recording") {
                mediaRecorder.stop();
                record.classList.remove("btn-danger");
                record.classList.add("btn-primary");
            } else {
                mediaRecorder.start();
                record.classList.remove("btn-primary");
                record.classList.add("btn-danger");
            }
        }

        mediaRecorder.ondataavailable = function (e) {
            chunks.push(e.data);
        }

        mediaRecorder.onstop = function () {
            let blob = new Blob(chunks, {type: "audio/webm"});
            chunks = [];

            let formData = new FormData();
            formData.append("audio", blob);

            fetch("/transcribe", {
                method: "POST",
                body: formData
            }).then((response) => response.json())
            .then((data) => {
                output.innerHTML = data.output;
            })
        }
    }

    let onMediaSetupFailure = function(err) {
        alert(err);
    }   

    navigator.mediaDevices.getUserMedia({ audio: true}).then(onMediaSetupSuccess, onMediaSetupFailure);

} else {
    alert("getUserMedia is not supported in your browser!")
}