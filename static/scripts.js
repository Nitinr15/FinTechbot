    // document.addEventListener("DOMContentLoaded", function() {
    //     const chatForm = document.getElementById("chatForm");
    //     const fileInput = document.getElementById("file");
    //     const messageContainer = document.getElementById("messageContainer");

    //     // Function to display loader
    //     function showLoader() {
    //         const loader = document.createElement("div");
    //         loader.className = "loader";
    //         messageContainer.appendChild(loader);
    //         autoScroll();
    //     }

    //     // Function to remove loader
    //     function hideLoader() {
    //         const loader = document.querySelector(".loader");
    //         if (loader) {
    //             loader.remove();
    //         }
    //         autoScroll(); // Ensure scrolling after removing loader
    //     }

    //     // Function to display message
    //     function showMessage(text, align = "left") {
    //         const messageBox = document.createElement("div");
    //         messageBox.className = `message-box message-${align}`;
    //         messageBox.textContent = text;
    //         messageContainer.appendChild(messageBox);
    //         autoScroll();
    //     }

    //     // Function to simulate typing
    //     function typeResponse(text, element) {
    //         const words = text.split(' ');
    //         let index = 0;

    //         function addWord() {
    //             if (index < words.length) {
    //                 element.textContent += words[index] + ' ';
    //                 index++;
    //                 setTimeout(addWord, 100);  // Adjust typing speed here (in milliseconds)
    //             } else {
    //                 autoScroll(); // Ensure scrolling after typing is complete
    //             }
    //         }

    //         addWord();
    //     }

    //     // Auto scroll function
    //     function autoScroll() {
    //         messageContainer.scrollTop = messageContainer.scrollHeight;
    //     }

    //     // Handle file upload
    //     fileInput.addEventListener("change", function() {
    //         const file = fileInput.files[0];
    //         if (file) {
    //             showLoader();
    //             const formData = new FormData();
    //             formData.append("file", file);

    //             fetch("/upload", {
    //                 method: "POST",
    //                 body: formData
    //             })
    //             .then(response => response.json())
    //             .then(data => {
    //                 hideLoader();
    //                 // Display the uploaded document name
    //                 showMessage(`Uploaded Document: ${file.name}`, "left");
    //                 // Display the success message
    //                 showMessage("File uploaded successfully.", "left");
    //                 fileInput.value = ""; // Clear the file input
    //             })
    //             .catch(error => {
    //                 hideLoader();
    //                 showMessage("Failed to upload file.", "left");
    //                 console.error("Error:", error);
    //             });
    //         }
    //     });

    //     // Handle form submission
    //     chatForm.addEventListener("submit", function(event) {
    //         event.preventDefault();
    //         const questionInput = document.getElementById("question");
    //         const question = questionInput.value;

    //         if (question.trim()) {
    //             showMessage(question, "left");
    //             const data = { question };

    //             fetch("/ask", {
    //                 method: "POST",
    //                 headers: {
    //                     "Content-Type": "application/json"
    //                 },
    //                 body: JSON.stringify(data)
    //             })
    //             .then(response => response.json())
    //             .then(data => {
    //                 const responseElement = document.createElement("div");
    //                 responseElement.className = "message-box message-left";
    //                 messageContainer.appendChild(responseElement);
    //                 if (data.answer) {
    //                     typeResponse(data.answer, responseElement);
    //                 } else {
    //                     responseElement.textContent = "Failed to get an answer.";
    //                     autoScroll(); // Ensure scroll down if no typing
    //                 }
    //                 questionInput.value = ""; // Clear the question input
    //             })
    //             .catch(error => {
    //                 showMessage("Failed to get an answer.", "right");
    //                 console.error("Error:", error);
    //             });
    //         }
    //     });
    // });
