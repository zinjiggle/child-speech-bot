var audio_context, recorder, volume, volumeLevel = 0, currentEditedSoundIndex;

function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  console.log('Media stream created.');

  volume = audio_context.createGain();
  volume.gain.value = volumeLevel;
  input.connect(volume);
  volume.connect(audio_context.destination);
  console.log('Input connected to audio context destination.');

  recorder = new Recorder(input);
  console.log('Recorder initialised.');
}

function changeVolume(value) {
  if (!volume) return;
  volumeLevel = value;
  volume.gain.value = value;
}

function startRecording(button) {
  recorder && recorder.record();
  console.log('Recording...');
}

function stopRecording(button) {
  recorder && recorder.stop();
  console.log('Stopped recording.');

  // create WAV download link using audio data blob
  createDownloadLink();

  recorder.clear();
}

function createDownloadLink() {
  currentEditedSoundIndex = -1;
  recorder && recorder.exportWAV(handleWAV.bind(this));
}

function handleWAV(blob) {
  var tableRef = document.getElementById('recordingslist');
  if (currentEditedSoundIndex !== -1) {
    $('#recordingslist tr:nth-child(' + (currentEditedSoundIndex + 1) + ')')
        .remove();
  }

  var url = URL.createObjectURL(blob);
  var newRow = tableRef.insertRow(currentEditedSoundIndex);
  newRow.className = 'soundBite';
  var audioElement = document.createElement('audio');
  var downloadAnchor = document.createElement('a');

  audioElement.controls = true;
  audioElement.src = url;

  downloadAnchor.href = url;
  downloadAnchor.download = new Date().toISOString() + '.wav';
  downloadAnchor.innerHTML = 'Download';
  downloadAnchor.className = 'btn btn-primary';

  var newCell = newRow.insertCell(-1);
  newCell.appendChild(audioElement);
  newCell = newRow.insertCell(-1);
  newCell.appendChild(downloadAnchor);

  /* Send blob to server and display response text. */
  var fd = new FormData();
  fd.append('fname', 'test.wav');
  fd.append('data', blob);
  $.ajax({
     type: 'POST',
     url: 'upload',
     data: fd,
     processData: false,
     contentType: false,
   }).done(function(data) {
    var newCell = newRow.insertCell(-1);
    var textElement = document.createElement('p');
    textElement.innerHTML = data;
    newCell.appendChild(textElement);
  });
  /**************************************************/
}

window.onload = function init() {
  try {
    // webkit shim
    window.AudioContext = window.AudioContext || window.webkitAudioContext ||
        window.mozAudioContext;
    navigator.getUserMedia = navigator.getUserMedia ||
        navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    window.URL = window.URL || window.webkitURL || window.mozURL;

    audio_context = new AudioContext();
    console.log('Audio context set up.');
    console.log(
        'navigator.getUserMedia ' +
        (navigator.getUserMedia ? 'available.' : 'not present!'));
  } catch (e) {
    console.warn('No web audio support in this browser!');
  }

  navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
    console.warn('No live audio input: ' + e);
  });
};
