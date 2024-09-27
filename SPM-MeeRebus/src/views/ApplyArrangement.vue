<template>
    <div class="apply-arrangement">
      <h2>Apply for WFH Arrangement</h2>
      
      <!-- Ad-Hoc Requests Info -->
      <RequestInfo :remainingRequests="remainingAdHocRequests" />
  
      <!-- WFH Request Form -->

      <WFHForm
        :blockedDays="blockedDays"
        :minDate="minDate"
        :maxDate="maxDate"
        @submitRequest="submitWFHRequest"
      />
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import RequestInfo from '../components/RequestInfo.vue';
  import WFHForm from '../components/WFHForm.vue';
  import { createWFHRequest } from '@/api/api';
  
  export default {
  name: 'ApplyArrangement',
  components: {
    RequestInfo,
    WFHForm,
  },
  data() {
    return {
      remainingAdHocRequests: 0,
      //min and max date to show error message
      minDate: '',
      maxDate: '',
      blockedDays: [],
      staff_id: localStorage.getItem('employeeId')|| null  //consider using global user context object
    };
  },
  methods: {
    async submitWFHRequest(payload) {
      try {
        payload.staff_id = this.staff_id;
        await createWFHRequest(payload);
        alert('WFH request submitted! It is now pending approval.');
      } catch (error) {
        console.error('Error submitting WFH request:', error);
        alert('Failed to submit WFH request. Please try again.');
      }
    },
  },
  onMounted() {
    const today = new Date();
    this.minDate = today.toISOString().split('T')[0];
    const oneYearFromNow = new Date(today.setFullYear(today.getFullYear() + 1));
    this.maxDate = oneYearFromNow.toISOString().split('T')[0];

  },
};

  </script>
  
  <style scoped>
  .apply-arrangement {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>
  