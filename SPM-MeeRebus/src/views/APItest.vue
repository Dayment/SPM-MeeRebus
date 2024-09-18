<script>
import axios from 'axios'


// Method to call the Flask API
export default {
  methods: {
    // Method to call the Flask API for employee
    async testApi() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/employee');
        console.log(response.data);  
      } catch (error) {
        console.log(error);
      }
    },

    // Method to call the Flask API for arrangement
    async testApi2() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/arrangement');
        console.log(response.data);  
      } catch (error) {
        console.log(error);
      }
    }
  }
};
</script>

<template>
    <div>
        <h1>Testing for API here</h1>
        <button @click="testApi2()">HELLO</button>
    </div>
</template>