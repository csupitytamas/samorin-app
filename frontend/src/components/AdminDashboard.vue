<template>
  <div class="admin-dashboard">
    <h2>Admin Dashboard</h2>
    <div class="admin-buttons">
      <button @click="goTo('user-admin')">User admin</button>
      <button @click="goTo('pole-create')">Add new Pole</button>
      <button @click="goTo('wings-create')">Add new Wings</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AdminDashboard",
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
