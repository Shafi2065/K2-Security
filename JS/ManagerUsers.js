const deleteButton = document.getElementById("deleteButton");
            deleteButton.addEventListener("click", () => {

                const employeeId = deleteButton.getAttribute("data-employee-id");
                fetch(`/employees/${employeeId}`, {
                    method: 'DELETE'
                })
                        .then(response => {
                            if (response.ok) {
                                console.log('Employee record deleted.');
                            } else {
                                console.error('Error deleting employee record.');
                            }
                        })
                        .catch(error => {
                            console.error('Network error:', error);
                        });
            });
            const addButton = document.getElementById("addButton");
            addButton.addEventListener("click", () => {
                // Get the table body
                const tableBody = document.querySelector("tbody");

                // Create a new row
                const newRow = tableBody.insertRow(-1);

                // Add cells to the row with the user details
                const cell1 = newRow.insertCell(0);
                const cell2 = newRow.insertCell(1);
                const cell3 = newRow.insertCell(2);
                const cell4 = newRow.insertCell(3);
                const cell5 = newRow.insertCell(4);
                const cell6 = newRow.insertCell(5);
                const cell7 = newRow.insertCell(6);
                const cell8 = newRow.insertCell(7);

                cell1.innerHTML = tableBody.rows.length - 1;
                cell2.innerHTML = "John";
                cell3.innerHTML = "Doe";
                cell4.innerHTML = "1234567890";
                cell5.innerHTML = "newuser@example.com";
                cell6.innerHTML = "Employee";
                cell7.innerHTML = '<button type="button" class="btn btn-success">Edit</button>';
                cell8.innerHTML = '<button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#DeleteModal" data-employee-id="5">Delete</button>';
            });
            const editButtons = document.querySelectorAll('.edit-btn');

            editButtons.forEach((button) => {
                button.addEventListener('click', () => {
                    const employeeId = button.getAttribute('data-employee-id');

                    // Retrieve employee data from server using employeeId
                    fetch(`/employees/${employeeId}`)
                            .then(response => response.json())
                            .then(employeeData => {
                                // Populate the edit form with employeeData
                                // Display the edit form to the user

                                // Add table-primary class to the parent row
                                const parentRow = button.parentElement.parentElement;
                                parentRow.classList.add('table-primary');
                            })
                            .catch(error => {
                                console.error('Error retrieving employee data:', error);
                            });
                });
            });