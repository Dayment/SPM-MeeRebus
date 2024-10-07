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

        <label for="team-select">Select Department Affected:</label>
            <select v-model="selectedDepartment" id="department-select" class="form-control" required>
                <option v-for="department in existingDepartment" :key="department.id" :value="department.name">
                    {{ department.name }}
                </option>
            </select>    

      <div class="form-group">
        <label for="days">Select Event Date:</label>
        <input
          type="date"
          id="days"
          v-model="selectedDate"
          class="form-control"
          :min="minDate"
          :max="maxDate"
          required
        />
      </div>

    <button type="submit" class="btn btn-primary">Submit Event Request</button>
    </form>
  </template>
  
  <script>
  export default {
    name: 'EventsForm',
    props: {

    },
    mounted() {
        const today = new Date();
        this.minDate = today.toISOString().split('T')[0];
        const oneYearFromNow = new Date(today.setFullYear(today.getFullYear() + 1));
        this.maxDate = oneYearFromNow.toISOString().split('T')[0];

        this.getDepartments(); // Call the API to fetch departments when the component is mounted
    },  
    data() {
      return {
        eventName : '',
        selectedDepartment: '', // Variable for storing the selected departments
        existingDepartment: [ // Array of departments

        ],
        selectedDate: '',
      };
    },
    computed: {

    },
    methods: {
        async getDepartments() {
            try {
                // const response = await axios.get('http://127.0.0.1:5000/arrangement');
                // this.departments = response.data;
                // this.existingDepartment = data; // Assign the fetched data to existingDepartment
            } catch (error) {
                console.error('Error fetching departments:', error);
            }
        },

        async getExistingEvents() {
        try {
          // Fetch existing events and assign them to existingEvents
          
          // const response = await axios.get('your_existing_events_api_endpoint');
          // this.existingEvents = response.data;
        } catch (error) {
          console.error('Error fetching existing events:', error);
        }
      },

      checkWhetherExistingDateOverlap(selectedDate) {
        const selectedEventDate = new Date(selectedDate);
        
        // Check for overlapping events
        return this.existingEvents.some(event => {
          const eventDate = new Date(event.date); // Assuming each event has a 'date' property
          return eventDate.toDateString() === selectedEventDate.toDateString();
        });
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
  