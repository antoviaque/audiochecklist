Audio Checklist
===============

## Install

System dependencies:
```
sudo apt install ffmpeg libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev \
libavutil-dev libswscale-dev libswresample-dev libpostproc-dev libsdl2-dev libsdl2-2.0-0 \
libsdl2-mixer-2.0-0 libsdl2-mixer-dev python3-dev poetry default-jre default-jdk ccache \
autoconf libtool
```

Python dependencies:

```
$ poetry install
```

Download `google-api-auth-text2speech.json` service account auth file from
Google Cloud Console.

Copy `audiochecklist.cfg.sample` to `audiochecklist.cfg` and set the values
