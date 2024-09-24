<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import Calendar from '@/components/Calendar.vue';
import TheWelcome from '../components/TheWelcome.vue';

const router = useRouter(); 

// onMounted(async () => {
//   // Retrieve employee ID from localStorage
//   const empId = localStorage.getItem('employeeId'); 

//     if (!empId) {
//         // If no employee ID, redirect to login page
//         router.push('/');
//     } else {
//         // If employee ID exists, call the API
//         await getEmpDetails
//         await getWFH(empId);
//     }
// });

// async function getEmpDetails(empId) {
//     try {
//         const response = await axios.get(`http://127.0.0.1:5000/employee/${empId}`);
//         console.log(response.data);
//     } catch (error) {
//         console.error('Error fetching Employee data:', error);
//     }
// }

// async function getWFH(empId) {
//     try {
//         const response = await axios.get(`http://127.0.0.1:5000/arrangement/emp/${empId}`);
//         localStorage.setItem('empArrangement', JSON.stringify(response.data));
//         console.log(response.data);
//     } catch (error) {
//         console.error('Error fetching WFH data:', error);
//     }
// }
</script>

<template>
  <div>
    <Calendar />
    <!-- Can use the Employee details to determine how to display the calendar here -->
    
  </div>
</template>