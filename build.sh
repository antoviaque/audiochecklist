#!/bin/bash

# Generate the audio files for the current checklist
./build_audio.sh

# Build the Android APK
buildozer -v android debug 
