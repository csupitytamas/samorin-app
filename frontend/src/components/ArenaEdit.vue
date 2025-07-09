<template>
  <div>
    <h2>Edit Arena</h2>

    <!-- ALREADY ASSIGNED POLES -->
    <h3>Assigned Poles</h3>
    <table border="1" cellpadding="6" style="margin-bottom:1.5rem; min-width:500px;">
      <thead>
        <tr>
          <th>Name</th>
          <th>Color</th>
          <th>Length (m)</th>
          <th>Quantity</th>
          <th>Image</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="poleLoc in assignedPoles" :key="poleLoc.id">
          <td>{{ poleLoc.pole.name_en }}</td>
          <td>{{ poleLoc.pole.color }}</td>
          <td>{{ poleLoc.pole.length }}</td>
          <td>{{ poleLoc.quantity }}</td>
          <td>
            <img v-if="poleLoc.pole.picture" :src="fullImageUrl(poleLoc.pole.picture)" alt="Pole" style="max-width:60px; max-height:60px;">
          </td>
           <td>
            <button @click="deletePoleLoc(poleLoc)">Delete</button>
         </td>
        </tr>
        <tr v-if="assignedPoles.length === 0">
          <td colspan="6" style="color:gray; text-align:center;">No poles assigned yet</td>
        </tr>
      </tbody>
    </table>

    <h3>Assigned Wings</h3>
    <table border="1" cellpadding="6" style="margin-bottom:1.5rem; min-width:400px;">
      <thead>
        <tr>
          <th>Name</th>
          <th>Color</th>
          <th>Quantity</th>
          <th>Image</th>
          <th>Delete</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="wingLoc in assignedWings" :key="wingLoc.id">
          <td>{{ wingLoc.wing.name_en }}</td>
          <td>{{ wingLoc.wing.color }}</td>
          <td>{{ wingLoc.quantity }}</td>
          <td>
            <img v-if="wingLoc.wing.picture" :src="fullImageUrl(wingLoc.wing.picture)" alt="Wing" style="max-width:60px; max-height:60px;">
          </td>
           <td>
            <button @click="deleteWingsLoc(wingLoc)">Delete</button>
         </td>
        </tr>
        <tr v-if="assignedWings.length === 0">
          <td colspan="5" style="color:gray; text-align:center;">No wings assigned yet</td>
        </tr>
      </tbody>
    </table>

    <!-- ASSIGN NEW POLES -->
    <h3>Assign New Poles</h3>
    <form @submit.prevent="submitPoles" style="margin-bottom:2rem;">
      <div v-for="pole in assignablePoles" :key="pole.id" style="margin-bottom: 8px;">
        <label>
          <input type="checkbox" v-model="selectedPoles" :value="pole.id">
          {{ pole.name_en }} ({{ pole.color }}, {{ pole.length }} m)
          <img v-if="pole.picture" :src="fullImageUrl(pole.picture)" alt="Pole" style="max-width:45px; max-height:45px; vertical-align: middle;">
        </label>
              <input
              type="number"
              v-model.number="poleQuantities[pole.id]"
              :disabled="!selectedPoles.includes(pole.id)"
              :max="pole.number"
              min="1"
              :placeholder="`Max: ${pole.number}`"
              style="margin-left: 6px; width: 70px;"
            />
      </div>
      <button type="submit" :disabled="assignablePoles.length === 0">Assign Selected Poles</button>
      <div v-if="assignablePoles.length === 0" style="color:gray;">All poles already assigned</div>
    </form>

    <!-- ASSIGN NEW WINGS -->
    <h3>Assign New Wings</h3>
    <form @submit.prevent="submitWings">
      <div v-for="wing in assignableWings" :key="wing.id" style="margin-bottom: 8px;">
        <label>
          <input type="checkbox" v-model="selectedWings" :value="wing.id">
          {{ wing.name_en }} ({{ wing.color }})
          <img v-if="wing.picture" :src="fullImageUrl(wing.picture)" alt="Wing" style="max-width:45px; max-height:45px; vertical-align: middle;">
        </label>
        <input
            type="number"
            v-model.number="wingQuantities[wing.id]"
            :disabled="!selectedWings.includes(wing.id)"
            :max="wing.number"
            min="1"
            :placeholder="`Max: ${wing.number}`"
            style="margin-left: 6px; width: 70px;"
          />
      </div>
      <button type="submit" :disabled="assignableWings.length === 0">Assign Selected Wings</button>
      <div v-if="assignableWings.length === 0" style="color:gray;">All wings already assigned</div>
    </form>

    <div v-if="successMessage" style="color:green; margin-top:10px;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red; margin-top:10px;">{{ errorMessage }}</div>
  </div>
</template>

<script>
import {
  fetchPoles,
  fetchWings,
  createPoleLocation,
  createWingLocation,
  fetchPoleLocationsByArena,
  fetchWingLocationsByArena,
  deleteWingsLocation, deletePoleLocation
} from '@/api/api';

export default {
  name: "ArenaEdit",
  props: ['arenaId'],
  data() {
    return {
      poles: [],
      wings: [],
      assignedPoles: [],
      assignedWings: [],
      selectedPoles: [],
      selectedWings: [],
      poleQuantities: {},
      wingQuantities: {},
      successMessage: '',
      errorMessage: ''
    }
  },
  computed: {
    assignablePoles() {
    const assignedIds = new Set(this.assignedPoles.map(loc => loc.pole.id));
    // warehouse-ban is van még elérhető?
    return this.poles.filter(pole => !assignedIds.has(pole.id) && pole.number > 0);
    },
    assignableWings() {
      const assignedIds = new Set(this.assignedWings.map(loc => loc.wing.id));
      return this.wings.filter(wing => !assignedIds.has(wing.id) && wing.number > 0);
    }
  },
  mounted() {
    this.loadPoles();
    this.loadWings();
    this.loadAssigned();
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://localhost:8000" + path;
    },
    loadPoles() {
      fetchPoles().then(res => { this.poles = res.data; });
    },
    loadWings() {
      fetchWings().then(res => { this.wings = res.data; });
    },
    loadAssigned() {
      fetchPoleLocationsByArena(this.arenaId)
        .then(res => { this.assignedPoles = res.data; });
      fetchWingLocationsByArena(this.arenaId)
        .then(res => { this.assignedWings = res.data; });
    },
        submitPoles() {
      Promise.all(this.selectedPoles.map(poleId => {
        return createPoleLocation({
          pole_id: poleId,
          quantity: this.poleQuantities[poleId] || 1,
          arena: this.arenaId
        });
      }))
      .then(() => {
        this.successMessage = "Poles assigned!";
        this.errorMessage = "";
        this.selectedPoles = [];
        this.poleQuantities = {};
        this.loadAssigned();
        this.loadPoles();  // ← hozzáadva!
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
    },
       submitWings() {
      Promise.all(this.selectedWings.map(wingId => {
        return createWingLocation({
          wing_id: wingId,
          quantity: this.wingQuantities[wingId] || 1,
          arena: this.arenaId
        });
      }))
      .then(() => {
        this.successMessage = "Wings assigned!";
        this.errorMessage = "";
        this.selectedWings = [];
        this.wingQuantities = {};
        this.loadAssigned();
        this.loadWings();  // ← hozzáadva!
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
    },
     deletePoleLoc(poleLoc) {
    // API hívás a polelocation törlésére
    deletePoleLocation(poleLoc.id)
      .then(() => {
        // Pole warehouse készletet frissítse a backend!
        this.loadAssigned();
        this.loadPoles();
      });
  },
     deleteWingsLoc(wingLoc) {
    // API hívás a polelocation törlésére
      deleteWingsLocation(wingLoc.id)
      .then(() => {
        this.loadAssigned();
        this.loadWings();
      });
  }
  }
}
</script>