// ESP32 Control Functions
const sendRequest = async (command) => {
    try {
        const response = await fetch(`http://${esp32IpAddress}${command}`);
        const data = await response.text();
        displayOutput(data);
    } catch (error) {
        console.error('Error:', error);
        displayOutput('Failed to connect to ESP32');
    }
};

const getWeather = async () => {
    const city = 'Kashipur'; // Replace with your desired city
    try {
        const response = await fetch(`https://wttr.in/${city}?format=%C+%t+%h`);
        const data = await response.text();
        displayOutput(`Current Weather in ${city}:\n${data}`);
    } catch (error) {
        displayOutput('Failed to fetch weather data');
    }
};

const displayOutput = (message) => {
    const outputArea = document.getElementById('outputArea');
    outputArea.innerText += message + '\n'; // Append the message to the output area
};

// Event listener for the Get Weather button
document.getElementById("getWeather").addEventListener("click", getWeather);

// News Function using NewsAPI
const getNews = async () => {
    const NEWS_API_KEY = '028c9fc91fd04dd99d86ba3db42db83d'; // Replace with your API key
    try {
        const response = await fetch(`https://newsapi.org/v2/top-headlines?country=us&apiKey=${NEWS_API_KEY}`);
        const data = await response.json();
        const headlines = data.articles.slice(0, 5).map(article => article.title).join('\n\n');
        displayOutput(`Top 5 Headlines:\n\n${headlines}`);
    } catch (error) {
        displayOutput('Failed to fetch news');
    }
};

// Voice Recognition Setup
const setupVoiceControl = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        const command = event.results[0][0].transcript.toLowerCase();
        processVoiceCommand(command);
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        displayOutput('Speech recognition error: ' + event.error);
        alert("error")
    };

    return recognition;
};

// Process Voice Commands
const processVoiceCommand = (command) => {
    if (command.includes('light 1 on')) sendRequest('/light1/on');
    else if (command.includes('light 1 off')) sendRequest('/light1/off');
    else if (command.includes('light 2 on')) sendRequest('/light2/on');
    else if (command.includes('light 2 off')) sendRequest('/light2/off');
    else if (command.includes('light 3 on')) sendRequest('/light3/on');
    else if (command.includes('light 3 off')) sendRequest('/light3/off');
    else if (command.includes('light 4 on')) sendRequest('/light4/on');
    else if (command.includes('light 4 off')) sendRequest('/light4/off');
    else if (command.includes('fan on')) sendRequest('/fan/on');
    else if (command.includes('fan off')) sendRequest('/fan/off');
    else if (command.includes('weather')) getWeather();
    else if (command.includes('news')) getNews();
    else displayOutput('Command not recognized');
};

// Get ESP32 IP address from user input
const esp32IpAddressInput = document.getElementById('esp32Ip');
let esp32IpAddress = esp32IpAddressInput.value;

// Initialize voice recognition
const recognition = setupVoiceControl();

// Event listeners for buttons
document.getElementById("turnOn1").addEventListener("click", () => sendRequest('/light1/on'));
document.getElementById("turnOff1").addEventListener("click", () => sendRequest('/light1/off'));
document.getElementById("turnOn2").addEventListener("click", () => sendRequest('/light2/on'));
document.getElementById("turnOff2").addEventListener("click", () => sendRequest('/light2/off'));
document.getElementById("turnOn3").addEventListener("click", () => sendRequest('/light3/on'));
document.getElementById("turnOff3").addEventListener("click", () => sendRequest('/light3/off'));
document.getElementById("turnOn4").addEventListener("click", () => sendRequest('/light4/on'));
document.getElementById("turnOff4").addEventListener("click", () => sendRequest('/light4/off'));
document.getElementById("fanOn").addEventListener("click", () => sendRequest('/fan/on'));
document.getElementById("fanOff").addEventListener("click", () => sendRequest('/fan/off'));
document.getElementById("getNews").addEventListener("click", getNews);
document.getElementById("startVoice").addEventListener("click", () => {
    recognition.start();
    displayOutput('Listening for voice commands...');
});

// Update esp32IpAddress when the input changes
esp32IpAddressInput.addEventListener('input', () => {
    esp32IpAddress = esp32IpAddressInput.value;
});
