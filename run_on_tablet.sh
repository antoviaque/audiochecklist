#!/bin/bash

buildozer -v android deploy run logcat | grep python
