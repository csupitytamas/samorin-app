<template>
  <div>
    <h2>Add new Pole</h2>
    <form @submit.prevent="addPole" enctype="multipart/form-data">
      <input v-model="name_hu" placeholder="Hungarian name" required />
      <input v-model="name_en" placeholder="English name" required />
      <input v-model="color" placeholder="Color" required />
      <input v-model.number="number" placeholder="Number" type="number" required />
      <input v-model.number="length" placeholder="Length (m)" type="number" step="0.01" required />
      <select v-model="warehouse">
        <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.name }}</option>
      </select>
      <input type="file" @change="onFileChange" /> <!-- ÚJ! -->
      <button type="submit">Add Pole</button>
    </form>
  </div>
</template>

<script>
import { fetchWarehouses, createPole } from "@/api/api"

export default {
  data() {
    return {
      name_hu: '',
      name_en: '',
      color: '',
      number: 1,
      length: 1,
      warehouse: null,
      warehouses: [],
      picture: null,    // ÚJ!
    }
  },
  async mounted() {
    this.warehouses = await fetchWarehouses()
  },
  methods: {
    onFileChange(e) {
      this.picture = e.target.files[0]
    },
    async addPole() {
      const formData = new FormData()
      formData.append("name_hu", this.name_hu)
      formData.append("name_en", this.name_en)
      formData.append("color", this.color)
      formData.append("number", this.number)
      formData.append("length", this.length)
      formData.append("warehouse", this.warehouse)
      if (this.picture) {
        formData.append("picture", this.picture)
      }
      await createPole(formData)
      alert('Pole added!')
      // opcionális: ürítsd ki a mezőket
      this.name_hu = ''
      this.name_en = ''
      this.color = ''
      this.number = 1
      this.length = 1
      this.warehouse = null
      this.picture = null
    }
  }
}
</script>
