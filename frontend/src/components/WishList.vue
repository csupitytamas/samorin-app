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

    <!-- GRID nézet minden eszközre -->
    <form @submit.prevent="submitWishlist" style="margin-top: 2rem;">
      <h3 style="font-weight:bold;">Válassz eszközöket (kártyás/grid, kereső/szűrő)</h3>
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
        <!-- Length filter csak Pole esetén -->
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

      <!-- Megjegyzés -->
      <div style="margin:24px 0;">
        <label for="wishlist-note">Megjegyzés (opcionális):</label>
        <textarea
          id="wishlist-note"
          v-model="note"
          rows="2"
          cols="40"
          placeholder="Írj megjegyzést..."></textarea>
      </div>
      <div style="text-align:right; margin:24px 0;">
        <button type="submit" :disabled="gridSelected.length === 0">
          Submit Wishlist
        </button>
      </div>
    </form>
    <div v-if="successMessage" style="color:green;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red;">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { fetchArenas, fetchPoles, fetchWings, wishList } from '@/api/api'

export default {
  name: 'WishlistCreate',
  data() {
    return {
      arenas: [],
      poles: [],
      wings: [],
      selectedArena: null,
      note: "",
      successMessage: '',
      errorMessage: '',
      // GRID
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
  mounted() {
    fetchArenas().then(res => { this.arenas = res.data; });
    fetchPoles().then(res => { this.poles = res.data; });
    fetchWings().then(res => { this.wings = res.data; });
  },
  computed: {
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

      // Kijelölt ID-kból külön pole_items, wing_items
      const pole_items = this.gridSelected
        .filter(key => key.startsWith('pole-'))
        .map(key => {
          const id = Number(key.split('-')[1]);
          return {
            pole: id,
            quantity: this.gridQuantities[key] || 1
          }
        })
        .filter(item => item.quantity > 0);

      const wing_items = this.gridSelected
        .filter(key => key.startsWith('wing-'))
        .map(key => {
          const id = Number(key.split('-')[1]);
          return {
            wing: id,
            quantity: this.gridQuantities[key] || 1
          }
        })
        .filter(item => item.quantity > 0);

      if (pole_items.length === 0 && wing_items.length === 0) {
        this.errorMessage = "Please add at least one item!";
        return;
      }

      wishList({
        arena: this.selectedArena,
        note: this.note,
        pole_items_input: pole_items,
        wing_items_input: wing_items
      })
      .then(() => {
        this.successMessage = "Wishlist saved!";
        this.errorMessage = "";
        this.gridSelected = [];
        this.gridQuantities = {};
        this.note = "";
      })
      .catch(err => {
        this.successMessage = "";
        this.errorMessage = "Error: " + (err.response?.data?.detail || err.message);
      });
    }
  }
}
</script>
