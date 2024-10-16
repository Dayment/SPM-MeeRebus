<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; 
import Calendar from '@/components/Calendar.vue';


const router = useRouter(); 

const approvedWFHDetails = ref([]);

onMounted(async () => {
  const empId = localStorage.getItem('employeeId');
  if (!empId) {
    router.push('/');
  } else {
    try {
      const wfhDetails = localStorage.getItem('empArrangement')
      approvedWFHDetails.value = JSON.parse(wfhDetails);

      console.log('WFH Details:', JSON.parse(wfhDetails));
    } catch (error) {
      console.error(error);
    }
  }
});
</script>

<template>
  <div>
    <Calendar :wfh-details="approvedWFHDetails"/>
  </div>
</template>