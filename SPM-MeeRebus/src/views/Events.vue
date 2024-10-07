<template>
    <div class="apply-events">
      <h2 class="heading">Apply for Events</h2><br>
  
      <!-- Ad-Hoc Requests Info -->
      <!-- <RequestInfo :remainingRequests="remainingAdHocRequests" /> --> 
    <EventsForm
      :min="minDate"
      :max="maxDate"
      required
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
        const today = new Date();
        this.minDate = today.toISOString().split('T')[0];
        const oneYearFromNow = new Date(today.setFullYear(today.getFullYear() + 1));
        this.maxDate = oneYearFromNow.toISOString().split('T')[0];
    },
    handleSubmit() {
        if (this.checkWhetherExistingDateOverlap(this.selectedDate)) {
          alert('This event date overlaps with an existing event. Please choose a different date.');
        } else {
          // Proceed with form submission (e.g., API call to save the new event)
          alert('Event submitted successfully!');
          // Clear the form
          this.eventName = '';
          this.selectedDepartment = '';
          this.selectedDate = '';
        }
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
  