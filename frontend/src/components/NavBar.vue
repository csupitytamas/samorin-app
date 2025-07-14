<template>
  <div class="dock-outer">
    <div class="dock-panel">
          <div
      v-for="(item, index) in computedItems"
      :key="index"
      class="dock-item"
      @mouseenter="hoveredIndex = index"
      @mouseleave="hoveredIndex = null"
      @click="goTo(item.to)"
      :style="{
        width: itemWidth(index) + 'px',
        height: itemWidth(index) + 'px'
      }"
    ><div class="dock-icon">
  <img v-if="item.iconType === 'img'" :src="item.iconSrc" alt="icon" class="icon-svg" />
  <span v-else v-html="item.icon"></span>
</div>
    </div>
    </div>
  </div>
</template>

<script>
import translations from '@/translations'
import { mapState } from 'vuex'
import archiveIcon from '@/assets/archive.svg'
import editIcon from '@/assets/edit.svg'
import listIcon from '@/assets/list.svg'
import profileIcon from '@/assets/user.svg'
import adminIcon from '@/assets/info.svg'
import createIcon from '@/assets/plus.svg'

export default {
  name: 'NavBar',
  data() {
    return {
      hoveredIndex: null,
      baseItemSize: 50,
      magnification: 70,
     items: [
      { iconType: 'img', iconSrc: listIcon, label: 'events', to: '/events/list', show: () => this.canSeeEvents },
      { iconType: 'img', iconSrc: createIcon, label: 'eventCreate', to: '/events/create', show: () => this.isAdmin },
      { iconType: 'img', iconSrc: archiveIcon, label: 'archivedEvents', to: '/archived-events', show: () => this.canSeeArchivedEvents },
      { iconType: 'img', iconSrc: editIcon, label: 'wishlistCreate', to: '/wishlist', show: () => this.canCreateWishlist },
      { iconType: 'img', iconSrc: profileIcon, label: 'profile', to: '/profile', show: () => this.isLoggedIn },
      { iconType: 'img', iconSrc: adminIcon, label: 'adminDashboard', to: '/admin', show: () => this.isAdmin }
    ]
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
    canSeeEvents() { return this.isAdmin || this.isCrew || this.isChief || this.isWorker },
    canSeeArchivedEvents() { return this.isAdmin || this.isCrew },
    canCreateWishlist() { return this.isAdmin || this.isCrew || this.isChief },
    computedItems() {
      return this.items.filter(item => item.show())
    },
    t() {
      return (key) => translations[this.lang]?.[key] || key;
    },
  },
  methods: {
    itemWidth(index) {
      return this.hoveredIndex === index ? this.magnification : this.baseItemSize;
    },
    goTo(path) {
      this.$router.push(path);
    }
  }
}
</script>

<style scoped>
.dock-outer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #060010;
  border-top: 1px solid #222;
  padding: 0.5rem 0;
  z-index: 999;
}
.dock-panel {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
}
.dock-item {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.dock-icon {
  font-size: 20px;
}
.dock-label {
  position: absolute;
  top: -1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: #060010;
  border: 1px solid #222;
  border-radius: 0.375rem;
  padding: 0.125rem 0.5rem;
  font-size: 0.75rem;
  color: #fff;
  white-space: nowrap;
}
</style>
