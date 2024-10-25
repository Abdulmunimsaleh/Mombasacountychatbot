<template>
  <div class="main-body app sidebar-mini">
    <!-- Loader -->
    <div id="global-loader">
      <img src="../assets/img/loader.svg" class="loader-img" alt="Loader" />
    </div>
    <!-- /Loader -->

    <!-- Page -->
    <div class="page" style="width: 50vw">
      <div class="main-content app-content">
        <div class="container-fluid">
          <div class="row main-content-app mb-4 mt-5">
            <div class="col-xl-8 col-lg-7 mt-5">
              <div class="card mt-5">
                <a class="main-header-arrow" href="#" id="ChatBodyHide">
                  <i class="icon ion-md-arrow-back"></i>
                </a>
                <div class="main-content-body">
                  <div class="main-chat-header">
                    <div class="main-img-user">
                      <img alt="" src="/src/assets/img/faces/msa.png" />
                    </div>
                    <div class="main-chat-msg-name">
                      <h6>Mombasa County Robo</h6>
                      <small>Online</small>
                    </div>
                  </div>

                  <!-- Modals -->
                  <div v-if="showStartModal" class="modal-overlay">
                    <div class="modal-container">
                      <div class="modal-content" style="width: 20vw">
                        <button @click="startConversation" class="start-btn">
                          Start Conversation
                        </button>
                      </div>
                    </div>
                  </div>

                  <div v-if="showUserFormModal" class="modal-overlay">
                    <div class="modal-container">
                      <div class="modal-content" style="width: 20vw">
                        <form @submit.prevent="submitUserInfo">
                          <input
                            v-model="userInfo.name"
                            placeholder="Enter your name"
                            required
                            style="
                              width: 15vw;
                              margin-bottom: 30px;
                              outline: none;
                              color: black;
                              border-bottom: 1px solid #fff;
                            "
                          />
                          <input
                            v-model="userInfo.phone"
                            placeholder="Enter your phone"
                            required
                            style="
                              width: 15vw;
                              color: black;
                              border-bottom: 1px solid #fff;
                              margin-bottom: 30px;
                              outline: none;
                            "
                          />
                          <input
                            v-model="userInfo.email"
                            type="email"
                            placeholder="Enter your email"
                            required
                            style="
                              width: 15vw;
                              color: black;
                              border-bottom: 1px solid #fff;
                              margin-bottom: 30px;
                              outline: none;
                            "
                          />
                          <button
                            type="submit"
                            class="start-chat-btn"
                            style="width: 15vw"
                          >
                            Start Chatting
                          </button>
                        </form>
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="!showStartModal && !showUserFormModal"
                    class="main-chat-body overflow-auto"
                    id="ChatBody"
                    ref="chatBody"
                  >
                    <div class="content-inner">
                      <div
                        v-for="(message, index) in messages"
                        :key="index"
                        class="media"
                        :class="{
                          'flex-row-reverse': message.sender === 'user',
                        }"
                      >
                        <div
                          class="main-img-user"
                          :class="{ online: message.sender === 'user' }"
                        >
                          <img
                            :src="
                              message.sender === 'user'
                                ? '../src/assets/img/faces/9.jpg'
                                : '../src/assets/img/faces/msa.png'
                            "
                            alt="User"
                          />
                        </div>
                        <div class="media-body">
                          <div
                            class="main-msg-wrapper"
                            :class="{
                              right: message.sender === 'user',
                              left: message.sender !== 'user',
                            }"
                          >
                            <span
                              v-if="message.sender === 'bot'"
                              v-html="message.text"
                            ></span>
                            <span v-else>{{ message.text }}</span>
                          </div>
                          <div>
                            <span>{{
                              new Date().toLocaleTimeString([], {
                                hour: "2-digit",
                                minute: "2-digit",
                              })
                            }}</span>
                            <a href="#"
                              ><i class="icon ion-android-more-horizontal"></i
                            ></a>
                          </div>
                        </div>
                      </div>
                      <!-- Typing Indicator -->
                      <div v-if="botTyping" class="media">
                        <div class="main-img-user">
                          <img src="/src/assets/img/faces/msa.png" alt="Bot" />
                        </div>
                        <div class="media-body">
                          <div class="main-msg-wrapper">
                            <div class="typing-indicator">
                              <span></span><span></span><span></span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Drop-up for Buttons -->
                  <div
                    v-if="!showStartModal && !showUserFormModal"
                    class="dropup-container"
                  >
                    <button class="dropup-button">
                      Options
                      <i class="fas fa-chevron-up"></i>
                    </button>
                    <div class="dropup-content">
                      <button @click="fetchData('sign up')">Sign Up</button>
                      <button @click="fetchData('log in')">Log In</button>
                      <button @click="fetchData('forgot password')">
                        Forgot Password
                      </button>
                      <button @click="fetchData('Payment for parking')">
                        Pay Parking
                      </button>
                      <button @click="fetchData('Payment for Landrates')">
                        Pay Land Rates
                      </button>
                      <button
                        @click="fetchData('Payment for Business permits')"
                      >
                        Pay Business permits
                      </button>
                      <button
                        @click="fetchData('Payment for Construction Permits')"
                      >
                        Pay Construction Permits
                      </button>
                      <button @click="fetchData('Payment for PSV Levy')">
                        Pay PSV Levy
                      </button>
                      <button @click="fetchData('Payment for House Rent')">
                        Pay House Rent
                      </button>
                      <button @click="fetchData('Payment for Cess')">
                        Pay Cess
                      </button>
                      <button @click="fetchData('Payment for Markets')">
                        Pay Markets
                      </button>
                      <button @click="fetchData('Payment for Hotel Levy')">
                        Pay Hotel Levy
                      </button>
                      <button @click="fetchData('Payment for Court Fines')">
                        Court Fines
                      </button>
                      <button @click="fetchData('Payment for Wayleaves')">
                        Pay Wayleaves
                      </button>
                    </div>
                  </div>

                  <div
                    v-if="!showStartModal && !showUserFormModal"
                    class="main-chat-footer"
                  >
                    <input
                      class="form-control"
                      v-model="userMessage"
                      placeholder="Type your message here..."
                      type="text"
                      @keyup.enter="sendMessage"
                    />
                    <a class="main-msg-send" @click="sendMessage">
                      <i class="far fa-paper-plane"></i>
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- row -->
        </div>
        <!-- Container closed -->
      </div>
      <!-- main-content closed -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      showStartModal: true, // Modal to start the conversation
      showUserFormModal: false, // Modal for user information
      userInfo: { name: "", phone: "", email: "" }, // User info data
      userMessage: "", // User input message
      messages: [], // Array to hold chat messages
      botTyping: false, // Track when the bot is "typing"
    };
  },
  methods: {
    // Method to start the conversation
    startConversation() {
      this.showStartModal = false;
      this.showUserFormModal = true;
    },
    // Method to submit user info and start chatting
    submitUserInfo() {
      this.showUserFormModal = false;
      this.messages.push({
        sender: "user",
        text: `Hi, I'm ${this.userInfo.name}`,
      });

      // Save user info to the database
      axios
        .post("http://127.0.0.1/save_user.php", this.userInfo)
        .then((response) => {
          if (response.data.status === "success") {
            console.log(response.data.message); // Optional: Log success message
          } else {
            console.error("Error saving user:", response.data.message);
          }
        })
        .catch((error) => {
          console.error("There was an error:", error);
        });

      this.getBotResponse(
        `Hello! ${this.userInfo.name}, how can I assist you today?`
      );
    },
    // Method to simulate bot responses for user inputs
    getBotResponse(userInput) {
      this.botTyping = true;
      setTimeout(() => {
        this.botTyping = false;
        this.messages.push({ sender: "bot", text: `${userInput}` });
      }, 1000); // Simulate a typing delay
    },
    sendMessage() {
      const message = this.userMessage.trim(); // Trim whitespace
      if (message) {
        // Add user message to the chat
        this.messages.push({ sender: "user", text: message });

        // Clear input field
        this.userMessage = "";

        // Immediately scroll to the bottom after user sends message
        this.$nextTick(() => {
          const chatBody = this.$refs.chatBody;
          chatBody.scrollTop = chatBody.scrollHeight;
        });

        // Show bot typing indicator
        this.botTyping = true;

        // Simulate a delay for bot's typing (e.g., 1 second)
        setTimeout(() => {
          // Send the message to the backend to get the bot's response
          axios
            .post("http://127.0.0.1:5000/chat", { message })
            .then((response) => {
              // Hide the typing indicator
              this.botTyping = false;

              // If bot response is received, add it to the messages array
              if (response.data && response.data.response) {
                this.messages.push({
                  sender: "bot",
                  text: response.data.response,
                });

                // After the bot's message is added, scroll down again
                this.$nextTick(() => {
                  const chatBody = this.$refs.chatBody;
                  chatBody.scrollTop = chatBody.scrollHeight;
                });

                // Display the further help message separately, if available
                if (response.data.further_help) {
                  setTimeout(() => {
                    this.messages.push({
                      sender: "bot",
                      text: response.data.further_help,
                    });

                    // Scroll down after further help is displayed
                    this.$nextTick(() => {
                      const chatBody = this.$refs.chatBody;
                      chatBody.scrollTop = chatBody.scrollHeight;
                    });
                  }, 500); // Delay the further help message slightly (e.g., 0.5s)
                }
              } else {
                console.error("Unexpected response structure:", response.data);
                this.botTyping = false; // Hide typing indicator if there's an error
              }
            })
            .catch((error) => {
              console.error(
                "There was an error with the request:",
                error.response ? error.response.data : error.message
              );
              this.botTyping = false; // Hide typing indicator if there's an error
            });
        }, 1000); // Simulate the bot "typing" delay (1 second)
      }
    },
    fetchData(action) {
      let responseMessage = "";

      // Construct the response message based on the action
      if (action === "sign up") {
        responseMessage = `
          Sign Up<br />
          Please follow the following instruction for a successful sign up:<br />
          Step 1: Click the "Sign Up" button (top right) and enter your details.<br />
          Step 2: Enter your email, click "Send OTP," check your email for the code, and click "Verify." <br />
          Step 3: Enter your phone number, click "Send OTP," check your SMS for the code, and click "Verify."
        `;
      } else if (action === "log in") {
        responseMessage = `
          Log In<br />
          Step 1: Click on the log in button on top.<br />
          Step 2: Fill in your email address and your password and click log in.
        `;
      } else if (action === "forgot password") {
        responseMessage = `
          Forgot Password<br />
          Step 1: Click on the forgot password button on top.<br />
        `;
      } else if (action === "Payment for parking") {
        responseMessage = `
          For App users <br>
          Step 1: Log in <br>
          Step 2: Select Access Parking Module<br>
          Step 3: Click Add Vehicle <br>
          Step 4: Enter your plate number (no spaces) and vehicle category, then click Add <br>
          Step 5: Click Submit <br>
          Step 6: Select the added vehicle, choose your payment period (daily, monthly, etc) <br>
          Step 7: Choose a parking zone and Lipa via Mpesa Express or Mpesa <br>
          Access parking system For non-app users (USSD users): <br>
          Step 1: Dial *282#  <br>
          Step 2: Select 1: My Services  <br>
          Step 3: Select 1: Parking <br>
          Step 4: Select 2: Pay for Existing (or 1 for New) <br>
          Step 5: Choose vehicle, period, and zone <br>
          Step 6: Confirm and enter Mpesa PIN <br>
        `;
      }

      // Add the action message from the user to the messages array
      this.messages.push({
        sender: "user",
        text: `${action.charAt(0).toUpperCase() + action.slice(1)}`,
      });

      // Add the response message from the bot
      this.messages.push({ sender: "bot", text: responseMessage });

      // Scroll down after adding the messages
      this.$nextTick(() => {
        const chatBody = this.$refs.chatBody;
        chatBody.scrollTop = chatBody.scrollHeight;
      });
    },
  },
};
</script>

<style scoped>
.modal-content {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 400px;
  padding: 40px;
  transform: translate(-50%, -50%);
  background: #007bff;
  box-sizing: border-box;
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.6);
  border-radius: 10px;
  margin-top: 30px;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  padding: 100px;
  width: 90%; /* Adjust the width as needed */
  max-width: 400px; /* Maximum width for larger screens */
  height: 50vh;
}

.start-btn,
.start-chat-btn {
  background-color: #007bff; /* Change this color as needed */
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.start-btn:hover,
.start-chat-btn:hover {
  background-color: #0056b3; /* Darker shade on hover */
}

.form-control {
  width: 100%;
  margin-bottom: 10px;
}

.dropup-container {
  position: relative;
  display: inline-block;
}

.dropup-button {
  background-color: #4caf50;
  color: white;
  padding: 12px;
  font-size: 12px;
  border: none;
  cursor: pointer;
}

.dropup-content {
  display: none;
  position: absolute;
  bottom: 100%;
  left: 0;
  background-color: #f1f1f1;
  /* min-width: 160px; */
  width: 100px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropup-container:hover .dropup-content {
  display: block;
}

.dropup-content button {
  color: black;
  padding: 12px;
  font-size: 12px;
  text-decoration: none;
  display: block;
  width: 100%;
}

.dropup-content button:hover {
  background-color: #ddd;
}

.button-container {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
}

button:hover {
  background-color: #0056b3;
}

.main-content-body {
  width: 100%; /* Make sure this is wide enough */
}

.main-chat-header {
  background-color: #0033cc;
}

h6 {
  color: rgba(187, 242, 255, 255);
}

small {
  color: rgba(187, 242, 255, 255);
}

.card {
  width: 150%; /* Ensure the card takes the full width of the parent */
  max-width: 800px; /* Set a max width if necessary */
  margin: 0 auto; /* Center the card */
}

.main-chat-body {
  width: 90% !important; /* Enforce this width */
  height: 400px; /* Adjust the height as needed */
  overflow-y: auto; /* Ensure vertical scrolling if content overflows */
  margin: 0 auto; /* Center the chat window */
}

.typing-indicator {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  height: 20px;
}

.typing-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin: 0 2px;
  background-color: #ccc;
  border-radius: 50%;
  opacity: 0;
  animation: typing 1.5s infinite;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0.2s;
}
.typing-indicator span:nth-child(2) {
  animation-delay: 0.4s;
}
.typing-indicator span:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes typing {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}

.main-chat-body .media.flex-row-reverse .main-msg-wrapper {
  background-color: #007fff;
  color: #fff;
}

.main-msg-wrapper {
  background-color: rgba(239, 242, 247, 255);
  color: rgba(39, 45, 59, 255);
}
</style>
