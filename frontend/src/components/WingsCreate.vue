<template>
  <div class="container">
    <h2>Add new Wings</h2>
    <form @submit.prevent="addWings" enctype="multipart/form-data" class="form-box">
      <div class="form-row">
        <label>Hungarian name:</label>
        <input v-model="name_hu" required />
      </div>
      <div class="form-row">
        <label>English name:</label>
        <input v-model="name_en" required />
      </div>
      <div class="form-row">
        <label>Color:</label>
        <input v-model="color" required />
      </div>
      <div class="form-row">
        <label>Number:</label>
        <input v-model.number="number" type="number" min="1" required />
      </div>
      <div class="form-row">
        <label>Picture:</label>
        <input type="file" @change="onFileChange" ref="fileInput" />
      </div>
      <div class="form-row" style="text-align: right;">
        <button type="submit">Add Wings</button>
      </div>
      <div v-if="successMessage" style="color: var(--accent-color); margin-top: 0.8rem;">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" style="color: #ff3860; margin-top: 0.8rem;">
        {{ errorMessage }}
      </div>
    </form>
  </div>
</template>

<script>
import { createWings } from "@/api/api"

export default {
  data() {
    return {
      name_hu: '',
      name_en: '',
      color: '',
      number: 1,
      picture: null,
      successMessage: '',
      errorMessage: ''
    }
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
      formData.append("warehouse", 1)
      if (this.picture) {
        formData.append("picture", this.picture)
      }

      try {
        await createWings(formData)
        this.successMessage = "Wings added!"
        this.errorMessage = ""
        this.resetForm()
      } catch (err) {
        this.successMessage = ""
        this.errorMessage = "Failed to add wings!"
      }
    },
    resetForm() {
      this.name_hu = ''
      this.name_en = ''
      this.color = ''
      this.number = 1
      this.picture = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ""
      }
    }
  }
}
</script>
