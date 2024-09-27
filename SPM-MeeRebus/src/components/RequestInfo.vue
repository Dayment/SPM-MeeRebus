<template>
    <div class="info-container">
      <p>You have {{ remainingRequests }} ad-hoc WFH requests left this month.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RequestInfo',
    props: {
      remainingRequests: {
        type: Number,
        required: true,
      },
    },
  };
  </script>
  
  <style scoped>
  .info-container {
    margin-bottom: 20px;
  }
  </style>
  