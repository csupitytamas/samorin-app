<template>
  <div>
    <h2>Edit Arena – add Poles and Wings</h2>

    <h3>Assign Poles</h3>
    <form @submit.prevent="submitPoles">
      <div v-for="pole in poles" :key="pole.id">
        <label>
          <input type="checkbox" v-model="selectedPoles" :value="pole.id">
          {{ pole.name_en }} ({{ pole.color }})
        </label>
        <input type="number"
               v-model.number="poleQuantities[pole.id]"
               :disabled="!selectedPoles.includes(pole.id)"
               min="1"
               placeholder="Quantity" />
      </div>
      <button type="submit">Assign Selected Poles</button>
    </form>

    <h3>Assign Wings</h3>
    <form @submit.prevent="submitWings">
      <div v-for="wing in wings" :key="wing.id">
        <label>
          <input type="checkbox" v-model="selectedWings" :value="wing.id">
          {{ wing.name_en }} ({{ wing.color }})
        </label>
        <input type="number"
               v-model.number="wingQuantities[wing.id]"
               :disabled="!selectedWings.includes(wing.id)"
               min="1"
               placeholder="Quantity" />
      </div>
      <button type="submit">Assign Selected Wings</button>
    </form>

    <div v-if="successMessage" style="color:green">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { fetchPoles, fetchWings, createPoleLocation, createWingLocation } from '@/api/api';

export default {
  name: "ArenaEdit",
  props: ['arenaId'],
  data() {
    return {
      poles: [],
      wings: [],
      selectedPoles: [],
      selectedWings: [],
      poleQuantities: {},
      wingQuantities: {},
      successMessage: '',
      errorMessage: ''
    }
  },
  mounted() {
    fetchPoles().then(res => { this.poles = res.data; });
    fetchWings().then(res => { this.wings = res.data; });
  },
  methods: {
    submitPoles() {
      Promise.all(this.selectedPoles.map(poleId => {
        return createPoleLocation({
          pole: poleId,
          quantity: this.poleQuantities[poleId] || 1,
          arena: this.arenaId
        });
      }))
      .then(() => {
        this.successMessage = "Poles assigned!";
        this.errorMessage = "";
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
    },
    submitWings() {
      Promise.all(this.selectedWings.map(wingId => {
        return createWingLocation({
          wing: wingId,
          quantity: this.wingQuantities[wingId] || 1,
          arena: this.arenaId
        });
      }))
      .then(() => {
        this.successMessage = "Wings assigned!";
        this.errorMessage = "";
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
    }
  }
}
</script>
