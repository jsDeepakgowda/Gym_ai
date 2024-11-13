function startAnalysis() {
    const videoMode = document.getElementById('video_mode').value;
    const exerciseType = document.getElementById('exercise_type').value;

    const formData = new FormData();
    formData.append('exercise_type', exerciseType);
    formData.append('video_mode', videoMode);

    if (videoMode === 'upload') {
        const videoFile = document.getElementById('video_file').files[0];
        formData.append('video_file', videoFile);
    }

    fetch('/start_analysis', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          if (data.status === "Analysis started") {
              document.getElementById('video-feed').src = `/video_feed?exercise_type=${exerciseType}`;
          } else {
              alert("Failed to start analysis.");
          }
      });
}

function stopAnalysis() {
    fetch('/stop_analysis', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
          if (data.error) {
              alert(data.error);
          } else {
              // Update final results in the summary section
              document.getElementById('final-calories').innerText = `Total Calories Burned: ${data.calories_burned}`;
              document.getElementById('final-count').innerText = `Total Rep Count: ${data.total_count}`;

              // Display the result-summary section with the final results
              document.getElementById('result-summary').style.display = 'block';

              // Clear the video feed
              document.getElementById('video-feed').src = '';
          }
      }).catch(error => {
          console.error("Error stopping analysis:", error);
      });
}

// Show/Hide video file upload input based on mode
document.getElementById('video_mode').addEventListener('change', (event) => {
    const uploadSection = document.getElementById('upload_section');
    uploadSection.style.display = event.target.value === 'upload' ? 'block' : 'none';
});
