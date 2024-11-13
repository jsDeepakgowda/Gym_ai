import streamlit as st
import cv2
from video_analysis import VideoAnalysis
import tempfile
import os

# Streamlit App Content
st.markdown('<div class="title">AI Fitness Trainer</div>', unsafe_allow_html=True)

# Step 1: Upload Video or Use Webcam Section
st.markdown('<div class="header">📹 Upload Your Workout Video or Use Webcam</div>', unsafe_allow_html=True)
video_file = st.file_uploader("Upload your workout video (MP4, MOV, AVI)", type=["mp4", "mov", "avi"])
exercise_type = st.selectbox("🏋️ Select Exercise Type", ["push-up", "pull-up", "squat", "sit-up", "walk"])

# Initialize session state variables for running status and control flags if not already present
if 'analysis_running' not in st.session_state:
    st.session_state.analysis_running = False
if 'stop_requested' not in st.session_state:
    st.session_state.stop_requested = False
if 'video_analyzer' not in st.session_state:
    st.session_state.video_analyzer = None

def stop_analysis():
    st.session_state.stop_requested = True
    st.session_state.analysis_running = False  # Mark analysis as stopped
    st.write("Debug: Stop analysis triggered")  # Debug log

# Step 2: Analyze Video Section (Real-time or Uploaded)
if video_file is not None:
    temp_dir = tempfile.gettempdir()
    video_path = os.path.join(temp_dir, video_file.name)
    with open(video_path, "wb") as f:
        f.write(video_file.read())

    if not st.session_state.analysis_running:
        if st.button("Start Video Analysis 💪"):
            st.session_state.analysis_running = True  # Start analysis
            st.session_state.stop_requested = False  # Reset stop flag
            stframe = st.empty()
            st.session_state.video_analyzer = VideoAnalysis(video_path)  # Initialize with video file path
            st.markdown('<div class="improvement-section"><h2>Analyzing Video...</h2></div>', unsafe_allow_html=True)

            with st.spinner("Processing... Please wait!"):
                # This loop will run for every frame processed
                for processed_frame in st.session_state.video_analyzer.analyze_video(exercise_type, stop_analysis_func=lambda: st.session_state.stop_requested):
                    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    stframe.image(frame_rgb, channels="RGB", use_column_width=True)

                    # Check if stop was requested in the middle of analysis
                    if st.session_state.stop_requested:
                        st.write("Debug: Stop requested in the loop")  # Debug log
                        break  # Stop analysis when button is pressed

            st.session_state.analysis_running = False  # Mark analysis as finished
            calories_burned, total_count = st.session_state.video_analyzer.get_summary()
            st.write(f"**Total Calories Burned:** {calories_burned:.2f} Kcal")
            st.write(f"**Total {exercise_type.capitalize()} Rep Count:** {total_count}")

    # Display the stop button
    if st.session_state.analysis_running:
        if st.button("Stop Analysis 🛑"):
            stop_analysis()  # Stop the analysis when clicked
            st.write("Analysis Stopped!")
            # Get final summary even if stopped
            calories_burned, total_count = st.session_state.video_analyzer.get_summary()
            st.write(f"**Total Calories Burned:** {calories_burned:.2f} Kcal")
            st.write(f"**Total {exercise_type.capitalize()} Rep Count:** {total_count}")

else:
    # Button to start webcam analysis
    if not st.session_state.analysis_running and st.button("Start Webcam Analysis 💪"):
        st.session_state.analysis_running = True  # Set the flag to running
        st.session_state.stop_requested = False  # Reset stop flag
        stframe = st.empty()
        st.session_state.video_analyzer = VideoAnalysis()  # Initialize for webcam usage
        st.markdown('<div class="improvement-section"><h2>Analyzing Live Video...</h2></div>', unsafe_allow_html=True)

        with st.spinner("Processing... Please wait!"):
            # This loop will run for every frame processed
            for processed_frame in st.session_state.video_analyzer.analyze_video(exercise_type, stop_analysis_func=lambda: st.session_state.stop_requested):
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                stframe.image(frame_rgb, channels="RGB", use_column_width=True)

                # Check if stop was requested in the middle of analysis
                if st.session_state.stop_requested:
                    st.write("Debug: Stop requested in the loop")  # Debug log
                    break  # Stop analysis when button is pressed

        st.session_state.analysis_running = False  # Mark analysis as finished
        calories_burned, total_count = st.session_state.video_analyzer.get_summary()
        st.write(f"**Total Calories Burned:** {calories_burned:.2f} Kcal")
        st.write(f"**Total {exercise_type.capitalize()} Rep Count:** {total_count}")

    if st.session_state.analysis_running:
        if st.button("Stop Analysis 🛑"):
            stop_analysis()  # Stop the analysis when clicked
            st.write("Analysis Stopped!")
            # Get final summary even if stopped
            calories_burned, total_count = st.session_state.video_analyzer.get_summary()
            st.write(f"**Total Calories Burned:** {calories_burned:.2f} Kcal")
            st.write(f"**Total {exercise_type.capitalize()} Rep Count:** {total_count}")
