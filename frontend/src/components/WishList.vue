<template>
  <div>
    <h2>{{ t('submitWishlist') }}</h2>
    <div>
      <label>{{ t('arena') }}:</label>
      <select v-model="selectedArena" required>
        <option v-for="arena in arenas" :key="arena.id" :value="arena.id">
          {{ arena.name }}
        </option>
      </select>
    </div>
    <form @submit.prevent="submitWishlist" style="margin-top: 2rem;">
      <div style="margin-bottom: 16px; display: flex; gap: 12px;">
        <input
          v-model="gridSearch"
          type="text"
          :placeholder="t('searchByName')"
          style="padding:4px 10px; border-radius:4px; border:1px solid #bbb;"
        />
        <select v-model="gridColor" style="padding:4px 10px; border-radius:4px;">
          <option value="">{{ t('allColors') }}</option>
          <option v-for="color in gridAvailableColors" :key="color" :value="color">{{ color }}</option>
        </select>
        <select v-model="gridType" style="padding:4px 10px; border-radius:4px;">
          <option value="">{{ t('both') }}</option>
          <option value="pole">{{ t('pole') }}</option>
          <option value="wing">{{ t('wing') }}</option>
        </select>
        <!-- Length filter csak Pole esetén -->
        <select v-if="gridType === 'pole'" v-model="gridLength" style="padding:4px 10px; border-radius:4px;">
          <option value="">{{ t('allLengths') }}</option>
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
            {{ lang === 'hu' ? item.name_hu : item.name_en }}
          </div>
          <div style="color:#555;">
            {{ item.color }}
            <span v-if="item.length">, {{ item.length }} m</span>
          </div>
          <div style="font-size:13px; color:#888; margin-bottom:4px;">
            {{ t(item.type) }}
          </div>
          <div>{{ t('stock') }}: {{ item.number }}</div>
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
        {{ t('noResults') }}
      </div>

      <!-- Megjegyzés -->
      <div style="margin:24px 0;">
        <label for="wishlist-note">{{ t('note') }}</label>
        <textarea
          id="wishlist-note"
          v-model="note"
          rows="2"
          cols="40"
          :placeholder="t('writeNote') || 'Írj megjegyzést...'"
        ></textarea>
      </div>
      <div style="text-align:right; margin:24px 0;">
        <button type="submit" :disabled="gridSelected.length === 0">
          {{ t('submitWishlist') || 'Submit Wishlist' }}
        </button>
      </div>
    </form>
    <div v-if="successMessage" style="color:green;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red;">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { fetchActiveArenas, fetchPoles, fetchWings, wishList } from '@/api/api'
import translations from '@/translations'
import { mapState } from 'vuex'

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
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    },
    gridAvailableItems() {
      return [
        ...this.poles.map(p => ({ ...p, type: 'pole' })),
        ...this.wings.map(w => ({ ...w, type: 'wing' }))
      ];
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
      return Math.ceil(this.filteredGridItems.length / this.gridPerPage) || 1
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
    fetchActiveArenas().then(res => { this.arenas = res.data; });
    fetchPoles().then(res => { this.poles = res.data; });
    fetchWings().then(res => { this.wings = res.data; });
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://localhost:8000" + path;
    },
    submitWishlist() {
      if (!this.selectedArena) {
        this.errorMessage = this.t('selectArena') || "Please select an arena!";
        return;
      }
      // Pole és Wing itemek összegyűjtése checkbox szerint
      const pole_items = [];
      const wing_items = [];
      for (const key of this.gridSelected) {
        const [type, idStr] = key.split('-');
        const id = Number(idStr);
        const quantity = this.gridQuantities[key] || 1;
        if (type === 'pole') pole_items.push({ pole: id, quantity });
        if (type === 'wing') wing_items.push({ wing: id, quantity });
      }

      if (pole_items.length === 0 && wing_items.length === 0) {
        this.errorMessage = this.t('addAtLeastOne') || "Please add at least one item!";
        return;
      }

      wishList({
        arena: this.selectedArena,
        note: this.note,
        pole_items_input: pole_items,
        wing_items_input: wing_items
      })
      .then(() => {
        this.successMessage = this.t('wishlistSaved') || "Wishlist saved!";
        this.errorMessage = "";
        this.gridSelected = [];
        this.gridQuantities = {};
        this.note = "";
      })
      .catch(err => {
        this.successMessage = "";
        this.errorMessage = this.t('errorOccurred') + ": " + (err.response?.data?.detail || err.message);
      });
    }
  }
}
</script>
