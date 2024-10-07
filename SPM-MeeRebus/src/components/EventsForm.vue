<template>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="event-name">Event Name:</label>
        <input
            type="text"
            v-model="eventName"
            id="event-name"
            class="form-control"
            placeholder="Enter the event name"
            required/>      
        </div>

        <div class="form-group">
          <label for="description">Description:</label>
          <textarea
            id="description"
            v-model="description"
            class="form-control"
            placeholder="Enter a brief description of the event"
            rows="4"
            required
          ></textarea>
      </div>  

    <label for="team-select">Select Department Affected:</label>
            <select v-model="selectedDepartment" id="department-select" class="form-control" required>
                <option v-for="department in existingDepartment" :key="department.id" :value="department.name">
                    {{ department.name }}
                </option>
            </select>    

      <div class="form-group">
        <label for="days" class="d-flex align-items-center">
        Select Event Date:
        <span
          data-bs-toggle="tooltip"
          data-bs-placement="top"
          title="Do not apply on dates where there are existing events"
          class="ms-2"
        >
          <i class="bi bi-info-circle" style="cursor: pointer;"></i>
        </span>
    </label>
      <input
      type="date"
      id="days"
      v-model="selectedDate"
      class="form-control"
      required
    />
      </div>
    <!-- Bootstrap Table to Display Events -->
    <div class="mt-4">
      <h3>Existing Events</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Date</th> 
            <th>Event Description</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(description, date) in apiDateDict" :key="date">
            <td>{{ date }}</td>
            <td>{{ description }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <button type="submit" class="btn btn-primary">Submit Event Request</button>
    </form>

        <!-- Success Message -->
    <div v-if="successMessage" class="success-message">
        {{ successMessage }}
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { getAllDepartments, getAllDatesWithEvents, getExistingEvents } from '../api/api';

  export default {
    name: 'EventsForm',
    props: {

    },
    async mounted() {
        const retrievedDepartment = await getAllDepartments(); // Call the API to fetch departments when the component is mounted
        this.existingDepartment = retrievedDepartment.map((departmentName, index) => {
          return {
          id: index + 1, // Assign an ID based on the index
          name: departmentName, // Use the name directly from the response
      };
    });
    const apiDateDict  = await getAllDatesWithEvents();
    await this.getExistingEventsDate()
    this.apiDateDict = this.formatDatesToYYYYMMDD(apiDateDict);
    console.log(this.apiDateDict);

    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(tooltipTriggerEl => {
    new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
    },  
    data() {
      return {
        eventName : '',
        selectedDepartment: '', // Variable for storing the selected departments
        existingDepartment: [ // Array of departments

        ],
        selectedDate: '',
        description: '',
        successMessage: '', // Add successMessage to data,
        apiDateDict: {},
        existingEvents: []
      };
    },
    computed: {

    },
    methods: {
        async getExistingEventsDate() {
        try {
          // Fetch existing events and assign them to existingEvents
          this.existingEvents = await getExistingEvents()
          this.existingEvents = this.existingEvents.map(event => {
          const dateObj = new Date(event);
          
          // Extract the components of the date
          const year = dateObj.getFullYear(); // Get the full year (e.g., 2024)
          const month = ('0' + (dateObj.getMonth() + 1)).slice(-2); // Add leading zero for month if necessary
          const day = ('0' + dateObj.getDate()).slice(-2); // Add leading zero for day if necessary

          // Combine them into the "YYYY-MM-DD" format
          return `${year}-${month}-${day}`;
      });    
            } catch (error) {
          console.error('Error fetching existing events:', error);
        }
      },

      checkWhetherExistingDateOverlap(selectedDate) {
      // Compare the selected date (already in YYYY-MM-DD format)
      return this.existingEvents.includes(selectedDate);
    },

    async handleSubmit() {
        if (this.checkWhetherExistingDateOverlap(this.selectedDate)) {
          console.log('failure')
          window.alert('This event date overlaps with an existing event. Please choose a different date.');
        } else {
           // Post request to create an event
           
           await axios.post('http://127.0.0.1:5000/create-event', {
            date: this.selectedDate,
        })
        .then(response => {
            console.log(response.data);  // Log the response to see what happens
            if (response.data.success) {
                window.alert('The event has been successfully created.');
            } else {
                window.alert('Failed to create the event.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            window.alert('An error occurred while creating the event.');
        });

        }
      },
      formatDatesToYYYYMMDD(dateDict) {
      const formattedDict = {};
      for (const [dateString, description] of Object.entries(dateDict)) {
        const date = new Date(dateString); // Convert to Date object
        const day = String(date.getDate()).padStart(2, '0'); // Get day with leading zero
        const month = String(date.getMonth() + 1).padStart(2, '0'); // Get month with leading zero
        const year = date.getFullYear(); // Get the full year

        formattedDict[`${year}-${month}-${day}`] = description; // Return formatted date as key
      }
      return formattedDict;
    },
  },
  };
  </script>
  
  <style scoped>
  .review-section {
    margin: 20px 0;
  }
  .form-group {
    margin-bottom: 20px; /* Adjust the value as needed */
}
.form-control {
    margin-bottom: 20px; /* Adjust the value as needed */
}
  </style>
  