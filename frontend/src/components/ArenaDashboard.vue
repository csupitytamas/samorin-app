<template>
  <div>
    <h2>Arena Dashboard (ID: {{ arenaId }})</h2>

    <h3>Poles</h3>
    <ul>
      <li v-for="pl in poleLocations" :key="pl.id" style="margin-bottom: 10px;">

        <strong>{{ pl.pole.name_en }}</strong> ({{ pl.pole.color }}, {{ pl.pole.length }} m) — Number: {{ pl.quantity }}
         <img :src="pl.pole.picture" alt="Pole picture" style="width: 50px; height: auto; vertical-align: middle; margin-right: 10px;">
      </li>
    </ul>

    <h3>Wings</h3>
    <ul>
      <li v-for="wl in wingLocations" :key="wl.id" style="margin-bottom: 10px;">
        <img :src="wl.wing.picture" alt="Wing picture" style="width: 50px; height: auto; vertical-align: middle; margin-right: 10px;">
        <strong>{{ wl.wing.name_en }}</strong> ({{ wl.wing.color }}) — Quantity: {{ wl.quantity }}
      </li>
    </ul>
  </div>
</template>

<script>
import { fetchPoleLocationsByArena, fetchWingLocationsByArena } from '@/api/api';

export default {
  name: 'ArenaDashboard',
  props: ['arenaId'],
  data() {
    return {
      poleLocations: [],
      wingLocations: [],
    }
  },
  mounted() {
    fetchPoleLocationsByArena(this.arenaId)
      .then(response => {
        this.poleLocations = response.data;
      });

    fetchWingLocationsByArena(this.arenaId)
      .then(response => {
        this.wingLocations = response.data;
      });
  }
}
</script>
