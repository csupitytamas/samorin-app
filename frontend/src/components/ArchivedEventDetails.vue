<template>
  <div class="container">
    <div v-if="event">
      <h2>{{ t('archivedEventDetails') }}</h2>
      <div class="box-border" style="text-align:center;">
        <p><b>{{ t('name') }}:</b> {{ event.event_name }}</p>
        <p><b>{{ t('start') }}:</b> {{ event.event_start }}</p>
        <p><b>{{ t('end') }}:</b> {{ event.event_end }}</p>
      </div>

      <h3>{{ t('arenas') }}</h3>
      <div v-for="arena in event.arenas" :key="arena.id" class="box-border">
        <h4 style="text-align:center;">{{ arena.name }}</h4>

        <!-- Poles table -->
      <div v-if="arena.poles.length">
  <table class="styled-table">
    <thead>
      <tr>
        <th>{{ t('name') }}</th>
        <th>{{ t('color') }}</th>
        <th>{{ t('length') }}</th>
        <th>{{ t('quantity') }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="pole in arena.poles" :key="pole.id">
        <td>{{ pole.pole_name }}</td>
        <td>{{ pole.color }}</td>
        <td>{{ pole.length }}</td>
        <td>{{ pole.quantity }}</td>
      </tr>
    </tbody>
  </table>
</div>
<div v-else class="muted" style="text-align:center;">
  {{ t('noArchivedPoles') }}
</div>

<div v-if="arena.wings.length" style="margin-top:1rem;">
  <table class="styled-table">
    <thead>
      <tr>
        <th>{{ t('name') }}</th>
        <th>{{ t('color') }}</th>
        <th>{{ t('quantity') }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="wing in arena.wings" :key="wing.id">
        <td>{{ wing.wing_name }}</td>
        <td>{{ wing.color }}</td>
        <td>{{ wing.quantity }}</td>
      </tr>
    </tbody>
  </table>
</div>
<div v-else class="muted" style="text-align:center;">
  {{ t('noArchivedWings') }}
</div>
        </div>
    </div>
    <div v-else style="text-align:center;">
      {{ t('loading') }}
    </div>
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
