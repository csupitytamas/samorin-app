<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label>Username:</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Email:</label>
        <input v-model="email" type="email" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Register</button>
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">Registration successful! Please log in.</div>
    </form>
      <p>
      Already have an account?
      <router-link :to="{ name: 'login' }">Login here!</router-link>
    </p>
  </div>
</template>

<script>

import {registerUser} from "@/api/api"

export default {
  name: 'RegistrationForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: '',
      success: false,
    }
  },
  methods: {
    async handleRegister() {
      this.error = ''
      this.success = false
      try {
      await registerUser({
        username: this.username,
        email: this.email,
        password: this.password,
      })
        this.success = true
        this.username = ''
        this.email = ''
        this.password = ''
      } catch (err) {
        this.error =
          err.response?.data?.detail ||
          'An error occurred during registration.'
      }
    },
  },
}
</script>

<style>
.error {
  color: red;
}
.success {
  color: green;
}
</style>