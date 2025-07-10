<template>
  <div class="admin-dashboard">
    <h2>{{ t('adminDashboard') }}</h2>
    <div class="admin-buttons">
      <button @click="goTo('user-admin')">{{ t('userAdmin') }}</button>
      <button @click="goTo('pole-create')">{{ t('addPole') }}</button>
      <button @click="goTo('wings-create')">{{ t('addWings') }}</button>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex"
import translations from "@/translations"

export default {
  name: "AdminDashboard",
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  methods: {
    goTo(routeName) {
      this.$router.push({ name: routeName })
    }
  }
}
</script>

<style>
.admin-dashboard {
  text-align: center;
  margin-top: 2rem;
}
.admin-buttons button {
  margin: 1rem;
  padding: 1rem 2rem;
  font-size: 1.2rem;
}
</style>
