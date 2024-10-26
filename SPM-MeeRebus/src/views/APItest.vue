<script>
import axios from 'axios';

// Method to call the Flask API
export default {
  methods: {
    // Method to call the Flask API for employee
    async testApi() {
      try {
        const response = await axios.get(
          'https://earnest-grace-production-04af.up.railway.app/employee',
        );
        localStorage.setItem('employee', JSON.stringify(response.data));
        console.log(response.data);
      } catch (error) {
        console.log(error);
      }
    },

    // Method to call the Flask API for arrangement
    async testApi2() {
      try {
        const response = await axios.get(
          'https://earnest-grace-production-04af.up.railway.app/arrangement',
        );
        localStorage.setItem('arrangement', JSON.stringify(response.data));
        console.log(response.data);
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>

<template>
  <div>
    <h1>Testing for API here</h1>
    <button @click="testApi2()">HELLO</button>
  </div>
</template>
