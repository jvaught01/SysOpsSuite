import json
import logging
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from main import process_backup_files

# Set up logging
logger = logging.getLogger(__name__)


class TriggerConsumer(WebsocketConsumer):
    def connect(self):
        # Accept the WebSocket connection
        self.accept()
        logger.debug("WebSocket connection established.")
        self.send(
            json.dumps(
                {
                    "type": "connection_established",
                    "message": "WebSocket connection established for triggers.",
                }
            )
        )

    def disconnect(self, close_code):
        # Log disconnection details
        logger.debug(f"WebSocket connection closed with code {close_code}.")
        print(f"WebSocket connection closed with code {close_code}.")

    def receive(self, text_data):
        """
        Handles incoming messages from the WebSocket.
        If 'start_backup_process' command is received, initiate the backup process.
        """
        data = json.loads(text_data)
        logger.debug(f"Received data: {data}")

        if data.get("command") == "start_backup_process":
            # Start the backup processing function when the correct command is received
            self.start_backup_process()

    def start_backup_process(self):
        """
        Executes the backup processing function and updates the client via WebSocket.
        """

        def update_progress(progress):
            """
            Callback to send progress updates to the client via WebSocket.
            The progress value is rounded to avoid decimals.
            """
            rounded_progress = round(progress)
            logger.debug(f"Sending progress: {rounded_progress}%")
            self.send(
                json.dumps({"type": "progress_update", "progress": rounded_progress})
            )

        # Call the backup processing function and send progress updates
        logger.debug("Starting backup processing...")
        process_backup_files(progress_callback=update_progress)

        # Ensure we send 100% at the end
        update_progress(100)

        # Once the process is complete, notify the client
        self.send(
            json.dumps(
                {
                    "type": "process_complete",
                    "message": "Backup processing completed. Please check backup status or search configs in config search.",
                }
            )
        )
        logger.debug("Backup processing completed.")
