import json
from channels.generic.websocket import WebsocketConsumer
from .models import Task
from django.contrib.auth.models import User


class TaskConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "WebSocket connection established",
                }
            )
        )

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)

        # Check if 'task_id' exists and is relevant for the operations
        task = None
        if "task_id" in data:
            task_id = data["task_id"]
            task = Task.objects.get(id=task_id)

        if data["type"] == "update_task":
            # Ensure task is fetched
            if task:
                # Handle task update
                if data["title"] != "":
                    task.title = data["title"]
                if data["due_date"] != "":
                    task.due_date = data["due_date"]
                if data["description"] != "":
                    task.description = data["description"]
                task.save()

                # Broadcast the updated task to all connected clients
                self.send(
                    text_data=json.dumps(
                        {
                            "type": "task_update",
                            "task_id": task.id,
                            "title": task.title,
                            "due_date": str(task.due_date),
                        }
                    )
                )

        elif data["type"] == "complete_task":
            # Ensure task is fetched
            if task:
                task.completed = data["completed"]
                task.save()

                self.send(
                    text_data=json.dumps(
                        {
                            "type": "complete_task",
                            "task_id": task.id,
                            "completed": task.completed,
                        }
                    )
                )

        elif data["type"] == "create_task":
            title = data["title"]
            due_date = data["due_date"]
            description = data["description"]
            user_id = int(data["user_id"])
            try:
                created_by = User.objects.get(id=user_id)  # Fetch the User instance
            except User.DoesNotExist:
                print(f"User with id {user_id} does not exist.")
                return

            task = Task.objects.create(
                title=title,
                due_date=due_date,
                description=description,
                created_by=created_by,
            )
            task.save()

            self.send(
                text_data=json.dumps(
                    {
                        "type": "create_task",
                        "task_id": task.id,
                        "title": task.title,
                        "due_date": str(task.due_date),
                        "description": task.description,
                    }
                )
            )

        elif data["type"] == "delete_task":
            # Ensure task is fetched
            if task:
                task.delete()

                self.send(
                    text_data=json.dumps(
                        {"type": "delete_task", "message": "Task deleted successfully"}
                    )
                )
