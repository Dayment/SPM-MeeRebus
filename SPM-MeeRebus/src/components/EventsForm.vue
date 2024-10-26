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
            <th>Event ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(description, date) in apiDateDict" :key="date">
            <td>{{ date }}</td>
            <td>{{ description[0]}}</td>
            <td>{{ description[1]}}</td>

            <td>
              <!-- X Button to Remove Event -->
              <button @click="removeEvent(date)" class="btn btn-danger btn-sm">X</button>
            </td>
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
  import { getAllDepartments, getAllDatesWithEvents, getExistingEvents, deleteEvent } from '../api/api';

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
      }
    });
    const apiDateDict  = await getAllDatesWithEvents();

    this.apiDateDict = this.formatDatesToYYYYMMDD(apiDateDict);
    console.log(this.apiDateDict)
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
           const empId = localStorage.getItem("employeeId")
           await axios.post('http://48.218.168.55:5000/create-event', {
            date: this.selectedDate,
            empId: empId,
            creator: empId,
            description: this.description
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

      for (const [dateString, event] of Object.entries(dateDict)) {
        // Instead of manually creating the date, use dateString directly
        const formattedDate = dateString; // Use the date as-is

        // Access description and event_id directly from the event object
        const description = event[0] || "No description"; // First element is description
        const eventId = event[1] || "No event ID"; // Second element is event_id

        // Assign the description and event_id as the array value
        formattedDict[formattedDate] = [description, eventId];
      }

      return formattedDict;
    },

    async removeEvent(date) {
  // Check if the date exists in the object before attempting to delete it
  if (this.apiDateDict.hasOwnProperty(date)) {
    const eventID = this.apiDateDict[date][1]; // Access the event ID correctly from array
    try {
      const response = await deleteEvent(eventID);  // Assuming deleteEvent sends the delete request to your backend
      if (response) {
        delete this.apiDateDict[date];  // Remove event from the local object if deletion is successful
        window.alert('Deletion succeeded  .');
      } else {
        window.alert('Deletion failed.');
      }
    } catch (error) {
      console.error('Error during deletion:', error);
    }
  }
}
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
  