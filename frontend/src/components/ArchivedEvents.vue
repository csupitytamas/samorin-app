<template>
  <div class="container">
    <h2>{{ t('archivedEvents') }}</h2>
    <div v-if="events.length > 0">
      <div
        v-for="event in events"
        :key="event.id"
        class="box-border event-item"
        @click="goToDetails(event.id)"
      >
        <div style="font-weight: bold;">
          {{ event.event_name }}
        </div>
        <div class="event-item-date">
          {{ event.event_start }} - {{ event.event_end }}
        </div>
      </div>
    </div>
    <div v-else class="muted" style="text-align: center;">
      {{ t('noArchivedEvents') }}
    </div>
  </div>
</template>

<script>
import { fetchArchivedEvents } from '@/api/api'
import { mapState } from 'vuex'
import translations from '@/translations'

export default {
  name: 'ArchivedEvents',
  data() {
    return { events: [] }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  mounted() {
    fetchArchivedEvents()
      .then(res => { this.events = res.data; })
      .catch(() => { this.events = []; });
  },
  methods: {
    goToDetails(id) {
      this.$router.push({ name: 'archived-event-details', params: { id } });
    }
  }
}
</script>
