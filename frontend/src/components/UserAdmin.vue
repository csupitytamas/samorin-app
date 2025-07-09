<template>
  <div>
    <h2>User admin</h2>
    <table>
      <thead>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>Role</th>
          <th>Change role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <select v-model="user.newRole">
              <option value="worker">Worker</option>
              <option value="chief">Chief</option>
              <option value="crew">Crew</option>
              <option value="admin">Admin</option>
            </select>
            <button @click="changeRole(user)">Save</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { fetchUsers, updateUserRole } from "@/api/api"

export default {
  name: "UserAdmin",
  data() {
    return {
      users: [],
    }
  },
  async mounted() {
    this.users = await fetchUsers()
    // Add newRole property for select binding
    this.users.forEach(u => { u.newRole = u.role })
  },
  methods: {
    async changeRole(user) {
      await updateUserRole(user.id, { role: user.newRole })
      user.role = user.newRole
      alert('Role updated!')
    },
  },
}
</script>
