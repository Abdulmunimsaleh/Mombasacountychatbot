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
                  <!-- main-chat-header -->
                  <div
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
                            alt=""
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
                          <img src="/src/assets/img/faces/msa.png" alt="" />
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
                </div>
                <div class="main-chat-footer">
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
          <!-- row -->
        </div>
        <!-- Container closed -->
      </div>
      <!-- main-content closed -->
      <div class="main-footer ht-40">
        <div class="container-fluid pd-t-0-f ht-100p">
          <span
            >Copyright © 2021 <a href="#">Valex</a>. Designed by
            <a href="https://www.spruko.com/">Spruko</a> All rights
            reserved.</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userMessage: "", // User input message
      messages: [], // Array to hold chat messages
      botTyping: false, // Track when the bot is "typing"
    };
  },
  methods: {
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

        // Scroll down again after typing indicator is shown
        this.$nextTick(() => {
          const chatBody = this.$refs.chatBody;
          chatBody.scrollTop = chatBody.scrollHeight;
        });

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
  },
};
</script>

<style scoped>
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
