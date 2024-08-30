document.addEventListener("DOMContentLoaded", function () {
  let url = `ws://${window.location.host}/ws/socket-server/`;

  const taskSocket = new WebSocket(url);

  taskSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);
  };

  // Modal Toggle Functions
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove("hidden"); // Show modal
    }
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add("hidden"); // Hide modal
    }
  }

  // Delete Task Function
  function deleteTask() {
    const taskId = document
      .getElementById("deleteTaskButton")
      .getAttribute("data-task-id");

    const taskDeleteData = {
      type: "delete_task",
      task_id: taskId,
    };

    taskSocket.send(JSON.stringify(taskDeleteData));
    deleteTaskElements(taskId);
  }

  // Check if elements exist before adding event listeners
  const editTaskButton = document.getElementById("editTaskButton");
  const closeEditModalButton = document.getElementById("closeEditModal");
  const createTaskButton = document.getElementById("createTaskButton");
  const closeCreateModalButton = document.getElementById("closeCreateModal");
  const deleteTaskButton = document.getElementById("deleteTaskButton");

  if (editTaskButton) {
    editTaskButton.addEventListener("click", () => {
      openModal("editModal");
    });
  }

  if (closeEditModalButton) {
    closeEditModalButton.addEventListener("click", () => {
      closeModal("editModal");
    });
  }

  if (createTaskButton) {
    createTaskButton.addEventListener("click", () => {
      openModal("createTaskModal");
    });
  }

  if (closeCreateModalButton) {
    closeCreateModalButton.addEventListener("click", () => {
      closeModal("createTaskModal");
    });
  }

  if (deleteTaskButton) {
    document
      .getElementById("deleteTaskButton")
      .addEventListener("click", () => deleteTask());
  }

  // Form submission handler for creating a new task
  const createTaskForm = document.getElementById("createTaskForm");
  if (createTaskForm) {
    createTaskForm.addEventListener("submit", function (e) {
      e.preventDefault();

      // Collect form data
      const userId = this.getAttribute("data-user-id");
      const taskTitle = document.getElementById("newTaskTitle").value;
      const taskDescription =
        document.getElementById("newTaskDescription").value;
      const taskDueDate = document.getElementById("newTaskDueDate").value;

      // Create a data object to send
      const taskCreateData = {
        type: "create_task",
        user_id: userId,
        title: taskTitle,
        description: taskDescription,
        due_date: taskDueDate,
      };

      // Send data over WebSocket
      taskSocket.send(JSON.stringify(taskCreateData));

      // Close modal without refreshing page
      closeModal("createTaskModal");
    });
  }

  // Form submission handler for editing an existing task
  const editForm = document.getElementById("editForm");
  if (editForm) {
    editForm.addEventListener("submit", function (e) {
      e.preventDefault();

      // Collect form data
      const taskId = document
        .getElementById("editTaskButton")
        .getAttribute("data-task-id");
      const taskTitle = document.getElementById("taskTitle").value;
      const taskDescription = document.getElementById("taskDescription").value;
      const taskDueDate = document.getElementById("taskDueDate").value;

      // Create a data object to send
      const taskUpdateData = {
        type: "update_task",
        task_id: taskId,
        title: taskTitle,
        description: taskDescription,
        due_date: taskDueDate,
      };

      // Send data over WebSocket
      taskSocket.send(JSON.stringify(taskUpdateData));
      closeModal("editModal");
    });
  }

  // Complete Task Function
  window.completeTask = (taskId) => {
    const checkbox = document.querySelector(`#task-complete-${taskId}`);
    const taskTitleElement = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='title']`
    );

    if (checkbox.checked) {
      crossTask(taskId);
    } else {
      if (taskTitleElement) {
        taskTitleElement.style.textDecoration = "none";
      }
    }

    const taskCompleteData = {
      type: "complete_task",
      task_id: taskId,
      completed: checkbox.checked,
    };

    taskSocket.send(JSON.stringify(taskCompleteData));
  };

  // Cross Task (line-through)
  function crossTask(taskId) {
    const taskTitleElement = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='title']`
    );
    if (taskTitleElement) {
      taskTitleElement.style.textDecoration = "line-through";
    }
  }

  // Update Task Elements on WebSocket message
  function receiveTaskUpdate(event) {
    const data = JSON.parse(event.data);

    if (data.type === "task_update") {
      const taskId = data.task_id;
      const taskTitle = data.title;
      const taskDueDate = data.due_date;

      // Update task title and due date dynamically
      updateTaskElements(taskId, taskTitle, taskDueDate);
    }
  }

  function updateTaskElements(taskId, taskTitle, taskDueDate) {
    const titleElement = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='title']`
    );
    if (titleElement) {
      titleElement.textContent = taskTitle;
    }

    const dueDateElement = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='due-date']`
    );
    if (dueDateElement) {
      dueDateElement.textContent = `Due Date: ${taskDueDate}`;
    }
  }

  function deleteTaskElements(taskId) {
    const taskContainer = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='container']`
    );
    cloneTaskContainer = taskContainer.cloneNode(true);
    if (taskContainer) {
      taskContainer.style.display = "none";
      cloneTaskContainer.innerHTML = `<h2 class="text-xl font-bold mb-4">No Tasks Today!</h2>`;
      taskContainer.parentNode.replaceChild(cloneTaskContainer, taskContainer);
    }
  }

  // Handle WebSocket message
  taskSocket.onmessage = receiveTaskUpdate;

  // Run on page load to cross out completed tasks
  document.querySelectorAll("[data-complete='true']").forEach((checkbox) => {
    const taskId = checkbox.getAttribute("data-task-id");
    crossTask(taskId);
  });
});
