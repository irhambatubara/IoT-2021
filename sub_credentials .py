#
# Example pub/sub subscribe pull version program
#
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from concurrent.futures import TimeoutError

#Project ID of Topic
PROJECT_ID = "iot-2021-tim-01"
# Subscription ID to subscribe to
SUBSCRIPTION_ID = "coba_baca"

# Credentials file
#GOOGLE_APPLICATION_CREDENTIALS_PATH = "/home/rahmad/workspace/Hardware-Software/pub-sub/latihan_service_account.json"
GOOGLE_APPLICATION_CREDENTIALS_PATH = "C:/Users/irham batubara/Documents/iot 2021/contoh kode/tes.json"
# Create credentials object
credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS_PATH)

# Callback function, called when a message arrives
def callback(message):
    # Do somwething with the message
    print(f"Message received:")
    print(f"{message}.")

    # Need to acknowledge receipt, if not will be resent
    message.ack()

# Create a subscriber client to access pub/sub service
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

# Create subscription object
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

# Subscribe (start receiving message) and give it the callback function name that will process incoming message
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

try:
    # Blocking event to wait, need to do this so it won't immediately end example program without receiving message
    streaming_pull_future.result(timeout=5)
except TimeoutError as err:
    # Exception when wait has timeout
    streaming_pull_future.cancel()
    print(f"Exception: {err}.")

# End subscription (stop receiving message)
subscriber.close()

