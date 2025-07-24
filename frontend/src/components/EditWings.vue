<template>
  <div class="container">
    <h2>Edit Wing</h2>
    <form @submit.prevent="save" enctype="multipart/form-data" class="form-box">
      <div class="form-row">
        <label>Name (HU):</label>
        <input v-model="name_hu" required />
      </div>
      <div class="form-row">
        <label>Name (EN):</label>
        <input v-model="name_en" required />
      </div>
      <div class="form-row">
        <label>Color:</label>
        <input v-model="color" required />
      </div>
      <div class="form-row">
        <label>Stock:</label>
        <input type="number" v-model.number="number" min="0" required />
      </div>
      <div class="form-row">
        <label>Image:</label>
        <input type="file" @change="onFileChange" ref="fileInput" />
        <div v-if="pictureUrl" style="margin-top:0.4rem;">
          <img :src="pictureUrl" style="max-height:60px; border-radius: var(--border-radius); box-shadow: 0 0 0.4rem var(--accent-color);" />
        </div>
      </div>
      <div class="form-row" style="text-align: right;">
        <button type="submit">Save</button>
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
import { fetchWings, updateWings } from '@/api/api'

export default {
  data() {
    return {
      name_hu: '',
      name_en: '',
      color: '',
      number: 0,
      picture: null,
      originalPicture: '',
      pictureUrl: '',
      successMessage: '',
      errorMessage: ''
    }
  },
  created() {
    this.loadWing()
  },
  methods: {
    async loadWing() {
      const wingId = this.$route.params.id
      try {
        const { data } = await fetchWings()
        const found = data.find(w => w.id == wingId)
        if (found) {
          this.name_hu = found.name_hu
          this.name_en = found.name_en
          this.color = found.color
          this.number = found.number
          this.originalPicture = found.picture
          this.pictureUrl = found.picture?.startsWith('http')
            ? found.picture
            : 'http://13.48.70.78:8000' + found.picture
        }
      } catch {
        this.errorMessage = "Failed to load wing data."
      }
    },
    onFileChange(e) {
      this.picture = e.target.files[0] || null
      this.pictureUrl = this.picture
        ? URL.createObjectURL(this.picture)
        : this.originalPicture
    },
    async save() {
      const wingId = this.$route.params.id
      const formData = new FormData()
      formData.append("name_hu", this.name_hu)
      formData.append("name_en", this.name_en)
      formData.append("color", this.color)
      formData.append("number", this.number)
      if (this.picture) formData.append("picture", this.picture)
      try {
        await updateWings(wingId, formData)
        this.successMessage = "Wing updated successfully."
        this.errorMessage = ""
        setTimeout(() => this.$router.back(), 500)
      } catch {
        this.successMessage = ""
        this.errorMessage = "Failed to save changes."
      }
    }
  }
}
</script>
