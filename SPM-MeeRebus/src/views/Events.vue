<template>
    <div class="apply-events">
      <h2 class="heading">Apply for Events</h2><br>
  
      <!-- Ad-Hoc Requests Info -->
      <!-- <RequestInfo :remainingRequests="remainingAdHocRequests" /> --> 
    <EventsForm
      
    />
    </div>
  </template>
  
  <script>
  import EventsForm from '../components/EventsForm.vue';

  export default {
    name: 'ApplyEvents',
    components: {
        EventsForm
    },
    data() {
      return {
      };
    },
    methods: {
    },
    onMounted() {

    },
  };
  </script>
  
  <style scoped>
    .apply-events {
    max-width: 600px;
    margin: 0 auto;
    margin-top: 20px; /* Adds space between the content and the navbar */
  }
  .heading {
    text-align: center; /* This centers the text horizontally */
  }
  </style>
  