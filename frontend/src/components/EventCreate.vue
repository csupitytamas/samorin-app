<template>
  <div class="container centered">
    <h2>{{ t('createEvent') }}</h2>
    <form @submit.prevent="submitEvent" class="form-box">
      <div class="form-row">
        <label>{{ t('name') }}:</label>
        <input v-model="form.name" required />
      </div>
      <div class="form-row">
        <label>{{ t('startDate') }}:</label>
        <input type="date" v-model="form.start_date" required />
      </div>
      <div class="form-row">
        <label>{{ t('endDate') }}:</label>
        <input type="date" v-model="form.end_date" required />
      </div>
      <button type="submit">{{ t('create') }}</button>
    </form>
    <div v-if="successMessage" class="success-msg">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error-msg">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { createEvent } from '@/api/api'
import { mapState } from 'vuex'
import translations from '@/translations'

export default {
  name: 'EventCreate',
  data() {
    return {
      form: {
        name: '',
        start_date: '',
        end_date: '',
        // is_active: true, // ha kell
        // is_archived: false // ha kell
      },
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
  methods: {
    submitEvent() {
      createEvent(this.form)
      .then(response => {
        const eventId = response.data.id
        this.successMessage = this.t('eventCreated')
        this.errorMessage = ''
        this.$router.push({ name: 'arena-create', params: { eventId } })
      })
      .catch(error => {
        this.errorMessage = this.t('error') + ': ' + (error.response?.data?.detail || error.message)
        this.successMessage = ''
      })
    }
  }
}
</script>
