<template>
  <div class="container">
    <h2>{{ t('submitWishlist') }}</h2>

    <div class="inline-form row">
   <select v-model="selectedArena">
    <option disabled value="default">{{ t('selectArena') }}</option>
    <option v-for="arena in arenas" :key="arena.id" :value="arena.id">
      {{ arena.name }}
    </option>
  </select>
  </div>

  <div v-if="selectedPreviewItems.length" class="box" style="margin-bottom:1rem;">
  <h4 style="margin-bottom:0.5rem;">{{ t('selectedItems') }}</h4>
  <ul style="list-style:none; padding:0;">
    <li v-for="item in selectedPreviewItems"
        :key="item.type + '-' + item.id"
        style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
      <div>
        <b>{{ lang === 'hu' ? item.name_hu : item.name_en }}</b>
        <span style="color:var(--muted-color);">
          ({{ item.color }}<span v-if="item.length">, {{ item.length }} m</span>)
        </span>
        — {{ item.quantity }} db
      </div>
      <button class="trash-button"
              @click="removeFromPreview(item)">🗑️</button>
    </li>
  </ul>
</div>

  <div class="box" style="margin-bottom:1.5rem;">
  <div class="inline-form row" style="flex-wrap:wrap;">
    <input v-model="gridSearch" type="text" :placeholder="t('searchByName')" />
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
</div>
<div class="arena-grid compact">
  <div
    v-for="item in paginatedGridItems"
    :key="item.type + '-' + item.id"
    class="table-row-card small-card"
    :class="{ selected: gridSelected.includes(item.type + '-' + item.id) }"
    @click="toggleGridItem(item)"
  >
<div class="checkbox-wrapper-29 wishlist-checkbox"
     style="position:absolute; top:1rem; left:1rem; transform: scale(0.6); background:none;">
  <label class="checkbox">
    <input
      type="checkbox"
      class="checkbox__input"
      :checked="gridSelected.includes(item.type + '-' + item.id)"
      @click.stop="toggleGridItem(item)"
    />
    <span class="checkbox__label"></span>
  </label>
</div>
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
        <div v-if="gridSelected.includes(item.type + '-' + item.id)" style="margin-top:5px;">
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

    <div style="margin-top:1.5rem;">
      <label>{{ t('note') }}</label>
      <textarea
        v-model="note"
        rows="2"
        cols="40"
        :placeholder="t('writeNote')"
        style="width:100%; margin-top:0.5rem;"
      ></textarea>
    </div>

    <div style="text-align:center; margin-top:1.5rem;">
      <button type="button" @click="submitWishlist" :disabled="gridSelected.length === 0">
        {{ t('assignSelected') }}
      </button>
    </div>

    <div v-if="successMessage" style="color:green; margin-top:1rem;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red; margin-top:1rem;">{{ errorMessage }}</div>

    <div v-if="fullscreenImage" class="image-modal" @click.self="fullscreenImage = null">
      <img :src="fullscreenImage" alt="Full image" />
      <button class="modal-close-btn" @click="fullscreenImage = null">Close</button>
    </div>
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
         selectedArena: "default",
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
      fullscreenImage: null,

    }
  },
  computed: {
  ...mapState(['lang']),
  t() {
    return key => translations[this.lang]?.[key] || key
  },
  selectedPreviewItems() {
    return this.gridSelected.map(key => {
      const [type, idStr] = key.split('-');
      const id = Number(idStr);
      const item = this.gridAvailableItems.find(i => i.id === id && i.type === type);
      return {
        ...item,
        type,
        quantity: this.gridQuantities[key] || 1
      };
    });
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
    toggleGridItem(item) {
      const key = item.type + '-' + item.id;
      if (this.gridSelected.includes(key)) {
        this.gridSelected = this.gridSelected.filter(k => k !== key);
        delete this.gridQuantities[key];
      } else {
        this.gridSelected.push(key);
        this.gridQuantities[key] = 1;
      }
    },
     removeFromPreview(item) {
    const key = item.type + '-' + item.id;
    this.gridSelected = this.gridSelected.filter(k => k !== key);
    delete this.gridQuantities[key];
  },
    submitWishlist() {
      if (!this.selectedArena) {
        this.errorMessage = this.t('selectArena') || "Please select an arena!";
        return;
      }
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
