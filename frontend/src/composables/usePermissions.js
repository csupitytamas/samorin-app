import { computed } from 'vue'
import { useStore } from 'vuex'

export default function usePermissions() {
  const store = useStore()

  // Közvetlenül a Vuex store gettereket csomagoljuk computed property-be
  // Ezek a store getterek mindig bool vagy string, nem lesz undefined!
  const role = computed(() => store.getters.user?.role || '')
  const isLoggedIn = computed(() => store.getters.isLoggedIn)
  const isAdmin = computed(() => store.getters.isAdmin)
  const isChief = computed(() => store.getters.isChief)
  const isWorker = computed(() => store.getters.isWorker)
  const isCrew = computed(() => store.getters.isCrew)

  // Ezeket is computedként adjuk vissza, de csak a role-ra hivatkozva!
  // (nem lesz undefined sosem, max false)
  const canSeeEvents = computed(() => ['worker','chief','crew','admin'].includes(role.value))
  const canSeeArenas = computed(() => ['worker','chief','crew','admin'].includes(role.value))
  const canEditArenas = computed(() => isCrew.value || isAdmin.value)
  const canSeeArchivedEvents = computed(() => ['worker','chief','crew','admin'].includes(role.value))
  const canCreateWishlist = computed(() => ['chief','admin'].includes(role.value))
  const canSeeWishlists = computed(() => ['chief','crew','admin'].includes(role.value))

  // Általános helper
  const hasRole = (...roles) => computed(() => roles.includes(role.value))

  return {
    role,
    isLoggedIn,
    isAdmin,
    isChief,
    isWorker,
    isCrew,
    canSeeEvents,
    canSeeArenas,
    canEditArenas,
    canSeeArchivedEvents,
    canCreateWishlist,
    canSeeWishlists,
    hasRole,
  }
}