<template>
  <div>
    <h2>Create new Event</h2>
    <form @submit.prevent="submitEvent">
      <div>
        <label>Name:</label>
        <input v-model="form.name" required>
      </div>
      <div>
        <label>Start date:</label>
        <input type="date" v-model="form.start_date" required>
      </div>
      <div>
        <label>End date:</label>
        <input type="date" v-model="form.end_date" required>
      </div>
      <!-- Itt lehet további mezőket hozzáadni, pl. is_active, is_archived -->
      <button type="submit">Create</button>
    </form>
    <div v-if="successMessage" style="color:green">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { createEvent } from '@/api/api';

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
  methods: {
    submitEvent() {
      createEvent(this.form)
      .then(response => {
        const eventId = response.data.id; // ezt a backendnek vissza kell adnia!
        this.successMessage = 'Event created!';
        this.errorMessage = '';
        // Átirányítás az ArenaCreate route-ra eventId-vel
        this.$router.push({ name: 'arena-create', params: { eventId } });
      })
      .catch(error => {
        this.errorMessage = 'Error: ' + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
        }
  }
}
</script>