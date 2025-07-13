<template>
  <div class="container">
    <h2>User admin</h2>

   <table class="styled-table">
  <thead>
    <tr>
      <th>Username</th>
      <th>Email</th>
      <th style="min-width: 1rem;">Role</th>
      <th>Change role</th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="user in users" :key="user.id">
      <td >{{ user.username }}</td>
      <td >{{ user.email }}</td>
      <td style="min-width: 1rem;" >{{ user.role }}</td>
      <td>
            <select v-model="user.newRole"
              style="background: var(--bg-color); color: var(--text-color); border: 1px solid rgba(255,255,255,0.15); border-radius: var(--border-radius); padding: var(--padding-s);">
              <option value="worker">Worker</option>
              <option value="chief">Chief</option>
              <option value="crew">Crew</option>
              <option value="admin">Admin</option>
            </select>
            <button @click="changeRole(user)">{{ t('save') || 'Save' }}</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="successMessage" style="color: var(--accent-color); margin-top: 0.8rem;">
      {{ successMessage }}
    </div>
    <div v-if="errorMessage" style="color: #ff3860; margin-top: 0.8rem;">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { fetchUsers, updateUserRole } from "@/api/api"
import { mapState } from "vuex"
import translations from "@/translations"

export default {
  name: "UserAdmin",
  data() {
    return {
      users: [],
      successMessage: '',
      errorMessage: ''
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  async mounted() {
    this.users = await fetchUsers()
    this.users.forEach(u => { u.newRole = u.role })
  },
  methods: {
    async changeRole(user) {
      try {
        await updateUserRole(user.id, { role: user.newRole })
        user.role = user.newRole
        this.successMessage = "Role updated!"
        this.errorMessage = ""
      } catch (err) {
        this.successMessage = ""
        this.errorMessage = "Failed to update role!"
      }
    }
  }
}
</script>