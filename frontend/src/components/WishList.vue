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

      <div>
        <h5>In (Warehouse)</h5>
        <ul style="list-style:none; padding:0;">
          <li v-for="item in selectedPreviewItems.filter(i => i.mode === 'in')"
              :key="'in-' + item.key"
              style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <div>
              <b>{{ item.label }}</b> — {{ item.quantity }} db
            </div>
            <button class="trash-button" @click="removeFromPreview(item)">🗑️</button>
          </li>
        </ul>
      </div>

      <div>
        <h5>Out (Arena)</h5>
        <ul style="list-style:none; padding:0;">
          <li v-for="item in selectedPreviewItems.filter(i => i.mode === 'out')"
              :key="'out-' + item.key"
              style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <div>
              <b>{{ item.label }}</b> — {{ item.quantity }} db
            </div>
            <button class="trash-button" @click="removeFromPreview(item)">🗑️</button>
          </li>
        </ul>
      </div>
    </div>

   <div class="box" style="margin-bottom:1.5rem;">
  <div class="inline-form row" style="display: flex; flex-wrap: wrap;">
    <input v-model="gridSearch" type="text" :placeholder="t('searchByName')" />

    <select v-model="gridColor" style="flex: 1 1 1rem; min-width: 0.1rem;">
      <option value="">{{ t('allColors') }}</option>
      <option v-for="color in gridAvailableColors" :key="color" :value="color">{{ color }}</option>
    </select>

    <select v-model="gridType" style="flex: 1 1 1rem; min-width: 0.1rem;">
      <option value="">{{ t('both') }}</option>
      <option value="pole">{{ t('pole') }}</option>
      <option value="wing">{{ t('wing') }}</option>
    </select>

    <select v-if="gridType === 'pole'" v-model="gridLength" style="flex: 1 1 1rem; min-width: 0.1rem;">
      <option value="">{{ t('allLengths') }}</option>
      <option v-for="len in gridAvailableLengths" :key="len" :value="len">{{ len }} m</option>
    </select>
  </div>
</div>

<h3> {{ t('chooseFromItems') }} </h3>
    <div style="margin:1rem 0;">
         <label>
      <input type="radio" value="in" v-model="viewMode" />
      {{ t('inMode') }}
    </label>
    <label style="margin-left:1rem;">
      <input type="radio" value="out" v-model="viewMode" />
      {{ t('outMode') }}
    </label>
    </div>


    <div class="box">
      <div class="arena-grid compact">
        <div
          v-for="item in paginatedGridItems"
          :key="item.type + '-' + item.id"
          class="table-row-card small-card"
          :class="{ selected: isSelected(item) }"
          @click="toggleGridItem(item)"
        >
          <div class="checkbox-wrapper-29 wishlist-checkbox"
               style="position:absolute; top:1rem; left:1rem; transform: scale(0.6); background:none;">
            <label class="checkbox">
              <input
                type="checkbox"
                class="checkbox__input"
                :checked="isSelected(item)"
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
            {{ t('stock') }}: {{ item.number || item.quantity }}
          </div>
          <div v-if="isSelected(item)" style="margin-top:5px;">
            <input
              type="number"
              :max="item.number || item.quantity"
              min="1"
              :value="getQuantity(item)"
              @input="updateQuantity(item, $event.target.value)"
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
      <button type="button" @click="submitWishlist" :disabled="selectedItems.length === 0">
        {{ t('assignSelected') }}
      </button>
    </div>

    <div v-if="popupMessage" class="popup-modal">
      {{ popupMessage }}
    </div>

    <div v-if="fullscreenImage" class="image-modal" @click.self="fullscreenImage = null">
      <img :src="fullscreenImage" alt="Full image" />
      <button class="modal-close-btn" @click="fullscreenImage = null">Close</button>
    </div>
  </div>
</template>

<script>
import { fetchActiveArenas, fetchPoles, fetchWings, wishList, fetchPoleLocationsByArena, fetchWingLocationsByArena } from '@/api/api'
import translations from '@/translations'
import { mapState } from 'vuex'

export default {
  name: 'WishlistCreate',
  data() {
    return {
      arenas: [],
      poles: [],
      wings: [],
      arenaItems: [],
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
      selectedItems: [],
      fullscreenImage: null,
      viewMode: 'in',
      popupMessage: "",
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    },
        selectedPreviewItems() {
      return this.selectedItems.map(sel => {
        const [type, idStr] = sel.key.split('-');
        const id = parseInt(idStr);
        const allItems = this.poles.concat(this.wings, this.arenaItems);
        const item = allItems.find(i => String(i.id) === String(id) && i.type === type);
        console.log('[selectedPreviewItems]', sel, 'found item:', item);
        return {
          label: item
            ? (this.lang === 'hu' ? item.name_hu : item.name_en) +
              ` (${item.color}${item.length ? ', ' + item.length + ' m' : ''})`
            : `(${type}-${idStr})`,
          quantity: sel.quantity,
          mode: sel.mode,
          key: sel.key
        };
      });
    },

    gridAvailableItems() {
      if (this.viewMode === 'in') {
        return [
          ...this.poles.map(p => ({ ...p, type: 'pole' })),
          ...this.wings.map(w => ({ ...w, type: 'wing' }))
        ];
      } else if (this.viewMode === 'out' && this.selectedArena !== "default") {
        return this.arenaItems;
      }
      return [];
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
    selectedArena(newVal) {
      if (this.viewMode === 'out' && newVal !== "default") {
        this.loadArenaItems(newVal);
      }
    },
    viewMode(newVal) {
      if (newVal === 'out' && this.selectedArena !== "default") {
        this.loadArenaItems(this.selectedArena);
      }
    },
    gridSearch() { this.gridCurrentPage = 1; },
    gridColor() { this.gridCurrentPage = 1; },
    gridType() { this.gridCurrentPage = 1; },
    gridLength() { this.gridCurrentPage = 1; },
  },
  mounted() {
    fetchActiveArenas().then(res => { this.arenas = res.data; });
    fetchPoles().then(res => { this.poles = res.data.map(p => ({ ...p, type: 'pole' })); });
    fetchWings().then(res => { this.wings = res.data.map(w => ({ ...w, type: 'wing' })); });
  },
  methods: {
     loadArenaItems(arenaId) {
      this.arenaItems = [];
      fetchPoleLocationsByArena(arenaId).then(res => {
        this.arenaItems.push(...res.data.map(p => {
          const item = {
            id: p.pole?.id,
            type: 'pole',
            arenaId: arenaId,
            name_hu: p.pole?.name_hu,
            name_en: p.pole?.name_en,
            color: p.pole?.color,
            length: p.pole?.length,
            picture: p.pole?.picture,
            quantity: p.quantity
          };
          return item;
        }));
      });
      fetchWingLocationsByArena(arenaId).then(res => {
      this.arenaItems.push(...res.data.map(w => {
        const item = {
          id: w.wing?.id,    // <--- EZ A LÉNYEG
          type: 'wing',
          arenaId: arenaId,
          name_hu: w.wing?.name_hu,
          name_en: w.wing?.name_en,
          color: w.wing?.color,
          picture: w.wing?.picture,
          quantity: w.quantity
        };
        return item;
           }));
          });
    },
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://13.48.70.78:8000" + path;
    },
    isSelected(item) {
      return this.selectedItems.some(e => e.key === (item.type + '-' + item.id) && e.mode === this.viewMode);
    },
    getQuantity(item) {
      const entry = this.selectedItems.find(e => e.key === (item.type + '-' + item.id) && e.mode === this.viewMode);
      return entry ? entry.quantity : '';
    },
    updateQuantity(item, val) {
      const entry = this.selectedItems.find(e => e.key === (item.type + '-' + item.id) && e.mode === this.viewMode);
      if (entry) entry.quantity = Number(val);
    },
          toggleGridItem(item) {
        let id = item.id || (item.pole && item.pole.id) || (item.wing && item.wing.id);
        if (!id) {
          return;
        }
        const key = item.type + '-' + id;
        const index = this.selectedItems.findIndex(e => e.key === key && e.mode === this.viewMode);
        if (index >= 0) {
          this.selectedItems.splice(index, 1);
        } else {
          this.selectedItems.push({
            key,
            quantity: 1,
            mode: this.viewMode
          });
        }
      },
    removeFromPreview(item) {
      const index = this.selectedItems.findIndex(e => e.key === item.key && e.mode === item.mode);
      if (index >= 0) this.selectedItems.splice(index, 1);
    },
    submitWishlist() {
  if (!this.selectedArena) {
    this.errorMessage = this.t('selectArena') || "Please select an arena!";
    return;
  }

  const pole_items = [];
  const wing_items = [];
  for (const sel of this.selectedItems) {
    const [type, idStr] = sel.key.split('-');
    const id = parseInt(idStr);
    if (!id || isNaN(id)) continue;
    if (type === 'pole') pole_items.push({
      pole: id,
      quantity: sel.quantity,
      mode: sel.mode  // <<< ez a fontos
    });
    if (type === 'wing') wing_items.push({
      wing: id,
      quantity: sel.quantity,
      mode: sel.mode
    });
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
    this.popupMessage = this.t('wishlistSaved') || "Wishlist saved!";
    this.selectedItems = [];
    this.note = "";
    setTimeout(() => this.popupMessage = '', 1000);
  })
  .catch(err => {
    this.popupMessage = this.t('errorOccurred') + ": " + (err.response?.data?.detail || err.message);
    setTimeout(() => this.popupMessage = '', 5000);
  });
  }
  }
}

</script>
