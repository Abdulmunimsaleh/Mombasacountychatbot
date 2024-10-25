<template>
  <div class="dropdown">
    <button class="dropdown-button">Choose an Option</button>
    <div class="dropdown-content">
      <button @click="fetchData('sign up')">Sign Up</button>
      <button @click="fetchData('log in')">Log In</button>
      <button @click="fetchData('forgot password')">Forgot Password</button>
      <button @click="fetchData('pay parking')">Pay Parking</button>
      <button @click="fetchData('pay water')">Pay Water</button>
      <button>Button 6</button>
      <button>Button 7</button>
      <button>Button 8</button>
      <button>Button 9</button>
      <button>Button 10</button>
      <button>Button 11</button>
      <button>Button 12</button>
    </div>
  </div>
  <div id="chatbot">
    <div class="button-container">
      <button @click="fetchData('sign up')">Sign Up</button>
      <button @click="fetchData('log in')">Log In</button>
      <button @click="fetchData('forgot password')">Forgot Password</button>
      <button @click="fetchData('pay parking')">Pay Parking</button>
      <button @click="fetchData('pay water')">Pay Water</button>
    </div>

    <div class="chat-container">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chat-message"
      >
        {{ message }}
      </div>
    </div>

    <input
      v-model="userInput"
      @keypress.enter="sendMessage"
      placeholder="Type your message..."
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: "",
      messages: [],
    };
  },
  methods: {
    fetchData(action) {
      fetch("data.txt")
        .then((response) => response.text())
        .then((data) => {
          // Split the data by lines and find the response based on action
          const lines = data.split("\n");
          let response = "Sorry, no response found for this action.";

          // Check for the action in the text file
          for (let line of lines) {
            if (line.toLowerCase().includes(action.toLowerCase())) {
              response = line;
              break;
            }
          }

          this.messages.push(response); // Add response to messages
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    sendMessage() {
      if (this.userInput.trim() !== "") {
        this.messages.push(`You: ${this.userInput}`);
        this.userInput = ""; // Clear the input

        // Here you can add code to process the user's message if needed
      }
    },
  },
};
</script>

<style scoped>
.button-container {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px;
}

.chat-container {
  border: 1px solid #ccc;
  padding: 10px;
  height: 300px; /* Adjust as needed */
  overflow-y: auto;
}

.chat-message {
  margin: 5px 0;
}
</style>
