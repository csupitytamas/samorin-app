import { createRouter, createWebHistory } from 'vue-router'
import EventCreate from "@/components/EventCreate.vue";
import EventList from "@/components/EventList.vue";
import ArenaCreate from "@/components/ArenaCreate.vue";
import ArenaEdit from "@/components/ArenaEdit.vue";
import ArenaDashboard from "@/components/ArenaDashboard.vue";

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
  path: '/arenas/:arenaId/dashboard',
  name: 'arena-dashboard',
  component: ArenaDashboard,
  props: true,
}

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
