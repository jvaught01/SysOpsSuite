document.addEventListener("DOMContentLoaded", function () {
  // WebSocket connection setup
  const url = `ws://${window.location.host}/ws/search-socket-server/`;
  const searchSocket = new WebSocket(url);

  let currentPage = 1;
  const resultsPerPage = 10; // Adjust as needed
  let searchResults = [];
  const searchButton = document.getElementById("search-button");
  const searchInput = document.getElementById("search-query");

  searchSocket.onmessage = handleSearchResults;
  searchSocket.onclose = function () {
    console.log("WebSocket connection closed.");
  };

  function handleSearchResults(event) {
    const data = JSON.parse(event.data);
    console.log("Received data:", data);

    if (data.type === "search_results") {
      searchResults = data.results;
      currentPage = 1;
      updateTable();
      updatePageInfo();
    }
  }

  function sendSearchRequest(searchTerm, filter) {
    const message = {
      type: "search",
      search_term: searchTerm,
      filter: filter,
    };
    console.log("Sending search request:", message);
    searchSocket.send(JSON.stringify(message));
  }

  // Event listener for the search button click
  searchButton.addEventListener("click", function (e) {
    e.preventDefault();
    initiateSearch();
  });

  // Event listener for the Enter key press
  searchInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      // Check if Enter key is pressed
      e.preventDefault();
      initiateSearch();
    }
  });

  // Function to initiate the search
  function initiateSearch() {
    const searchTerm = searchInput.value;
    const filter = document.querySelector("select[name='filter']").value;

    if (searchTerm.trim() === "") {
      alert("Please enter a search term.");
      return;
    }

    sendSearchRequest(searchTerm, filter);
  }

  // Event listener for the clear button
  document
    .getElementById("clear-button")
    .addEventListener("click", function () {
      searchInput.value = "";
      document.querySelector("select[name='filter']").selectedIndex = 0;
      clearTable();
    });

  // Event listener for the previous page button
  document.getElementById("prev-page").addEventListener("click", function () {
    if (currentPage > 1) {
      currentPage--;
      updateTable();
      updatePageInfo();
    }
  });

  // Event listener for the next page button
  document.getElementById("next-page").addEventListener("click", function () {
    if (currentPage < Math.ceil(searchResults.length / resultsPerPage)) {
      currentPage++;
      updateTable();
      updatePageInfo();
    }
  });

  function updateTable() {
    const tableBody = document.querySelector("#results-tbody");
    tableBody.innerHTML = "";

    const start = (currentPage - 1) * resultsPerPage;
    const end = start + resultsPerPage;

    searchResults.slice(start, end).forEach((result) => {
      const row = document.createElement("tr");
      row.classList.add("text-gray-500");

      const categoryCell = document.createElement("td");
      categoryCell.classList.add(
        "border-t-0",
        "px-4",
        "align-middle",
        "text-sm",
        "font-normal",
        "whitespace-nowrap",
        "p-4",
        "text-left"
      );
      categoryCell.textContent = result.where;

      const lineCell = document.createElement("td");
      lineCell.classList.add(
        "border-t-0",
        "px-4",
        "align-middle",
        "text-xs",
        "font-medium",
        "text-gray-900",
        "whitespace-nowrap",
        "p-4"
      );
      lineCell.textContent = result.line;

      const hostnameCell = document.createElement("td");
      hostnameCell.classList.add(
        "border-t-0",
        "px-4",
        "align-middle",
        "text-xs",
        "font-medium",
        "text-gray-900",
        "whitespace-nowrap",
        "p-4"
      );
      hostnameCell.textContent = result.hostname;

      row.appendChild(categoryCell);
      row.appendChild(lineCell);
      row.appendChild(hostnameCell);

      tableBody.appendChild(row);
    });
  }

  function updatePageInfo() {
    document.getElementById(
      "page-info"
    ).textContent = `Page ${currentPage} of ${Math.ceil(
      searchResults.length / resultsPerPage
    )}`;
    document.getElementById("prev-page").disabled = currentPage === 1;
    document.getElementById("next-page").disabled =
      currentPage === Math.ceil(searchResults.length / resultsPerPage);
  }

  function clearTable() {
    const tableBody = document.querySelector("#results-tbody");
    tableBody.innerHTML = "";
  }
});
