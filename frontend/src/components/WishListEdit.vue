<template>
  <div v-if="wishlist">
    <h2>{{ t('editWishlist') }} ({{ wishlist.arena_name }})</h2>
    <div>
      <label>{{ t('note') }}:</label>
      <textarea v-model="note" rows="3" cols="50" :placeholder="t('writeNote') || ''"></textarea>
    </div>

    <!-- Wishlist Items: egymás alatt -->
    <div style="margin-top: 2rem;">
      <h3>{{ t('wishlistItems') }}</h3>
      <div v-if="wishlistItems.length === 0" style="color:gray; margin-bottom:1em;">{{ t('noItemsInWishlist') }}</div>
      <div v-for="item in wishlistItems" :key="item.type + '-' + item.id" style="position:relative; margin-bottom:10px; border:1px solid #e1e1e1; border-radius:10px; padding:12px 14px 12px 48px; background:#f8f9fb;">
        <span
          @click="removeItemFromWishlist(item)"
          :title="t('remove')"
          style="position:absolute; left:12px; top:14px; cursor:pointer; font-size:19px; color:#e11d48; font-weight:bold; line-height:1;">
          ×
        </span>
        <img v-if="item.picture" :src="fullImageUrl(item.picture)" style="height:35px; max-width:50px; object-fit:contain; margin-right:8px;">
        <b>{{ lang === 'hu' ? item.name_hu : item.name_en }}</b>
        <span v-if="item.type==='pole'">({{ item.color }}, {{ item.length }} m)</span>
        <span v-else>({{ item.color }})</span>
        <span style="margin-left:10px; color:#888;">x</span>
        <input
          type="number"
          v-model.number="item.quantity"
          min="1"
          :max="item.number"
          style="width:60px; margin-left:4px;"
        />
        <span style="color:#aaa; margin-left:8px;">({{ t(item.type) }})</span>
      </div>
    </div>

    <!-- Warehouse grid, egymás alatt -->
    <div style="margin-top: 3.5rem;">
      <h3>{{ t('addNewItemsFromWarehouse') }}</h3>
      <div style="margin-bottom: 16px; display: flex; gap: 12px; flex-wrap: wrap;">
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
        <select v-if="gridType === 'pole'" v-model="gridLength" style="padding:4px 10px; border-radius:4px;">
          <option value="">{{ t('allLengths') }}</option>
          <option v-for="len in gridAvailableLengths" :key="len" :value="len">{{ len }} m</option>
        </select>
      </div>
      <div class="arena-grid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(210px,1fr)); gap:16px;">
        <div
          v-for="item in paginatedGridItems"
          :key="item.type + '-' + item.id"
          style="position:relative; border:1px solid #e1e1e1; border-radius:10px; padding:13px 8px 13px 36px; text-align:center; background:#fafbfc;"
        >
          <input
            type="checkbox"
            :id="`grid-check-${item.type}-${item.id}`"
            :value="item.type + '-' + item.id"
            v-model="gridSelected"
            style="position:absolute; left:8px; top:13px; width:17px; height:17px;"
          />
          <img v-if="item.picture" :src="fullImageUrl(item.picture)" alt="" style="height: 46px; margin-bottom: 6px; object-fit:contain;">
          <div style="font-weight:bold; margin-bottom:2px;">
            {{ lang === 'hu' ? item.name_hu : item.name_en }}
          </div>
          <div style="color:#555;">
            {{ item.color }}
            <span v-if="item.length">, {{ item.length }} m</span>
          </div>
          <div style="font-size:13px; color:#888; margin-bottom:4px;">{{ t('type') }}: {{ t(item.type) }}</div>
          <div>{{ t('stock') }}: {{ item.number }}</div>
          <div v-if="gridSelected.includes(item.type + '-' + item.id)" style="margin-top:6px;">
            <input
              type="number"
              :max="item.number"
              min="1"
              v-model.number="gridQuantities[item.type + '-' + item.id]"
              :placeholder="`${t('pcs')}: ${item.number}`"
              style="width:68px;"
            />
          </div>
        </div>
      </div>
      <!-- Pagination -->
      <div v-if="gridPageCount > 1" style="display:flex; gap:8px; justify-content:center; margin:20px 0 0 0;">
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
      <div style="text-align:right; margin:18px 0;">
        <button type="button" @click="addSelectedToWishlist" :disabled="gridSelected.length === 0">
          {{ t('addSelectedToWishlist') }}
        </button>
      </div>
    </div>

    <!-- MENTÉS -->
    <div style="margin:30px 0 0 0; text-align:right;">
      <button @click="saveEdit" :disabled="wishlistItems.length === 0">{{ t('save') }}</button>
      <button type="button" @click="$router.back()" style="margin-left:14px;">{{ t('cancel') }}</button>
    </div>
    <div v-if="successMessage" style="color:green; margin-top:6px;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red; margin-top:6px;">{{ errorMessage }}</div>
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
          type: 'pole',
          quantity: p.quantity
        })),
        ...(this.wishlist.wing_items || []).map(w => ({
          ...this.wings.find(z => z.id === w.wing),
          type: 'wing',
          quantity: w.quantity
        })),
      ]
      this.gridSelected = []
      this.gridQuantities = {}
    } catch (err) {
      this.errorMessage = this.t('couldNotLoadWishlist') || "Could not load wishlist"
    }
  },
  methods: {
    fullImageUrl(path) {
      if (!path) return "";
      if (path.startsWith('http')) return path;
      return "http://localhost:8000" + path;
    },
    removeItemFromWishlist(item) {
      this.wishlistItems = this.wishlistItems.filter(
        x => !(x.type === item.type && x.id === item.id)
      )
    },
    addSelectedToWishlist() {
      for (const key of this.gridSelected) {
        const [type, idStr] = key.split('-');
        const id = Number(idStr);
        const quantity = this.gridQuantities[key] || 1;
        let item = null;
        if (type === 'pole') {
          item = { ...this.poles.find(p => p.id === id), type: 'pole', quantity }
        }
        if (type === 'wing') {
          item = { ...this.wings.find(w => w.id === id), type: 'wing', quantity }
        }
        if (item) {
          if (!this.wishlistItems.some(x => x.type === type && x.id === id)) {
            this.wishlistItems.push(item)
          }
        }
      }
      this.gridSelected = []
      this.gridQuantities = {}
    },
    async saveEdit() {
      const pole_items = this.wishlistItems
        .filter(x => x.type === 'pole')
        .map(x => ({
          pole: x.id,
          quantity: x.quantity || 1
        }))
        .filter(item => item.quantity > 0)
      const wing_items = this.wishlistItems
        .filter(x => x.type === 'wing')
        .map(x => ({
          wing: x.id,
          quantity: x.quantity || 1
        }))
        .filter(item => item.quantity > 0)
      if (pole_items.length === 0 && wing_items.length === 0) {
        this.errorMessage = this.t('addAtLeastOne') || "Please add at least one item!";
        return;
      }
      try {
        await updateWishlist(
          this.wishlist.id, {
            note: this.note,
            pole_items_input: pole_items,
            wing_items_input: wing_items
          }
        )
        this.successMessage = this.t('wishlistUpdated') || "Wishlist updated!"
        setTimeout(() => {
          this.$router.back()
        }, 1000)
      } catch (err) {
        this.errorMessage = this.t('updateFailed') || "Update failed!"
      }
    }
  }
}
</script>
