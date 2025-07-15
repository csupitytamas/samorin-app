<template>
  <div v-if="wishlist" class="container">
    <h2>{{ t('editWishlist') }} ({{ wishlist.arena_name }})</h2>

    <div class="box">
      <label>{{ t('note') }}:</label>
      <textarea v-model="note" rows="3" :placeholder="t('writeNote')"
        style="width:100%; border:1px solid rgba(255,255,255,0.15); background:var(--bg-color); color:var(--text-color); border-radius:var(--border-radius); padding:var(--padding-s);">
      </textarea>
    </div>

    <div class="box-border">
      <h3>{{ t('wishlistItems') }}</h3>
      <div v-if="wishlistItems.length === 0" class="muted">{{ t('noItemsInWishlist') }}</div>
      <div v-for="item in wishlistItems" :key="item.type + '-' + item.id" class="wishlist-card">
        <div class="wishlist-header">
          <div style="display:flex; align-items:center;">
            <span @click="removeItemFromWishlist(item)" class="trash-button">×</span>
            <img v-if="item.picture" :src="fullImageUrl(item.picture)" class="table-image" style="margin-left:0.8rem;">
            <div style="margin-left:0.8rem;">
              <b>{{ lang === 'hu' ? item.name_hu : item.name_en }}</b>
              <div style="font-size:var(--font-size-s); color:var(--muted-color);">
                <span v-if="item.type==='pole'">({{ item.color }}, {{ item.length }} m)</span>
                <span v-else>({{ item.color }})</span>
              </div>
            </div>
          </div>
          <div>
            <input type="number" v-model.number="item.quantity" min="1" :max="item.number"
              style="width:60px; background:var(--bg-color); color:var(--text-color); border:1px solid rgba(255,255,255,0.15); border-radius:var(--border-radius); padding:var(--padding-s);">
            <span style="font-size:var(--font-size-s); color:var(--muted-color); margin-left:0.5rem;">{{ t(item.type) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="box-border">
      <h3>{{ t('addNewItemsFromWarehouse') }}</h3>
      <div class="inline-form row">
        <input v-model="gridSearch" type="text" :placeholder="t('searchByName')">
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
      <div v-for="item in paginatedGridItems"
           :key="item.type + '-' + item.id"
           class="table-row-card small-card"
           :class="{ selected: gridSelected.includes(item.type + '-' + item.id) }"
           @click="toggleGridItem(item)">

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

        <img v-if="item.picture" :src="fullImageUrl(item.picture)"
             class="table-image small-image clickable-image"
             @click.stop="fullscreenImage = fullImageUrl(item.picture)">
        <div style="margin-top:4px; font-weight:bold;">
          {{ lang === 'hu' ? item.name_hu : item.name_en }}
        </div>
        <div style="margin-top:2px;">
          {{ item.color }}<span v-if="item.length">, {{ item.length }} m</span>
        </div>
        <div style="font-size:var(--font-size-s); color:var(--muted-color); margin-top:2px;">
          {{ t(item.type) }}
        </div>
        <div style="margin-top:3px;">
          {{ t('stock') }}: {{ item.number }}
        </div>
        <div v-if="gridSelected.includes(item.type + '-' + item.id)" style="margin-top:5px;">
          <input type="number" :max="item.number" min="1"
                 v-model.number="gridQuantities[item.type + '-' + item.id]"
                 :placeholder="`Max: ${item.number}`"
                 style="width:60px; background:var(--bg-color); color:var(--text-color);
                        border:1px solid rgba(255,255,255,0.15); border-radius:var(--border-radius);
                        padding:var(--padding-s);">
        </div>
      </div>
    </div>

      <div class="dot-pagination" v-if="gridPageCount > 1">
    <span
      v-for="page in gridPageCount"
      :key="page"
      class="dot"
      :class="{ active: gridCurrentPage === page }"
      @click="gridCurrentPage = page"
      title="Page {{ page }}"
    ></span>
      </div>


      <div v-if="paginatedGridItems.length === 0" class="muted centered">{{ t('noResults') }}</div>
      <div style="text-align:center; margin-top:var(--padding-m);">
        <button @click="addSelectedToWishlist" :disabled="gridSelected.length === 0">
          {{ t('assignSelected') }}
        </button>
      </div>
    </div>


    <div style="margin-top:var(--padding-l); text-align:center;">
      <button @click="saveEdit" :disabled="wishlistItems.length === 0">{{ t('save') }}</button>
      <button @click="$router.back()" style="margin-left:1rem;">{{ t('cancel') }}</button>
    </div>
    <div v-if="successMessage" style="color:var(--accent-color); margin-top:0.8rem;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:#ff3860; margin-top:0.8rem;">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { fetchWishlist, updateWishlist, fetchPoles, fetchWings } from "@/api/api"
import translations from '@/translations'
import { mapState } from 'vuex'

export default {
  name: "WishlistEdit",
  data() {
    return {
      wishlist: null,
      note: "",
      poles: [],
      wings: [],
      wishlistItems: [],
      gridSearch: '',
      gridColor: '',
      gridType: '',
      gridLength: '',
      gridCurrentPage: 1,
      gridPerPage: 8,
      gridSelected: [],
      gridQuantities: {},
      successMessage: "",
      errorMessage: "",
      fullscreenImage: null
    }
  },
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    },
    gridAvailableItems() {
      const usedPoleIds = new Set(this.wishlistItems.filter(x => x.type === 'pole').map(x => x.id))
      const usedWingIds = new Set(this.wishlistItems.filter(x => x.type === 'wing').map(x => x.id))
      return [
        ...this.poles.filter(p => p.number > 0 && !usedPoleIds.has(p.id)).map(p => ({ ...p, type: 'pole' })),
        ...this.wings.filter(w => w.number > 0 && !usedWingIds.has(w.id)).map(w => ({ ...w, type: 'wing' }))
      ]
    },
    gridAvailableColors() {
      return [...new Set(this.gridAvailableItems.map(i => i.color).filter(Boolean))];
    },
    gridAvailableLengths() {
      return [...new Set(this.gridAvailableItems.filter(i => i.type === 'pole').map(i => i.length).filter(Boolean))].sort((a, b) => a - b)
    },
    filteredGridItems() {
      return this.gridAvailableItems.filter(i =>
        (!this.gridSearch || (i.name_en && i.name_en.toLowerCase().includes(this.gridSearch.toLowerCase())) ||
          (i.name_hu && i.name_hu.toLowerCase().includes(this.gridSearch.toLowerCase()))) &&
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
  async mounted() {
    const id = this.$route.params.id
    try {
      const [wishlistRes, polesRes, wingsRes] = await Promise.all([
        fetchWishlist(id), fetchPoles(), fetchWings()
      ])
      this.wishlist = wishlistRes.data
      this.note = this.wishlist.note || ""
      this.poles = polesRes.data
      this.wings = wingsRes.data
      this.wishlistItems = [
        ...(this.wishlist.pole_items || []).map(p => ({
          ...this.poles.find(z => z.id === p.pole),
          type: 'pole', quantity: p.quantity
        })),
        ...(this.wishlist.wing_items || []).map(w => ({
          ...this.wings.find(z => z.id === w.wing),
          type: 'wing', quantity: w.quantity
        })),
      ]
    } catch (err) {
      this.errorMessage = this.t('couldNotLoadWishlist') || "Could not load wishlist"
    }
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return "";
      return path.startsWith('http') ? path : "http://13.48.70.78:8000" + path;
    },
    toggleGridItem(item) {
      const key = item.type + '-' + item.id
      if (this.gridSelected.includes(key)) {
        this.gridSelected = this.gridSelected.filter(k => k !== key)
        delete this.gridQuantities[key]
      } else {
        this.gridSelected.push(key)
        this.gridQuantities[key] = 1
      }
    },
    removeItemFromWishlist(item) {
      this.wishlistItems = this.wishlistItems.filter(x => !(x.type === item.type && x.id === item.id))
    },
    addSelectedToWishlist() {
      for (const key of this.gridSelected) {
        const [type, idStr] = key.split('-');
        const id = Number(idStr);
        const quantity = this.gridQuantities[key] || 1;
        let item = null;
        if (type === 'pole') item = { ...this.poles.find(p => p.id === id), type: 'pole', quantity }
        if (type === 'wing') item = { ...this.wings.find(w => w.id === id), type: 'wing', quantity }
        if (item && !this.wishlistItems.some(x => x.type === type && x.id === id)) {
          this.wishlistItems.push(item)
        }
      }
      this.gridSelected = []
      this.gridQuantities = {}
    },
    async saveEdit() {
      const pole_items = this.wishlistItems.filter(x => x.type === 'pole').map(x => ({ pole: x.id, quantity: x.quantity || 1 }))
      const wing_items = this.wishlistItems.filter(x => x.type === 'wing').map(x => ({ wing: x.id, quantity: x.quantity || 1 }))
      if (pole_items.length === 0 && wing_items.length === 0) {
        this.errorMessage = this.t('addAtLeastOne') || "Please add at least one item!"
        return
      }
      try {
        await updateWishlist(this.wishlist.id, { note: this.note, pole_items_input: pole_items, wing_items_input: wing_items })
        this.successMessage = this.t('wishlistUpdated') || "Wishlist updated!"
        setTimeout(() => this.$router.back(), 1000)
      } catch (err) {
        this.errorMessage = this.t('updateFailed') || "Update failed!"
      }
    }
  }
}
</script>
