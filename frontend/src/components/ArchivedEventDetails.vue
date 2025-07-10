<template>
  <div v-if="event">
    <h2>{{ t('archivedEventDetails') }}</h2>
    <p><b>{{ t('name') }}:</b> {{ event.event_name }}</p>
    <p><b>{{ t('start') }}:</b> {{ event.event_start }}</p>
    <p><b>{{ t('end') }}:</b> {{ event.event_end }}</p>
    <p><b>{{ t('closedAt') }}:</b> {{ event.closed_at }}</p>

    <h3>{{ t('arenas') }}</h3>
    <div v-for="arena in event.arenas" :key="arena.id" style="margin-bottom:2rem;">
      <b>{{ arena.name }}</b>
      <div>
        <span>{{ t('poles') }}:</span>
        <ul>
          <li v-for="pole in arena.poles" :key="pole.id">
            {{ pole.pole_name }} - {{ pole.color }} - {{ pole.length }}m ({{ pole.quantity }})
          </li>
          <li v-if="arena.poles.length === 0" style="color:gray;">{{ t('noPoles') }}</li>
        </ul>
      </div>
      <div>
        <span>{{ t('wings') }}:</span>
        <ul>
          <li v-for="wing in arena.wings" :key="wing.id">
            {{ wing.wing_name }} - {{ wing.color }} ({{ wing.quantity }})
          </li>
          <li v-if="arena.wings.length === 0" style="color:gray;">{{ t('noWings') }}</li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else>
    {{ t('loading') }}
  </div>
</template>

<script>
import { mapState } from "vuex";
import translations from "@/translations";
import { fetchArchivedEventDetails } from '@/api/api';
export default {
  name: 'ArchivedEventDetails',
  props: ['id'],
  data() {
    return { event: null }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  mounted() {
    fetchArchivedEventDetails(this.id)
      .then(res => { this.event = res.data; })
      .catch(() => { this.event = null });
  }
}
</script>
