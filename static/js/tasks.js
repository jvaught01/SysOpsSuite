document.addEventListener("DOMContentLoaded", function () {
  // WebSocket connection setup
  let url = `ws://${window.location.host}/ws/socket-server/`;
  const taskSocket = new WebSocket(url);

  // Handle WebSocket message
  taskSocket.onmessage = receiveTaskUpdate;

  // WebSocket message handling function
  function receiveTaskUpdate(event) {
    const data = JSON.parse(event.data);

    if (data.type === "task_update") {
      const taskId = data.task_id;
      const taskTitle = data.title;
      const taskDueDate = data.due_date;
      const description = data.description;

      // Update task title, due date, and description dynamically
      updateTaskElements(taskId, taskTitle, taskDueDate, description);
    }

    if (data.type === "create_task") {
      const taskId = data.task_id;
      const taskTitle = data.title;
      const taskDueDate = data.due_date;
      const description = data.description;

      // Add the new task to the DOM
      addNewTaskElement(taskId, taskTitle, taskDueDate, description);
    }
  }

  // Function to update task elements
  function updateTaskElements(taskId, taskTitle, taskDueDate, description) {
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

    const descriptionElement = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='description']`
    );
    if (descriptionElement) {
      descriptionElement.textContent = `Description: ${description}`;
    }
  }

  // Delete Task Function
  function deleteTask(taskId) {
    const taskDeleteData = {
      type: "delete_task",
      task_id: taskId,
    };
    console.log(taskId);

    taskSocket.send(JSON.stringify(taskDeleteData));
    deleteTaskElements(taskId);
  }

  // Add New Task Element Function
  function addNewTaskElement(taskId, taskTitle, taskDueDate, description) {
    const taskContainer = document.createElement("div");
    taskContainer.classList.add(
      "task-container",
      "mb-5",
      "p-5",
      "bg-white",
      "shadow",
      "rounded-2xl",
      "flex",
      "flex-col",
      "md:flex-row",
      "items-start",
      "md:items-center",
      "justify-between"
    );
    taskContainer.setAttribute("data-task-id", taskId);

    taskContainer.innerHTML = `
      <div class="flex-1 mb-4 md:mb-0">
        <h1 class="text-xl md:text-2xl font-bold mb-2 md:mb-0" data-task-id="${taskId}" data-task-field="title">${taskTitle}</h1>
        <div class="text-gray-500 text-sm">
          Due Date: <span data-task-id="${taskId}" data-task-field="due-date">${taskDueDate}</span><br />
          Description: <span data-task-id="${taskId}" data-task-field="description">${description}</span>
        </div>
      </div>
      <div class="flex items-center gap-4 mt-4 md:mt-0">
        <form method="post">
          <input type="checkbox" onclick="completeTask(${taskId})" class="shrink-0 mt-0.5 border-gray-200 rounded text-blue-600 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none" id="task-complete-${taskId}" data-task-id="${taskId}" data-complete="False" />
          <label for="task-complete-${taskId}" class="text-sm text-gray-500">Task Complete</label>
        </form>
        <button type="button" class="editTaskButton inline-flex items-center justify-center h-9 px-4 md:px-6 rounded-xl bg-gray-900 text-white text-sm font-semibold transition-all duration-200" data-task-id="${taskId}">
          Edit Task
        </button>
        <button type="button" class="deleteTaskButton inline-flex items-center justify-center h-9 px-4 md:px-6 rounded-xl bg-red-600 text-white text-sm font-semibold transition-all duration-200" data-task-id="${taskId}">
        <!-- Trashcan Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.137 21H7.863a2 2 0 01-1.996-1.858L5 7m5 4v6m4-6v6M1 3h22M4 7h16"></path>
        </svg>
      </button>
      </div>
    `;

    // Insert the new task container before the "Create New Task" button
    const taskListContainer = document.getElementById("taskListContainer");
    if (taskListContainer) {
      taskListContainer.appendChild(taskContainer);
    }

    // Add event listener for the new edit button
    const editButton = taskContainer.querySelector(".editTaskButton");
    if (editButton) {
      editButton.addEventListener("click", function () {
        const taskId = this.getAttribute("data-task-id");
        document.getElementById("editTaskId").value = taskId;
        openModal("editModal");
      });
    }

    // Add event listener for the new delete button
    const deleteButton = taskContainer.querySelector(".deleteTaskButton");
    if (deleteButton) {
      deleteButton.addEventListener("click", function () {
        const taskId = this.getAttribute("data-task-id");
        deleteTask(taskId);
      });
    }
  }

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

  // Set up event listeners for buttons if they exist
  const createTaskButton = document.getElementById("createTaskButton");
  if (createTaskButton) {
    createTaskButton.addEventListener("click", () =>
      openModal("createTaskModal")
    );
  }

  const closeEditModalButton = document.getElementById("closeEditModal");
  if (closeEditModalButton) {
    closeEditModalButton.addEventListener("click", () =>
      closeModal("editModal")
    );
  }

  const closeCreateModalButton = document.getElementById("closeCreateModal");
  if (closeCreateModalButton) {
    closeCreateModalButton.addEventListener("click", () =>
      closeModal("createTaskModal")
    );
  }

  // Form submission handler for creating a new task
  const createTaskForm = document.getElementById("createTaskForm");
  if (createTaskForm) {
    console.log("Form found:", createTaskForm);
    createTaskForm.addEventListener("submit", function (e) {
      e.preventDefault();

      // Collect form data
      const userId = this.getAttribute("data-user-id");
      const taskTitle = document.getElementById("newTaskTitle").value;
      const taskDescription =
        document.getElementById("newTaskDescription").value;
      const taskDueDate = document.getElementById("newTaskDueDate").value;
      console.log("Task Title:", taskTitle);

      // Create a data object to send
      const taskCreateData = {
        type: "create_task",
        user_id: userId,
        title: taskTitle,
        description: taskDescription,
        due_date: taskDueDate,
      };

      // Send data over WebSocket
      console.log("Sending data over WebSocket");
      taskSocket.send(JSON.stringify(taskCreateData));
      closeModal("createTaskModal");
    });
  }

  // Form submission handler for editing an existing task
  const editForm = document.getElementById("editForm");
  if (editForm) {
    editForm.addEventListener("submit", function (e) {
      e.preventDefault();

      const taskId = document.getElementById("editTaskId").value;
      const taskTitle = document.getElementById("taskTitle").value;
      const taskDueDate = document.getElementById("taskDueDate").value;
      const taskDescription = document.getElementById("taskDescription").value;

      // Create a data object to send
      const taskUpdateData = {
        type: "update_task",
        task_id: taskId,
        title: taskTitle,
        due_date: taskDueDate,
        description: taskDescription,
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

  function deleteTaskElements(taskId) {
    const taskContainer = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='container']`
    );
    if (taskContainer) {
      taskContainer.remove();
    }
  }

  // Cross Task (line-through)
  function crossTask(taskId) {
    const taskTitleElement = document.querySelector(
      `[data-task-id='${taskId}'][data-task-field='title']`
    );
    if (taskTitleElement) {
      taskTitleElement.style.textDecoration = "line-through";
    }
  }

  // Run on page load to cross out completed tasks
  document.querySelectorAll("[data-complete='true']").forEach((checkbox) => {
    const taskId = checkbox.getAttribute("data-task-id");
    crossTask(taskId);
  });
});
