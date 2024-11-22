import paypalrestsdk
import logging

paypalrestsdk.configure({
    "mode": "sandbox",  # Cambia a "live" para producción
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

logging.basicConfig(level=logging.INFO)
