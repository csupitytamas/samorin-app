import { createRouter, createWebHistory } from 'vue-router'
import store from "@/store"

import EventCreate from "@/components/EventCreate.vue";
import EventList from "@/components/EventList.vue";
import ArenaCreate from "@/components/ArenaCreate.vue";
import ArenaEdit from "@/components/ArenaEdit.vue";
import EventDetails from "@/components/EventDetails.vue";
import EventEdit from "@/components/EventEdit.vue";
import WishList from "@/components/WishList.vue";
import ArchivedEventDetails from "@/components/ArchivedEventDetails.vue";
import ArchivedEvents from "@/components/ArchivedEvents.vue";
import RegisterForm from "@/components/RegisterForm.vue";
import LoginForm from "@/components/LoginForm.vue";
import AdminDashboard from "@/components/AdminDashboard.vue"
import UserAdmin from "@/components/UserAdmin.vue"
import PoleCreate from "@/components/PoleCreate.vue"
import WingsCreate from "@/components/WingsCreate.vue"
import Profile from "@/components/Profile.vue";
import WishListEdit from "@/components/WishListEdit.vue";
import EventWishlists from "@/components/EventWishlists.vue";

const routes = [
  {
    path: '/',
    redirect: '/events/list'
  },
  {
    path: '/events/create',
    name: 'event-create',
    component: EventCreate,
    meta: { requiresAuth: true, adminOnly: true }
  },
  {
    path: '/events/list',
    name: 'event-list',
    component: EventList,
    meta: { requiresAuth: true }
  },
  {
    path: '/arenas/create/:eventId',
    name: 'arena-create',
    component: ArenaCreate,
    props: true,
    meta: { requiresAuth: true, adminOrCrew: true }
  },
  {
    path: '/arenas/:arenaId/edit',
    name: 'arena-edit',
    component: ArenaEdit,
    props: true,
    meta: { requiresAuth: true, adminOrCrew: true }
  },
  {
    path: '/events/:id/edit',
    name: 'event-edit',
    component: EventEdit,
    props: true,
    meta: { requiresAuth: true, adminOnly: true }
  },
  {
    path: '/events/:id/details',
    name: 'event-details',
    component: EventDetails,
    props: true,
    meta: { requiresAuth: true }
  },
  { path: '/wishlist/:arenaId?', name: 'wishlist', component: WishList, props: true, meta: { requiresAuth: true, chiefOrAdmin: true }},
  { path: '/archived-events/:id/details', name: 'archived-event-details', component: ArchivedEventDetails, props: true, meta: { requiresAuth: true }},
  { path: '/archived-events', name: 'archived-events', component: ArchivedEvents, meta: { requiresAuth: true }},
  { path: '/register', name: 'register', component: RegisterForm },
  { path: '/login', name: 'login', component: LoginForm },
  { path: '/admin', name: 'admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, adminOnly: true } },
  { path: '/admin/users', name: 'user-admin', component: UserAdmin, meta: { requiresAuth: true, adminOnly: true } },
  { path: '/admin/pole', name: 'pole-create', component: PoleCreate, meta: { requiresAuth: true, adminOnly: true } },
  { path: '/admin/wings', name: 'wings-create', component: WingsCreate, meta: { requiresAuth: true, adminOnly: true } },
  { path: '/profile', name: 'profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/wishlist/edit/:id', name: 'wishlist-edit', component: WishListEdit, props: true, meta: { requiresAuth: true, chiefOrAdmin: true }},
  {
    path: '/events/:eventId/wishlists',
    name: 'event-wishlists',
    component: EventWishlists,
    props: true,
    meta: { requiresAuth: true, crewOrChiefOrAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ROUTE GUARD
router.beforeEach((to, from, next) => {
  const user = store.state.user
  const isLoggedIn = !!user
  const role = user?.role

  // Csak bejelentkezett user láthatja azokat, ahol szükséges
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ name: 'login' })
  }

  // Admin-only oldal
  if (to.meta.adminOnly && role !== 'admin') {
    return next({ name: 'event-list' })
  }

  // Crew vagy Admin
  if (to.meta.adminOrCrew && !(role === 'admin' || role === 'crew')) {
    return next({ name: 'event-list' })
  }

  // Chief vagy Admin
  if (to.meta.chiefOrAdmin && !(role === 'admin' || role === 'chief')) {
    return next({ name: 'event-list' })
  }

  // Crew, Chief, vagy Admin
  if (to.meta.crewOrChiefOrAdmin && !(role === 'admin' || role === 'chief' || role === 'crew')) {
    return next({ name: 'event-list' })
  }

  // Minden rendben, tovább
  next()
})

export default router