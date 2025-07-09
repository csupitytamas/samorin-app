<template>
  <div>
    <h2>Add new Wings</h2>
    <form @submit.prevent="addWings" enctype="multipart/form-data">
      <input v-model="name_hu" placeholder="Hungarian name" required />
      <input v-model="name_en" placeholder="English name" required />
      <input v-model="color" placeholder="Color" required />
      <input v-model.number="number" placeholder="Number" type="number" required />
      <select v-model="warehouse">
        <option v-for="w in warehouses" :key="w.id" :value="w.id">{{ w.name }}</option>
      </select>
      <input type="file" @change="onFileChange" />
      <button type="submit">Add Wings</button>
    </form>
  </div>
</template>

<script>
import { fetchWarehouses, createWings } from "@/api/api"

export default {
  data() {
    return {
      name_hu: '',
      name_en: '',
      color: '',
      number: 1,
      warehouse: null,
      warehouses: [],
      picture: null,
    }
  },
  async mounted() {
    this.warehouses = await fetchWarehouses()
  },
  methods: {
    onFileChange(e) {
      this.picture = e.target.files[0]
    },
    async addWings() {
      const formData = new FormData()
      formData.append("name_hu", this.name_hu)
      formData.append("name_en", this.name_en)
      formData.append("color", this.color)
      formData.append("number", this.number)
      formData.append("warehouse", this.warehouse)
      if (this.picture) {
        formData.append("picture", this.picture)
      }
      await createWings(formData)
      alert('Wings added!')
      // mezők ürítése
      this.name_hu = ''
      this.name_en = ''
      this.color = ''
      this.number = 1
      this.warehouse = null
      this.picture = null
    }
  }
}
</script>