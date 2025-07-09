import { createRouter, createWebHistory } from 'vue-router'
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

const routes = [
    {
  path: '/',
  redirect: '/events/list'
  },
  {
    path: '/events/create',
    name: 'event-create',
    component: EventCreate
  },
  {
    path: '/events/list',
    name: 'event-list',
    component: EventList
  },
  {
  path: '/arenas/create/:eventId',
  name: 'arena-create',
  component: ArenaCreate,
  props: true
  },
  {
  path: '/arenas/:arenaId/edit',
  name: 'arena-edit',
  component: ArenaEdit,
  props: true
  },
  {
    path: '/events/:id/edit',
    name: 'event-edit',
    component: EventEdit,
    props: true
  },
  {
    path: '/events/:id/details',
    name: 'event-details',
    component: EventDetails,
    props: true
  },
  { path: '/wishlist/:arenaId?', name: 'wishlist', component: WishList, props: true},
  { path: '/archived-events/:id/details', name: 'archived-event-details', component: ArchivedEventDetails, props: true},
  { path: '/archived-events', name: 'archived-events', component: ArchivedEvents},
  { path: '/register', name: 'register', component: RegisterForm},
  { path: '/login', name: 'login', component: LoginForm},
  { path: '/admin', name: 'admin-dashboard', component: AdminDashboard },
  { path: '/admin/users', name: 'user-admin', component: UserAdmin },
  { path: '/admin/pole', name: 'pole-create', component: PoleCreate },
  { path: '/admin/wings', name: 'wings-create', component: WingsCreate },
  { path: '/profile', name: 'profile', component: Profile }


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
