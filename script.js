// Paste this to the developer console.
// Dont forget to open the websocket!


(function() {
    console.log("[BM] Assist by: https://github.com/blamemess/monkeytype-hack"); 

    // Connect to WebSocket server (Python server)
    const socket = new WebSocket("ws://localhost:8765");

    socket.onopen = () => {
        console.log("Connected with the port 8765"); 

        // Function to capture all words and send to Python
        async function captureAndSend() {
            const wordElements = document.querySelectorAll('.word');
            const words = [];

            wordElements.forEach(wordElement => {
                const word = Array.from(wordElement.querySelectorAll('letter')).map(letter => letter.textContent || letter.innerHTML).join('');
                words.push(word);
            });

            console.log('Captured words:', words.join(' '));

            // Send the words to the Python WebSocket server
            const data = { words: words };
            socket.send(JSON.stringify(data));
        }

        // Send words immediately when the script starts
        captureAndSend();
    };

    socket.onmessage = function(event) {
        console.log("Received Packets:", event.data); 
    };

    socket.onerror = function(error) {
        console.error("WebSocket Error:", error);
    };

    socket.onclose = function() {
        console.log("Websocket Closed."); 
    };
})();
