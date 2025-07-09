<template>
  <div>
    <h2>Edit Event</h2>
    <form @submit.prevent="saveEvent">
      <div>
        <label>Name:</label>
        <input v-model="event.name" required>
      </div>
      <div>
        <label>Start Date:</label>
        <input type="date" v-model="event.start_date" required>
      </div>
      <div>
        <label>End Date:</label>
        <input type="date" v-model="event.end_date" required>
      </div>
      <button type="submit">Save</button>
      <button @click="archiveEvent" type="button" style="color:orange;">Close Event</button>
    </form>

    <div v-if="successMessage" style="color:green; margin-top:10px;">{{ successMessage }}</div>
    <div v-if="errorMessage" style="color:red; margin-top:10px;">{{ errorMessage }}</div>

    <h3>Arenas</h3>
   <ul>
      <li v-for="arena in arenas" :key="arena.id">
        <template v-if="editingArenaId === arena.id">
          <input v-model="arenaNewName" @keyup.enter="saveArenaName(arena)" @blur="saveArenaName(arena)" style="width:120px;">
          <button @click="saveArenaName(arena)">Save</button>
          <button @click="cancelEditArena">Cancel</button>
        </template>
        <template v-else>
          {{ arena.name }}
          <button @click="startEditArena(arena)">Edit</button>
        </template>
      </li>
      <li v-if="arenas.length === 0" style="color:gray;">No arenas for this event</li>
    </ul>
  </div>
</template>

<script>
import {fetchEvent, updateEvent, deleteEvent, fetchArenas, updateArena, archiveEvent} from '@/api/api'

export default {
  name: "EventEdit",
  props: ['id'],
  data() {
    return {
      event: { name: '', start_date: '', end_date: '' },
      arenas: [],
      successMessage: '',
      errorMessage: '',
      editingArenaId: null,      // ← Kell a data-ban!
      arenaNewName: "",          // ← Kell a data-ban!
    }
  },
  methods: {
    loadData() {
      fetchEvent(this.id)
        .then(res => { this.event = res.data; })
        .catch(() => { this.errorMessage = "Could not load event data"; });

      fetchArenas()
        .then(res => {
          this.arenas = res.data.filter(a => a.event == this.id);
        });
    },
    saveEvent() {
      updateEvent(this.id, this.event)
        .then(() => {
          this.successMessage = "Event saved!";
          this.errorMessage = "";
          this.$router.push('/events/list');
        })
        .catch(() => {
          this.successMessage = "";
          this.errorMessage = "Could not save event!";
        });
    },
     archiveEvent() {
      if (!confirm("Are you sure you want to close and archive this event? All items will be returned to the warehouse and the state will be saved for history.")) return;
      archiveEvent(this.id)
        .then(() => {
          this.successMessage = "Event archived and all items returned!";
          this.errorMessage = "";
          this.$router.push('/events/list');
        })
        .catch(() => {
          this.successMessage = "";
          this.errorMessage = "Could not archive event!";
        });
    },
    deleteEvent() {
      if (!confirm("Are you sure you want to delete this event and all related arenas/poles/wings?")) return;
      deleteEvent(this.id)
        .then(() => {
          this.$router.push('/events/list');
        })
        .catch(() => {
          this.errorMessage = "Could not delete event!";
        });
    },
    goToArenaEdit(arena) {
      this.$router.push({ name: 'arena-edit', params: { arenaId: arena.id } });
    },
    // --- Ezeket is ide tedd ---
    startEditArena(arena) {
      this.editingArenaId = arena.id;
      this.arenaNewName = arena.name;
    },
    cancelEditArena() {
      this.editingArenaId = null;
      this.arenaNewName = "";
    },
    saveArenaName(arena) {
        if (!this.arenaNewName.trim() || this.arenaNewName === arena.name) {
          this.cancelEditArena();
          return;
        }
        updateArena(arena.id, { name: this.arenaNewName })
          .then(() => {
            // Helyben frissítheted (ez csak gyors trükk):
            // arena.name = this.arenaNewName;

            // HELYETTE: újratöltöd az adatokat a szerverről!
            this.loadData();           // EZT hívd meg!
            this.cancelEditArena();

          })
          .catch(() => {
            alert("Could not rename arena!");
          });
      }
  },
  mounted() {
    this.loadData();
  }
}

</script>