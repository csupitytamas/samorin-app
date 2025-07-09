<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label>Username:</label>
        <input v-model="username" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="password" type="password" required />
      </div>
      <div>
        <input type="checkbox" id="rememberMe" v-model="rememberMe" />
        <label for="rememberMe">Keep me logged in</label>
      </div>
      <button type="submit">Login</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
       <p>
        Don't have an account?
        <router-link :to="{ name: 'register' }">Register here!</router-link>
      </p>
  </div>
</template>

<script>
import { loginUser } from "@/api/api"



export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      error: '',
    }
  },
  methods: {
  async handleLogin() {
    this.error = ''
    try {  // ← EZ HIÁNYZOTT!
      const res = await loginUser({
        username: this.username,
        password: this.password,
      })
      // Store tokens: localStorage if rememberMe, else sessionStorage
      if (this.rememberMe) {
        localStorage.setItem('access_token', res.data.access)
        localStorage.setItem('refresh_token', res.data.refresh)
      } else {
        sessionStorage.setItem('access_token', res.data.access)
        sessionStorage.setItem('refresh_token', res.data.refresh)
      }
      // Redirect to main page (adjust to your routes)
      this.$router.push({ name: 'event-list' })
    } catch (err) {
      this.error = 'Invalid login credentials!'
    }
  },
}
}
</script>

<style>
.error {
  color: red;
}
</style>