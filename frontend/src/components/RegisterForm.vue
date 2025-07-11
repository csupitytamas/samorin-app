<template>
  <div class="register">
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label>Name:</label>
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
      <div>
        <label>Confirm Password:</label>
        <input v-model="password2" type="password" required />
      </div>
      <div class="password-hint">
        Minimum 8 characters, at least one uppercase letter.
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
import { registerUser, loginUser, fetchProfile } from "@/api/api"

function isStrongPassword(pw) {
  return pw.length >= 8 && /[A-Z]/.test(pw)
}

export default {
  name: 'RegistrationForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      error: '',
      success: false,
    }
  },
  methods: {
  async handleRegister() {
    this.error = ''
    this.success = false

    // Ellenőrzések:
    if (this.password !== this.password2) {
      this.error = "Passwords do not match!"
      return
    }
    if (!isStrongPassword(this.password)) {
      this.error = "Password must be at least 8 characters and contain at least one uppercase letter."
      return
    }

         try {
        await registerUser({
          username: this.username,
          email: this.email,
          password: this.password,
        })

        // Automatikus login
        const loginRes = await loginUser({
          username: this.username,
          password: this.password,
        })

        // Tokenek mentése
        if (loginRes.data.access) localStorage.setItem('access_token', loginRes.data.access)
        if (loginRes.data.refresh) localStorage.setItem('refresh_token', loginRes.data.refresh)

        // Lekérjük a profilt és elmentjük a store-ba
        const user = await fetchProfile()
        this.$store.dispatch('setUser', user)

        // Átirányítás (pl. profil oldalra)
        this.$router.push({ name: 'event-list' })

      } catch (err) {
        let detail = err.response?.data?.detail || err.response?.data?.email || err.message
        if (typeof detail === 'object' && Array.isArray(detail)) {
          detail = detail.join(' ')
        }
        if ((detail + '').toLowerCase().includes('email')) {
          this.error = 'This email is already taken!'
        } else {
          this.error = detail || 'Hiba történt a regisztráció során.'
        }
      }
  },
},
}
</script>

<style>
.error { color: red; }
.success { color: green; }
.password-hint {
  color: #888;
  font-size: 13px;
  margin-bottom: 10px;
}
</style>