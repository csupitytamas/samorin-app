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

    <!-- ÜZENETEK -->
    <div v-if="successMessage" style="color:green; margin-top:10px;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red; margin-top:10px;">{{ errorMessage }}</div>

    <!-- GRID nézet, checkbox-szal és egyszerre assign-nal -->
    <form @submit.prevent="assignGridSelected" style="margin-top: 3rem;">
      <h3 style="font-weight:bold;">Összes elérhető eszköz (kártyás/grid nézet, keresővel, szűrőkkel, kijelöléssel)</h3>
      <div style="margin-bottom: 16px; display: flex; gap: 12px;">
        <input
          v-model="gridSearch"
          type="text"
          placeholder="Keresés név szerint..."
          style="padding:4px 10px; border-radius:4px; border:1px solid #bbb;"
        />
        <select v-model="gridColor" style="padding:4px 10px; border-radius:4px;">
          <option value="">Minden szín</option>
          <option v-for="color in gridAvailableColors" :key="color" :value="color">{{ color }}</option>
        </select>
        <select v-model="gridType" style="padding:4px 10px; border-radius:4px;">
          <option value="">Mindkettő</option>
          <option value="pole">Pole</option>
          <option value="wing">Wing</option>
        </select>

        <!-- LENGTH FILTER: csak ha pole a típus -->
        <select v-if="gridType === 'pole'" v-model="gridLength" style="padding:4px 10px; border-radius:4px;">
          <option value="">Minden hossz</option>
          <option v-for="len in gridAvailableLengths" :key="len" :value="len">
            {{ len }} m
          </option>
        </select>
      </div>
      <div class="arena-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 18px;">
        <div
          v-for="item in paginatedGridItems"
          :key="item.type + '-' + item.id"
          style="position:relative; border: 1px solid #e1e1e1; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 2px 8px #eee; background: #fafbfc;"
        >
          <!-- Checkbox a sarokban -->
          <input
            type="checkbox"
            :id="`grid-check-${item.type}-${item.id}`"
            :value="item.type + '-' + item.id"
            v-model="gridSelected"
            style="position: absolute; top: 8px; left: 8px; width: 18px; height: 18px;"
          />
          <img
            v-if="item.picture"
            :src="fullImageUrl(item.picture)"
            alt=""
            style="height: 70px; margin-bottom: 8px; object-fit: contain;"
          />
          <div style="font-weight: bold; margin-bottom: 2px;">
            {{ item.name_en || item.name_hu }}
          </div>
          <div style="color:#555;">
            {{ item.color }}
            <span v-if="item.length">, {{ item.length }} m</span>
          </div>
          <div style="font-size:13px; color:#888; margin-bottom:4px;">Típus: {{ item.type }}</div>
          <div>Készlet: {{ item.number }}</div>
          <!-- Quantity input, ha kijelölve -->
          <div v-if="gridSelected.includes(item.type + '-' + item.id)" style="margin-top:7px;">
            <input
              type="number"
              :max="item.number"
              min="1"
              v-model.number="gridQuantities[item.type + '-' + item.id]"
              :placeholder="`Max: ${item.number}`"
              style="width:70px;"
            />
          </div>
        </div>
      </div>
      <!-- Pagination -->
      <div v-if="gridPageCount > 1" style="display:flex; gap:8px; justify-content:center; margin:24px 0 0 0;">
        <button
          v-for="page in gridPageCount"
          :key="page"
          @click="gridCurrentPage = page"
          :style="{
            padding:'3px 13px', borderRadius:'7px',
            background: gridCurrentPage === page ? '#2563eb' : '#ececec',
            color: gridCurrentPage === page ? '#fff' : '#444',
            border:'none', cursor:'pointer', fontWeight: gridCurrentPage === page ? 'bold' : 'normal'
          }"
        >
          {{ page }}
        </button>
      </div>
      <div v-if="paginatedGridItems.length === 0" style="color:gray; text-align:center; margin-top:1em;">
        Nincs találat.
      </div>
      <div style="text-align:right; margin:24px 0;">
        <button type="submit" :disabled="gridSelected.length === 0">
          Assign selected to Arena
        </button>
      </div>
    </form>
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
  deleteWingsLocation,
  deletePoleLocation
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
      errorMessage: '',
      // GRID szekcióhoz
      gridSearch: '',
      gridColor: '',
      gridType: '',
      gridLength: '',
      gridCurrentPage: 1,
      gridPerPage: 8,
      gridSelected: [],
      gridQuantities: {},
    }
  },
  computed: {
    assignablePoles() {
      const assignedIds = new Set(this.assignedPoles.map(loc => loc.pole.id));
      return this.poles.filter(pole => !assignedIds.has(pole.id) && pole.number > 0);
    },
    assignableWings() {
      const assignedIds = new Set(this.assignedWings.map(loc => loc.wing.id));
      return this.wings.filter(wing => !assignedIds.has(wing.id) && wing.number > 0);
    },
    // ------- GRID logika -------
    gridAvailableItems() {
      // Az összes pole+wing, amiből válogat a grid (warehouse, ami > 0)
      return [
        ...this.poles.map(p => ({ ...p, type: 'pole' })),
        ...this.wings.map(w => ({ ...w, type: 'wing' }))
      ].filter(i => i.number > 0)
    },
    gridAvailableColors() {
      // Egyedi színek
      return [...new Set(this.gridAvailableItems.map(i => i.color).filter(Boolean))];
    },
    gridAvailableLengths() {
      // Csak pole típushoz!
      return [...new Set(
        this.gridAvailableItems
          .filter(i => i.type === 'pole')
          .map(i => i.length)
          .filter(Boolean)
      )].sort((a, b) => a - b)
    },
    filteredGridItems() {
      return this.gridAvailableItems.filter(i =>
        (!this.gridSearch || (i.name_en && i.name_en.toLowerCase().includes(this.gridSearch.toLowerCase())) ||
          (i.name_hu && i.name_hu.toLowerCase().includes(this.gridSearch.toLowerCase()))
        ) &&
        (!this.gridColor || i.color === this.gridColor) &&
        (!this.gridType || i.type === this.gridType) &&
        // csak pole-nál szűr hosszt
        (!this.gridLength || i.type !== 'pole' || String(i.length) === String(this.gridLength))
      )
    },
    gridPageCount() {
      return Math.ceil(this.filteredGridItems.length / this.gridPerPage)
    },
    paginatedGridItems() {
      const start = (this.gridCurrentPage - 1) * this.gridPerPage
      return this.filteredGridItems.slice(start, start + this.gridPerPage)
    }
  },
  watch: {
    gridSearch() { this.gridCurrentPage = 1; },
    gridColor() { this.gridCurrentPage = 1; },
    gridType() { this.gridCurrentPage = 1; },
    gridLength() { this.gridCurrentPage = 1; },
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
        this.loadPoles();
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
        this.loadWings();
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
    },
    deletePoleLoc(poleLoc) {
      deletePoleLocation(poleLoc.id)
        .then(() => {
          this.loadAssigned();
          this.loadPoles();
        });
    },
    deleteWingsLoc(wingLoc) {
      deleteWingsLocation(wingLoc.id)
        .then(() => {
          this.loadAssigned();
          this.loadWings();
        });
    },
    assignGridSelected() {
      // Kiválasztott pole/wing szétválogatása
      const polesToAssign = [];
      const wingsToAssign = [];
      for (const key of this.gridSelected) {
        const [type, idStr] = key.split('-');
        const id = Number(idStr);
        const quantity = this.gridQuantities[key] || 1;
        if (type === 'pole') polesToAssign.push({ pole_id: id, quantity });
        if (type === 'wing') wingsToAssign.push({ wing_id: id, quantity });
      }
      Promise.all([
        ...polesToAssign.map(p =>
          createPoleLocation({
            pole_id: p.pole_id,
            quantity: p.quantity,
            arena: this.arenaId
          })
        ),
        ...wingsToAssign.map(w =>
          createWingLocation({
            wing_id: w.wing_id,
            quantity: w.quantity,
            arena: this.arenaId
          })
        )
      ])
      .then(() => {
        this.successMessage = "Assigned selected items!";
        this.errorMessage = '';
        this.gridSelected = [];
        this.gridQuantities = {};
        this.loadAssigned();
        this.loadPoles();
        this.loadWings();
      })
      .catch(error => {
        this.errorMessage = "Error: " + (error.response?.data?.detail || error.message);
        this.successMessage = '';
      });
    }
  }
}
</script>
