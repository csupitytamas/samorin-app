<template>
  <div class="container" style="max-width: 400px;">
    <div class="box-border">
      <h2 style="text-align: center;">{{ t('register') }}</h2>
      <form @submit.prevent="handleRegister" class="inline-form column">
        <div style="margin-bottom: 1rem;">
          <input v-model="username" :placeholder="t('name')" required />
        </div>
        <div style="margin-bottom: 1rem;">
          <input v-model="email" type="email" :placeholder="t('email')" required />
        </div>
        <div style="margin-bottom: 1rem;">
          <input v-model="password" type="password" :placeholder="t('password')" required />
        </div>
        <div style="margin-bottom: 0.5rem;">
          <input v-model="password2" type="password" :placeholder="t('confirmPassword')" required />
        </div>
        <div class="password-hint" style="text-align:center;">
          {{ t('passwordHint') }}
        </div>
        <button type="submit" style="width:100%;">{{ t('register') }}</button>
      </form>
      <div v-if="error" style="color:red; margin-top:1rem; text-align:center;">
        {{ error }}
      </div>
      <div v-if="success" style="color:green; margin-top:1rem; text-align:center;">
        {{ t('registrationSuccess') }}
      </div>
    </div>
    <p style="text-align:center; margin-top:1.5rem;">
      {{ t('alreadyAccount') }}
      <router-link :to="{ name: 'login' }">{{ t('loginHere') }}</router-link>
    </p>
  </div>
</template>

<script>
import { registerUser, loginUser, fetchProfile } from "@/api/api"
import { mapState } from "vuex"
import translations from "@/translations"

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
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  methods: {
    async handleRegister() {
      this.error = ''
      this.success = false

      if (this.password !== this.password2) {
        this.error = this.t('passwordMismatch')
        return
      }
      if (!isStrongPassword(this.password)) {
        this.error = this.t('passwordStrength')
        return
      }

      try {
        await registerUser({
          username: this.username,
          email: this.email,
          password: this.password,
        })
        const loginRes = await loginUser({
          username: this.username,
          password: this.password,
        })

        if (loginRes.data.access) localStorage.setItem('access_token', loginRes.data.access)
        if (loginRes.data.refresh) localStorage.setItem('refresh_token', loginRes.data.refresh)

        const user = await fetchProfile()
        this.$store.dispatch('setUser', user)
        this.$router.push({ name: 'event-list' })
      } catch (err) {
        let detail = err.response?.data?.detail || err.response?.data?.email || err.message
        if (typeof detail === 'object' && Array.isArray(detail)) {
          detail = detail.join(' ')
        }
        if ((detail + '').toLowerCase().includes('email')) {
          this.error = this.t('emailTaken')
        } else {
          this.error = detail || this.t('registrationError')
        }
      }
    },
  },
}
</script>

<style scoped>
.password-hint {
  color: var(--muted-color);
  font-size: var(--font-size-s);
}
</style>