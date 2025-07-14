from webpush import send_user_notification
import json

def send_push_notification(user, title, message, url="/"):
    payload = {
        "head": title,
        "body": message,
        "url": url
    }

    print(" Payload to send:")
    print(json.dumps(payload, indent=4)) 

    try:
        send_user_notification(
            user=user,
            payload=json.dumps(payload),
            ttl=1000
        )
        print(f" Push notification sent to {user.username}")
    except Exception as e:
        print(f" Error sending push notification to {user.username}: {e}")