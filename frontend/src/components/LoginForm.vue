<template>
  <div class="container" style="max-width: 400px;">
    <div class="box-border">
      <h2 style="text-align: center;">{{ t('login') }}</h2>
      <form @submit.prevent="handleLogin" class="inline-form column">
        <div style="margin-bottom: 1rem;">
          <input v-model="username" :placeholder="t('username')" required />
        </div>
        <div style="margin-bottom: 1rem;">
          <input v-model="password" type="password" :placeholder="t('password')" required />
        </div>
    <div class="form-group" style="display: flex; align-items: center; justify-content: center; gap: 0.6rem; margin: 1rem 0;">
  <div class="checkbox-wrapper-29">
    <label class="checkbox">
      <input type="checkbox" class="checkbox__input" v-model="rememberMe" />
      <span class="checkbox__label"></span>
    </label>
  </div>
  <label @click="rememberMe = !rememberMe" style="cursor: pointer;">{{   t('keepLoggedIn') }}</label>
</div>
        <button type="submit" style="width:100%;">{{ t('login') }}</button>
      </form>
      <div v-if="error" style="color:red; margin-top:1rem; text-align:center;">
        {{ error }}
      </div>
    </div>
    <p style="text-align:center; margin-top:1.5rem;">
      {{ t('noAccount') }}
      <router-link :to="{ name: 'register' }">{{ t('registerHere') }}</router-link>
    </p>
  </div>
</template>

<script>
import { loginUser, fetchProfile } from "@/api/api"
import { mapState } from "vuex"
import translations from "@/translations"

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
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  methods: {
    async handleLogin() {
      this.error = ''
      try {
        const res = await loginUser({
          username: this.username,
          password: this.password,
        })
        if (this.rememberMe) {
          localStorage.setItem('access_token', res.data.access)
          localStorage.setItem('refresh_token', res.data.refresh)
        } else {
          sessionStorage.setItem('access_token', res.data.access)
          sessionStorage.setItem('refresh_token', res.data.refresh)
        }
        const user = await fetchProfile()
        this.$store.dispatch('setUser', user)
        this.$router.push({ name: 'event-list' })
      } catch (err) {
        this.error = this.t('invalidLogin') || 'Invalid login credentials!'
      }
    },
  }
}
</script>