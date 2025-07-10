<template>
  <div>
    <h2>Add new Wings</h2>
    <form @submit.prevent="addWings" enctype="multipart/form-data" style="display: flex; flex-direction: column; gap: 10px; max-width: 370px;">
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
        Picture:<br>
        <input type="file" @change="onFileChange" ref="fileInput" />
      </label>
      <!-- warehouse mező elrejtve, fixen 1-es ID-t küldünk -->
      <button type="submit">Add Wings</button>
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
      formData.append("warehouse", 1) // mindig az 1-es ID!
      if (this.picture) {
        formData.append("picture", this.picture)
      }
      await createWings(formData)
      alert('Wings added!')
      this.name_hu = ''
      this.name_en = ''
      this.color = ''
      this.number = 1
      this.picture = null
      this.$refs.fileInput.value = ""
    }
  }
}
</script>