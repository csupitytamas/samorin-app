<template>
  <div>
    <h2>Add new Pole</h2>
    <form @submit.prevent="addPole" enctype="multipart/form-data" style="display: flex; flex-direction: column; gap: 10px; max-width: 370px;">
      <label>
        Hungarian name:<br>
        <input v-model="name_hu" required />
      </label>
      <label>
        English name:<br>
        <input v-model="name_en" required />
      </label>
      <label>
        Color:<br>
        <input v-model="color" required />
      </label>
      <label>
        Number:<br>
        <input v-model.number="number" type="number" min="1" required />
      </label>
      <label>
        Length (m):<br>
        <select v-model.number="length" required>
          <option :value="3.5">3.5</option>
          <option :value="3">3</option>
          <option :value="2.5">2.5</option>
          <option :value="2">2</option>
        </select>
      </label>
      <label>
        Picture:<br>
        <input type="file" @change="onFileChange" ref="fileInput" />
      </label>
      <button type="submit">Add Pole</button>
    </form>
  </div>
</template>

<script>
import { createPole } from "@/api/api"

export default {
  data() {
    return {
      name_hu: '',
      name_en: '',
      color: '',
      number: 1,
      length: 3.5, // alapértelmezett
      picture: null,
    }
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
      formData.append("warehouse", 1)
      if (this.picture) {
        formData.append("picture", this.picture)
      }
      await createPole(formData)
      alert('Pole added!')
      this.name_hu = ''
      this.name_en = ''
      this.color = ''
      this.number = 1
      this.length = 3.5
      this.picture = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ""
      }
    }
  }
}
</script>
