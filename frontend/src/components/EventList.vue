<template>
  <div>
    <h2>Running Events </h2>
    <ul>
      <li v-for="event in runningEvents" :key="event.id" @click="goToEventDetails(event)" style="cursor:pointer;">
        <b>{{ event.name }}</b>
        <span> ({{ event.start_date }} - {{ event.end_date }})</span>
      </li>
      <li v-if="runningEvents.length === 0" style="color:gray;">No running events</li>
    </ul>

    <h2>Upcoming Events (starting within 1 month)</h2>
    <ul>
      <li v-for="event in upcomingEvents" :key="event.id" @click="goToEventDetails(event)" style="cursor:pointer;">
        <b>{{ event.name }}</b>
        <span> ({{ event.start_date }} - {{ event.end_date }})</span>
      </li>
      <li v-if="upcomingEvents.length === 0" style="color:gray;">No upcoming events</li>
    </ul>

    <div v-if="eventDetails">
      <h3>Arenas:</h3>
      <div v-for="arenaObj in eventDetails.arenas" :key="arenaObj.arena.id" style="margin-bottom: 1.5rem;">
        <b>{{ arenaObj.arena.name }}</b>
        <div>
          <span>Poles:</span>
          <ul>
            <li v-for="poleLoc in arenaObj.poles" :key="poleLoc.id">
              {{ poleLoc.pole.name_hu }} ({{ poleLoc.quantity }})
            </li>
          </ul>
        </div>
        <div>
          <span>Wings:</span>
          <ul>
            <li v-for="wingLoc in arenaObj.wings" :key="wingLoc.id">
              {{ wingLoc.wing.name_hu }} ({{ wingLoc.quantity }})
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { fetchEvents } from '@/api/api';

export default {
  name: "EventList",
  data() {
    return {
      events: [],
      runningEvents: [],
      upcomingEvents: [],
      eventDetails: null,
    }
  },
  methods: {
    goToEventDetails(event) {
      this.$router.push({ name: 'event-details', params: { id: event.id } });
    },
    filterEvents() {
      const today = new Date();
      const sevenDaysAgo = new Date(today);
      sevenDaysAgo.setDate(today.getDate() - 7);
      const oneMonthLater = new Date(today);
      oneMonthLater.setMonth(today.getMonth() + 1);

      function parse(d) { return new Date(d); }

      this.runningEvents = this.events.filter(e =>
        parse(e.start_date) >= sevenDaysAgo &&
        parse(e.start_date) <= today &&
        parse(e.end_date) >= today &&
        e.is_active
      );

      this.upcomingEvents = this.events.filter(e =>
        parse(e.start_date) > today &&
        parse(e.start_date) <= oneMonthLater &&
        e.is_active
      );
    }
  },
  mounted() {
    fetchEvents()
      .then(response => {
        this.events = response.data;
        this.filterEvents();
      })
      .catch(error => {
        console.error(error);
      });
  }
}
</script>