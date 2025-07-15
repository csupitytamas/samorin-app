<template>
  <div class="container">
    <h3>{{ t('assignedPoles') }}</h3>
    <div class="table-container">
      <table class="styled-table">
        <thead>
          <tr>
            <th>{{ t('name') }}</th>
            <th>{{ t('color') }}</th>
            <th>{{ t('length') }}</th>
            <th>{{ t('quantity') }}</th>
            <th>{{ t('image') }}</th>
            <th>{{ t('delete') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="poleLoc in assignedPoles" :key="poleLoc.id">
            <td>{{ lang === 'hu' ? poleLoc.pole.name_hu : poleLoc.pole.name_en }}</td>
            <td>{{ poleLoc.pole.color }}</td>
            <td>{{ poleLoc.pole.length }}</td>
            <td>{{ poleLoc.quantity }}</td>
            <td>
              <img
                v-if="poleLoc.pole.picture"
                :src="fullImageUrl(poleLoc.pole.picture)"
                alt="Pole"
                class="table-image clickable-image"
                @click="fullscreenImage = fullImageUrl(poleLoc.pole.picture)"
              />
            </td>
            <td>
              <button
                v-if="isAdmin || isCrew"
                @click="deletePoleLoc(poleLoc)"
                class="trash-button"
                title="Delete"
              >🗑️</button>
            </td>
          </tr>
          <tr v-if="assignedPoles.length === 0">
            <td colspan="6" class="muted" style="text-align:center;">{{ t('noPoles') }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3>{{ t('assignedWings') }}</h3>
    <div class="table-container">
      <table class="styled-table">
        <thead>
          <tr>
            <th>{{ t('name') }}</th>
            <th>{{ t('color') }}</th>
            <th>{{ t('quantity') }}</th>
            <th>{{ t('image') }}</th>
            <th>{{ t('delete') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wingLoc in assignedWings" :key="wingLoc.id">
            <td>{{ lang === 'hu' ? wingLoc.wing.name_hu : wingLoc.wing.name_en }}</td>
            <td>{{ wingLoc.wing.color }}</td>
            <td>{{ wingLoc.quantity }}</td>
            <td>
             <img
                  v-if="wingLoc.wing.picture"
                  :src="fullImageUrl(wingLoc.wing.picture)"
                  alt="Wing"
                  class="table-image clickable-image"
                  @click="fullscreenImage = fullImageUrl(wingLoc.wing.picture)"
                />
            </td>
            <td>
              <button
                v-if="isAdmin || isCrew"
                @click="deleteWingsLoc(wingLoc)"
                class="trash-button"
                title="Delete"
              >🗑️</button>
            </td>
          </tr>
          <tr v-if="assignedWings.length === 0">
            <td colspan="5" class="muted" style="text-align:center;">{{ t('noWings') }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <form v-if="isAdmin || isCrew" @submit.prevent="assignGridSelected" style="margin-top: 3rem;">
      <h3>{{ t('availableGrid') }}</h3>
     <div class="inline-form row">
  <input
    v-model="gridSearch"
    type="text"
    :placeholder="t('searchByName')"
  />
  <select v-model="gridColor">
    <option value="">{{ t('allColors') }}</option>
    <option v-for="color in gridAvailableColors" :key="color" :value="color">{{ color }}</option>
  </select>
  <select v-model="gridType">
    <option value="">{{ t('both') }}</option>
    <option value="pole">{{ t('pole') }}</option>
    <option value="wing">{{ t('wing') }}</option>
  </select>
  <select v-if="gridType === 'pole'" v-model="gridLength">
    <option value="">{{ t('allLengths') }}</option>
    <option v-for="len in gridAvailableLengths" :key="len" :value="len">{{ len }} m</option>
  </select>
</div>


<div class="arena-grid compact">
  <div
    v-for="item in paginatedGridItems"
    :key="item.type + '-' + item.id"
    class="table-row-card small-card"
    :class="{ selected: gridSelected.includes(item.type + '-' + item.id) }"
    @click="toggleGridItem(item)"
  >
    <input
      type="checkbox"
      :checked="gridSelected.includes(item.type + '-' + item.id)"
      class="grid-checkbox"
      style="position:absolute; top:8px; left:8px;"
      readonly
    />
    <img
      v-if="item.picture"
      :src="fullImageUrl(item.picture)"
      alt=""
      class="table-image small-image clickable-image"
      @click.stop="fullscreenImage = fullImageUrl(item.picture)"
    />
    <div style="margin-top:4px; font-weight:bold;">
      {{ lang === 'hu' ? item.name_hu : item.name_en }}
    </div>
    <div style="margin-top:2px;">
      {{ item.color }}<span v-if="item.length">, {{ item.length }} m</span>
    </div>
    <div style="font-size:13px; color:#aaa; margin-top:2px;">
      {{ t(item.type) }}
    </div>
    <div style="margin-top:3px;">
      {{ t('stock') }}: {{ item.number }}
    </div>
    <div
      v-if="gridSelected.includes(item.type + '-' + item.id)"
      style="margin-top:5px;"
    >
      <input
        type="number"
        :max="item.number"
        min="1"
        v-model.number="gridQuantities[item.type + '-' + item.id]"
        :placeholder="`Max: ${item.number}`"
        style="width:60px;"
        @click.stop
        @mousedown.stop
      />
    </div>
  </div>
</div>

<div class="dot-pagination">
  <span
    v-for="page in gridPageCount"
    :key="page"
    class="dot"
    :class="{ active: gridCurrentPage === page }"
    @click="gridCurrentPage = page"
  ></span>
</div>
      <div style="text-align:center; margin: 2rem 0;">
        <button type="submit" :disabled="gridSelected.length === 0">
          {{ t('assignSelected') }}
        </button>
      </div>
    </form>

    <div v-else class="muted" style="margin:3rem 0; text-align:center;">
      {{ t('noEditPermission') }}
    </div>

    <div style="text-align:center; margin-bottom:1.5rem;">
      <button type="button"
          @click="$router.push({ name: 'event-list' })">
    {{ t('save') || 'Save' }}
      </button>
    </div>

    <!-- Modal a nagy képhez -->
    <div v-if="fullscreenImage" class="image-modal" @click.self="fullscreenImage = null">
      <img :src="fullscreenImage" alt="Full image" />
      <button class="modal-close-btn" @click="fullscreenImage = null">Close</button>
    </div>

    <div v-if="popupMessage" class="popup-modal">
      {{ popupMessage }}
    </div>
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
import { mapState } from 'vuex'
import translations from '@/translations'


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
       fullscreenImage: null,
       popupMessage: "",
    }
  },
  computed: {
    ...mapState(['lang']),
    isAdmin() { return this.$store.getters.isAdmin },
  isCrew() { return this.$store.getters.isCrew },
  isChief() { return this.$store.getters.isChief },
  isWorker() { return this.$store.getters.isWorker },
  isLoggedIn() { return this.$store.getters.isLoggedIn },
  role() { return this.$store.getters.user?.role || '' },
    t() {
      return (key) => translations[this.lang]?.[key] || key;
    },
    gridAvailableItems() {
      return [
        ...this.poles.map(p => ({ ...p, type: 'pole' })),
        ...this.wings.map(w => ({ ...w, type: 'wing' }))
      ].filter(i => i.number > 0)
    },
    gridAvailableColors() {
      return [...new Set(this.gridAvailableItems.map(i => i.color).filter(Boolean))];
    },
    gridAvailableLengths() {
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
      return "http://13.48.70.78:8000" + path;
    },
    toggleGridItem(item) {
    const id = item.type + '-' + item.id;
    if (this.gridSelected.includes(id)) {
      this.gridSelected = this.gridSelected.filter(e => e !== id);
    } else {
      this.gridSelected.push(id);
    }
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
  showPopup(message) {
    this.popupMessage = message;
    setTimeout(() => {
      this.popupMessage = "";
    }, 1000);
  },
    deletePoleLoc(poleLoc) {
      deletePoleLocation(poleLoc.id)
        .then(() => {
          this.loadAssigned();
          this.loadPoles();
        });
       this.showPopup(this.t('poleDeleted'));
    },
    deleteWingsLoc(wingLoc) {
      deleteWingsLocation(wingLoc.id)
        .then(() => {
          this.loadAssigned();
          this.loadWings();
        });

      this.showPopup(this.t('wingDeleted'));
    },
    assignGridSelected() {
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
         this.showPopup(this.t('assignedSuccess'));
        this.errorMessage = '';
        this.gridSelected = [];
        this.gridQuantities = {};
        this.loadAssigned();
        this.loadPoles();
        this.loadWings();
      })
      .catch(error => {
         this.showPopup("❌ " + (error.response?.data?.detail || error.message));
        this.successMessage = '';
      });
    }
  }
}
</script>
