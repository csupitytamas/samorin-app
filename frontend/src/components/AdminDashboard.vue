<template>
  <div class="container">
    <h2>{{ t('adminDashboard') }}</h2>
    <div class="box centered" style="margin-top:2rem;">
      <div class="admin-buttons">
        <button @click="goTo('user-admin')">{{ t('userAdmin') }}</button>
        <button @click="goTo('pole-create')">{{ t('addPole') }}</button>
        <button @click="goTo('wings-create')">{{ t('addWings') }}</button>
      </div>
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

<style scoped>
.admin-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
@media (min-width: 600px) {
  .admin-buttons {
    flex-direction: row;
  }
}
</style>
