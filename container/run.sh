#!/bin/bash

exec huey_consumer.py scheduler.huey &
exec python notification_telegram.py
