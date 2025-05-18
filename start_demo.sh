#!/bin/bash

# Port to expose
PORT=8000

# Run Django server in the background in current terminal
echo "🚀 Starting Django server on 0.0.0.0:$PORT ..."
python manage.py runserver 0.0.0.0:$PORT &

# Get the PID so you can stop it later if needed
DJANGO_PID=$!

# Sleep briefly to allow Django to start
sleep 3

# Reverse port for all connected Android devices
echo "🔁 Setting up ADB reverse on all connected devices..."
adb devices | grep -v "List of devices" | grep "device" | cut -f1 | while read -r device; do
    echo "🔄 Reversing port $PORT for device $device"
    adb -s "$device" reverse tcp:$PORT tcp:$PORT
done

echo "✅ All devices can now access Django using http://127.0.0.1:$PORT or http://10.0.2.2:$PORT"
echo "🔚 Press Ctrl+C to stop the Django server..."

# Wait for Django process to exit so logs stay visible
wait $DJANGO_PID
