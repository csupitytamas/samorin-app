<template>
  <div class="container">
    <h2>Admin Dashboard</h2>

    <!-- User management button -->
    <div style="margin-bottom:2rem;">
      <button @click="goToUserAdmin">Manage Users</button>
    </div>

    <!-- Warehouse selector + tables -->
       <div class="box" style="margin-bottom:2rem;">
      <select id="warehouse-select" v-model="selectedWarehouseId" @change="refreshItems" class="accent-button">>
        <option disabled value="">-- Select a warehouse --</option>
        <option v-for="wh in warehouses" :key="wh.id" :value="wh.id">{{ wh.name }}</option>
      </select>
    </div>

    <div v-if="selectedWarehouseId">
      <!-- Poles -->
      <h3>Poles</h3>
      <button v-if="isAdmin" @click="addPole" style="margin-bottom:1rem;">Add New Pole</button>
      <div class="table-container">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Name(HU)</th>
              <th>Name(EN)</th>
              <th>Col</th>
              <th>Len</th>
              <th>Img</th>
              <th>Num</th>
              <th>Act</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="_pole in poles" :key="_pole.id">
              <td>{{ _pole.name_hu }}</td>
              <td>{{ _pole.name_en }}</td>
              <td>{{ _pole.color }}</td>
              <td>{{ _pole.length }}</td>
              <td>
              <img
                v-if="_pole.picture"
                :src="fullImageUrl(_pole.picture)"
                alt="Pole"
                class="table-image clickable-image"
                @click="fullscreenImage = fullImageUrl(_pole.picture)"
              />
              </td>
              <td>{{ _pole.number }}</td>
             <td v-if="isAdmin" style="display: flex; gap: 0.5rem">
              <button class="tiny-icon-button" @click="editPole(_pole)">✎</button>
              <button class="tiny-icon-button danger" @click="handleDeletePole(_pole)" title="Delete">🗑️</button>
            </td>
            </tr>
            <tr v-if="poles.length === 0">
              <td colspan="7" class="muted" style="text-align:center;">No poles in this warehouse.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Wings -->
      <h3 style="margin-top:2rem;">Wings</h3>
      <button v-if="isAdmin" @click="addWing" style="margin-bottom:1rem;">Add New Wing</button>
      <div class="table-container">
        <table class="styled-table">
          <thead>
            <tr>
              <th>Name(HU)</th>
              <th>Name(EN)</th>
              <th>Col</th>
              <th>Img</th>
              <th>Num</th>
              <th>Act</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="_wing in wings" :key="_wing.id">
              <td>{{ _wing.name_hu }}</td>
              <td>{{ _wing.name_en }}</td>
              <td>{{ _wing.color }}</td>
              <td>
                <img
                  v-if="_wing.picture"
                  :src="fullImageUrl(_wing.picture)"
                  alt="Wing"
                  class="table-image clickable-image"
                  @click="fullscreenImage = fullImageUrl(_wing.picture)"
                />
              </td>
              <td>{{ _wing.number }}</td>
              <td v-if="isAdmin" style="display: flex; gap: 0.5rem; padding:1.5rem;">
                <button class="tiny-icon-button" @click="editWing(_wing)">✎</button>
                <button class="tiny-icon-button danger" @click="handleDeleteWing(_wing)" title="Delete">🗑️</button>
              </td>
            </tr>
            <tr v-if="wings.length === 0">
              <td colspan="6" class="muted" style="text-align:center;">No wings in this warehouse.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
     <div v-if="fullscreenImage" class="image-modal" @click.self="fullscreenImage = null">
      <img :src="fullscreenImage" alt="Full image" />
      <button class="modal-close-btn" @click="fullscreenImage = null">Close</button>
    </div>
  </div>
</template>

<script>
import { fetchWarehouses, fetchPoles, fetchWings, deletePole as apiDeletePole, deleteWings as apiDeleteWings } from '@/api/api'
import { mapState } from 'vuex'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      poles: [],
      wings: [],
      warehouses: [],
      selectedWarehouseId: '',
     fullscreenImage: null,
    }
  },
  computed: {
    ...mapState(['user']),
    isAdmin() {
      return this.user && this.user.role === 'admin'
    }
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://13.48.70.78:8000" + path;
    },
    async refreshItems() {
      if (!this.selectedWarehouseId) return
      const [allPoles, allWings] = await Promise.all([fetchPoles(), fetchWings()])
      this.poles = allPoles.data.filter(p => p.warehouse === this.selectedWarehouseId)
      this.wings = allWings.data.filter(w => w.warehouse === this.selectedWarehouseId)
    },
    addPole() {
      this.$router.push({ name: 'pole-create' })
    },
    editPole(pole) {
      this.$router.push({ name: 'pole-edit', params: { id: pole.id } })
    },
    handleDeletePole(pole) {
      if (confirm('Are you sure you want to delete this pole?')) {
        apiDeletePole(pole.id).then(this.refreshItems)
      }
    },
    addWing() {
      this.$router.push({ name: 'wings-create' })
    },
    editWing(wing) {
      this.$router.push({ name: 'wings-edit', params: { id: wing.id } });
    },
    handleDeleteWing(wing) {
      if (confirm('Are you sure you want to delete this wing?')) {
        apiDeleteWings(wing.id).then(this.refreshItems)
      }
    },
    goToUserAdmin() {
      this.$router.push({ name: 'user-admin' })
    }
  },
  watch: {
    selectedWarehouseId: {
      immediate: true,
      handler() {
        this.refreshItems()
      }
    }
  },
  mounted() {
    fetchWarehouses().then(res => {
      this.warehouses = Array.isArray(res) ? res : res.data
    })
  }
}
</script>
