<script setup>
import Navbar from './components/Navbar.vue';
import { ref, onMounted } from 'vue';
import VueCal from 'vue-cal';
import 'vue-cal/dist/vuecal.css'; // Import default CSS
import axios from 'axios';

// Data for the calendar events
const events = ref([]);

// Fetch events or set default events
const fetchEvents = () => {
  const today = new Date();
  events.value = [
    {
      start: new Date(today.getTime() + 21.5 * 60 * 60 * 1000),
      end: new Date(today.getTime() + 22.5 * 60 * 60 * 1000),
      title: 'Here a summary',
      description: 'The description',
      location: 'Location',
    },
  ];
};

// Call fetchEvents when component is mounted
onMounted(() => {
  fetchEvents();
});
</script>

<template>
  <div id="app">
    <Navbar />
    <router-view></router-view>
  </div>
</template>

<style scoped>
@import url('https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css');
@import url('https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css');
</style>
