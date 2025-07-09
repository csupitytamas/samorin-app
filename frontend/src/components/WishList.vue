<template>
  <div>
    <h2>Wishlist Submission</h2>
    <div>
      <label>Arena:</label>
      <select v-model="selectedArena" required>
        <option v-for="arena in arenas" :key="arena.id" :value="arena.id">
          {{ arena.name }}
        </option>
      </select>
    </div>

<h3>Poles</h3>
      <div v-for="pole in filteredPoles" :key="pole.id" style="margin-bottom:8px;">
        <input type="checkbox"
               :id="'pole_'+pole.id"
               v-model="selectedPoles"
               :value="pole.id">
        <label :for="'pole_'+pole.id">
          <b>{{ pole.name_en }}</b> ({{ pole.color }}, {{ pole.length }} m)
          <img v-if="pole.picture" :src="fullImageUrl(pole.picture)" style="max-width:40px;max-height:40px;vertical-align:middle;">
        </label>
        <input type="number"
               v-model.number="poleQuantities[pole.id]"
               min="1"
               :max="pole.number"
               :placeholder="`Max: ${pole.number}`"
               :disabled="!selectedPoles.includes(pole.id)"
               style="margin-left:8px;width:60px;">
      </div>

<h3>Wings</h3>
      <div v-for="wing in filteredWings" :key="wing.id" style="margin-bottom:8px;">
        <input type="checkbox"
               :id="'wing_'+wing.id"
               v-model="selectedWings"
               :value="wing.id">
        <label :for="'wing_'+wing.id">
          <b>{{ wing.name_en }}</b> ({{ wing.color }})
          <img v-if="wing.picture" :src="fullImageUrl(wing.picture)" style="max-width:40px;max-height:40px;vertical-align:middle;">
        </label>
        <input type="number"
               v-model.number="wingQuantities[wing.id]"
               min="1"
               :max="wing.number"
               :placeholder="`Max: ${wing.number}`"
               :disabled="!selectedWings.includes(wing.id)"
               style="margin-left:8px;width:60px;">
      </div>

    <button @click="submitWishlist">Submit Wishlist</button>
    <div v-if="successMessage" style="color:green;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red;">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { fetchArenas, fetchPoles, fetchWings } from '@/api/api'
import axios from 'axios'

export default {
  name: 'WishlistCreate',
  data() {
    return {
      arenas: [],
      poles: [],
      wings: [],
      selectedArena: null,
      selectedPoles: [],           // checkbox: checked pole IDs
      selectedWings: [],
      poleQuantities: {},          // {poleId: quantity}
      wingQuantities: {},          // {wingId: quantity}
      successMessage: '',
      errorMessage: ''
    }
  },
  mounted() {
    fetchArenas().then(res => { this.arenas = res.data; });
    fetchPoles().then(res => { this.poles = res.data; });
    fetchWings().then(res => { this.wings = res.data; });
  },
  computed: {
  filteredPoles() {
    // Csak azokat mutasd, amelyekből van készleten!
    return this.poles.filter(pole => pole.number > 0);
  },
  filteredWings() {
    return this.wings.filter(wing => wing.number > 0);
  }
},
  methods: {
      fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://localhost:8000" + path;
    },
    submitWishlist() {
      if (!this.selectedArena) {
        this.errorMessage = "Please select an arena!";
        return;
      }

      // CSAK a kipipált ID-k + quantity megy
      const pole_items = this.selectedPoles
        .map(id => ({
          pole: id,
          quantity: this.poleQuantities[id] || 1
        }))
        .filter(item => item.quantity > 0);

      const wing_items = this.selectedWings
        .map(id => ({
          wing: id,
          quantity: this.wingQuantities[id] || 1
        }))
        .filter(item => item.quantity > 0);

      if (pole_items.length === 0 && wing_items.length === 0) {
        this.errorMessage = "Please add at least one item!";
        return;
      }

      axios.post('http://localhost:8000/api/wishlist/', {
        arena: this.selectedArena,
        pole_items,
        wing_items
      })
      .then(() => {
        this.successMessage = "Wishlist saved!";
        this.errorMessage = "";
        this.selectedPoles = [];
        this.selectedWings = [];
        this.poleQuantities = {};
        this.wingQuantities = {};
      })
      .catch(err => {
        this.successMessage = "";
        this.errorMessage = "Error: " + (err.response?.data?.detail || err.message);
      });
    }
  }
}
</script>
