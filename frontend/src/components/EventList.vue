<template>
  <div>
    <h2>Events</h2>
    <ul>
      <li v-for="event in events" :key="event.id">
        <b>{{ event.name }}</b>
        <span> ({{ event.start_date }} - {{ event.end_date }})</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { fetchEvents } from '@/api/api';

export default {
  name: "EventList",
  data() {
    return {
      events: []
    }
  },
  mounted() {
    fetchEvents()
      .then(response => {
        this.events = response.data;
      })
      .catch(error => {
        console.error(error);
      });
  }
}
</script>