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
                      <div class="modal-content">
                        <button @click="startConversation" class="start-btn">
                          Start Conversation
                        </button>
                      </div>
                    </div>
                  </div>

                  <div v-if="showUserFormModal" class="modal-overlay">
                    <div class="modal-container2">
                      <div class="modal-content2">
                        <form @submit.prevent="submitUserInfo">
                          <p>Provide us with below information</p>
                          <input
                            class="fill"
                            v-model="userInfo.name"
                            placeholder="Full Name"
                            required
                          />
                          <input
                            class="fill"
                            v-model="userInfo.phone"
                            placeholder="Phone Number"
                            required
                          />
                          <input
                            class="fill"
                            v-model="userInfo.email"
                            type="email"
                            placeholder="Email Address"
                            required
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

                  <!-- Carousel Buttons 
                  <div
                    v-if="!showStartModal && !showUserFormModal"
                    class="carousel-buttons-container"
                  >
                    <div class="carousel-buttons">
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
                        Pay Business Permits
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
                      <button @click="fetchData('Hawkers')">Hawkers</button>
                      <button @click="fetchData('Wayleaves')">
                        Pay Wayleaves
                      </button>
                    </div>
                  </div> -->

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
        `Hello! ${this.userInfo.name}, how can I assist you today?Select one of the following options:<br>
            1) Sign up support<br>
            2) Log in support<br>
            3) Forgot password<br>
            4) Payment for parking<br>
            5) Payment for Landrates <br>
            6) Payment for Cess <br>
            7) Payment for PSV Levy <br>
            8) Payment for House Rent <br>
            9) Payment for Wayleaves <br>
            10) Hawkers <br>
            11) Markets`
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

    // Carousell fetch data buttons action
    // fetchData(action) {
    //   let responseMessage = "";

    //   // Construct the response message based on the action
    //   if (action === "sign up") {
    //     responseMessage = `
    //       Sign Up<br />
    //       Please follow the following instruction for a successful sign up:<br />
    //       Step 1: Click the "Sign Up" button (top right) and enter your details.<br />
    //       Step 2: Enter your email, click "Send OTP," check your email for the code, and click "Verify." <br />
    //       Step 3: Enter your phone number, click "Send OTP," check your SMS for the code, and click "Verify."
    //     `;
    //   } else if (action === "log in") {
    //     responseMessage = `
    //       Log In<br />
    //       Step 1: Click on the log in button on top.<br />
    //       Step 2: Fill in your email address and your password and click log in.
    //     `;
    //   } else if (action === "forgot password") {
    //     responseMessage = `
    //       Forgot Password<br />
    //       Step 1: Click on the forgot password button on top.<br />
    //     `;
    //   } else if (action === "Payment for parking") {
    //     responseMessage = `
    //       For App users <br>
    //       Step 1: Log in <br>
    //       Step 2: Select Access Parking Module<br>
    //       Step 3: Click Add Vehicle <br>
    //       Step 4: Enter your plate number (no spaces) and vehicle category, then click Add <br>
    //       Step 5: Click Submit <br>
    //       Step 6: Select the added vehicle, choose your payment period (daily, monthly, etc) <br>
    //       Step 7: Choose a parking zone and Lipa via Mpesa Express or Mpesa <br>
    //       Access parking system For non-app users (USSD users): <br>
    //       Step 1: Dial *282#  <br>
    //       Step 2: Select 1: My Services  <br>
    //       Step 3: Select 1: Parking <br>
    //       Step 4: Select 2: Pay for Existing (or 1 for New) <br>
    //       Step 5: Choose vehicle, period, and zone <br>
    //       Step 6: Confirm and enter Mpesa PIN <br>
    //     `;
    //   } else if (action === "Payment for Landrates") {
    //     responseMessage = `
    //     Step 1: After Logging in select land rates module <br>
    //     Step 2: Top right select "pay for land service" <br>
    //     Step 3: Choose any service you want to pay for land <br>
    //     Step 4: Fill in all the necessary information and click next <br>
    //     Step 5: Upload all the necessary documnts and click finish <br>
    //     Step 6: For Land transfer Please select Land Usage and proceed to payment <br>
    //     Step 7: For Land clearance Please select clearance certificate fee and proceed to payment <br>
    //     Step 8: For Land sub division fee Please select Sub-division fees and proceed to payment
    //     `;
    //   } else if (action === "Payment for Business permits") {
    //     responseMessage = `
    //     Step 1: After Logging in select Business permits module <br>
    //     `;
    //   } else if (action === "Payment for Construction Permits") {
    //     responseMessage = `
    //     Step 1: After Logging in select Construction permits module <br>
    //     `;
    //   } else if (action === "Payment for PSV Levy") {
    //     responseMessage = `
    //     Step 1: After Logging in select PSV Levy module <br>
    //     Step 2: Click add vehicle <br>
    //     Step 3: Enter your number plate and click the blue box button to add your number plate <br>
    //     Step 4: Insert another number plate and click the submit button <br>
    //     Step 5: Click on the green button to make payment <br>
    //     Step 6: After payment click on the blue button to dowload your sticker and click on the red button to delete your vehicle
    //     `;
    //   } else if (action === "Payment for House Rent") {
    //     responseMessage = `
    //     Step 1: After Logging in select House Rent module <br>
    //     Step 2: View a list of all registered houses under your details <br>
    //     Step 3: Click the purple icon on the right to view your house rent statement <br>
    //     Step 4: Click the green button writen pay to make online payment <br>
    //     Step 5: Enter the phone number you wish to make payments from and click send payment request.You will receive an mpesa STK push to insert your pin number and complete the transaction <br>
    //     Step 6: Upon successful payment, you will be redirected back to your registered houses <br>
    //     Step 7: Click on my receipt to view a copy of your receipt or to download your receipt
    //     `;
    //   } else if (action === "Payment for Cess") {
    //     responseMessage = `
    //     Step 1: After Logging in select Cess module <br>
    //     Step 2: Click on New Application <br>
    //     Step 3: Fill in the details <br>
    //     Step 4: Click on the check box <br>
    //     Step 5: Click on the	submit button <br>
    //     Step 6: Click on pay and proceed to payment
    //     `;
    //   } else if (action === "Payment for Markets") {
    //     responseMessage = `
    //     Step 1: After Logging in select Markets module <br>
    //     Step 2: Click on the purple icon to view the statement <br>
    //     Step 3: Click the green icon written pay to pay for your stall <br>
    //     Step 4: Proceed to payment.
    //     `;
    //   } else if (action === "Hawkers") {
    //     responseMessage = `
    //     Step 1: After Logging in select Hawking module <br>
    //     Step 2: Click the search button to filter hawkers report <br>
    //     Step 3: Click the purple or green button to download hawkers collection report <br>
    //     Step 4: Go through above process 2 and process 3 to access hawkers zonal report
    //     `;
    //   } else if (action === "Wayleaves") {
    //     responseMessage = `
    //     Step 1: After Logging in select Wayleaves module <br>
    //     Step 2: Click the blue eye icon button to view the application details <br>
    //     Step 3: Click the "Download structure file" to download the application <br>
    //     Step 4: Click the button in red to "reject" or the button in blue to "approve" the application <br>
    //     Step 5: In Receipt page you can click the filter button to use any preferences <br>
    //     Step 6: Click the purple and green button to export as pdf or excel <br>
    //     Step 8: Click on the blue eye icon to view or download the receipt <br>
    //     Step 9: Follow the same from step 5 to step 8 for bills and licenses
    //     `;
    //   }

    //   // Add the action message from the user to the messages array
    //   this.messages.push({
    //     sender: "user",
    //     text: `${action.charAt(0).toUpperCase() + action.slice(1)}`,
    //   });

    //   // Add the response message from the bot
    //   this.messages.push({ sender: "bot", text: responseMessage });

    //   // Scroll down after adding the messages
    //   this.$nextTick(() => {
    //     const chatBody = this.$refs.chatBody;
    //     chatBody.scrollTop = chatBody.scrollHeight;
    //   });
    // },
  },
};
</script>

<style scoped>
.modal-content {
  width: 100%; /* Adjust as needed to center the button in the modal */
  margin-left: 85px;
  outline: none;
  border: none;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 400px;
  height: 60vh;
  display: grid;
  place-items: center;
  border: none;
  outline: none;
}

.start-btn {
  background-color: #7cdf5b;
  color: black;
  border: none;
  padding: 15px 40px;
  border-radius: 50px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  outline: none;
}

.start-btn:hover {
  background: linear-gradient(to right, #0a3aca, #6d91fb);
}

.modal-content2 {
  display: grid;
  place-items: center;
  padding: 20px;
  margin-left: 25px;
  width: 25vw;
}

.modal-container2 {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 400px;
  display: grid;
  place-items: center;
}

form {
  background-color: #7cdf5b;
  display: grid;
  gap: 15px;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  width: 100%;
}

.fill {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
  border-radius: 30px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.start-chat-btn {
  background-color: #022d68;
  color: white;
  border: none;
  padding: 5px;
  margin-bottom: 10px;
  border-radius: 30px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  margin-left: 35px;
}

.main-chat-footer {
  padding: 35px 20px;
}

.form-control {
  width: 100%;
  margin-top: 10px;
  margin-bottom: 10px;
  border: 3px solid #58595b;
  border-radius: 20px;
  padding: 1px 5px;
  background: #cecfeb;
}

.carousel-buttons-container {
  width: 100%;
  margin-top: 10px;
  padding-bottom: 15px;
  overflow: hidden;
}

.carousel-buttons {
  display: flex;
  flex-direction: row;
  overflow: hidden;
  overflow-x: auto; /* Enable horizontal scrolling */
  scroll-behavior: smooth;
}

.carousel-buttons button {
  flex: 0 0 auto;
  margin: 0 8px;
  padding: 5px 20px;
  background-color: #22466d;
  color: #fff;
  border-radius: 15px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.carousel-buttons button:hover {
  background: linear-gradient(to right, #0a3aca, #6d91fb);
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
  background: #e5e5e5;
}

h6 {
  color: black;
}

small {
  color: black;
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
  background-color: black;
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
  /* background: linear-gradient(to right, #0a3aca, #6d91fb); */
  background: #cecfeb;
  color: black;
  border-radius: 10px;
}

.main-msg-wrapper {
  /* background-color: rgba(239, 242, 247, 255); */
  background: #cecfeb;
  color: black;
  border-radius: 10px;
}

.media {
  color: black;
}
</style>
