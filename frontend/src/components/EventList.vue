<template>
  <div class="container">
    <div class="box-border">
      <h2>{{ t('runningEvents') }}</h2>
      <div v-for="event in runningEvents"
           :key="event.id"
           class="event-item"
           @click="goToEventDetails(event)">
        <div>
          <b>{{ lang === 'hu' ? event.name_hu || event.name : event.name_en || event.name }}</b>
        </div>
        <div class="event-item-date">
          {{ event.start_date }} - {{ event.end_date }}
        </div>
      </div>
      <div v-if="runningEvents.length === 0" class="muted">{{ t('noRunningEvents') }}</div>
    </div>

    <div class="box-border">
      <h2>{{ t('upcomingEvents') }}</h2>
      <div v-for="event in upcomingEvents"
           :key="event.id"
           class="event-item"
           @click="goToEventDetails(event)">
        <div>
          <b>{{ lang === 'hu' ? event.name_hu || event.name : event.name_en || event.name }}</b>
        </div>
        <div class="event-item-date">
          {{ event.start_date }} - {{ event.end_date }}
        </div>
      </div>
      <div v-if="upcomingEvents.length === 0" class="muted">{{ t('noUpcomingEvents') }}</div>
    </div>
  </div>
</template>

<script>
import { fetchEvents } from '@/api/api'
import { mapState } from 'vuex'
import translations from '@/translations'

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
  computed: {
    ...mapState(['lang']),
    t() {
      return key => translations[this.lang]?.[key] || key
    }
  },
  methods: {
    goToEventDetails(event) {
      this.$router.push({ name: 'event-details', params: { id: event.id } })
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
