<script setup>
import { ref, onMounted } from 'vue'; // import ref to create reactive properties
import { useRouter } from 'vue-router';
import { getAllEmployee, getAllApprovedArrangement } from '../api/api';
import Calendar from '../components/Calendar.vue';

const router = useRouter();
const approvedWFHDetails = ref([]);

onMounted(async () => {
  const empId = localStorage.getItem('employeeId');
  if (!empId) {
    router.push('/');
  } else {
    try {
      const empDetails = await getAllEmployee(empId);
      const wfhDetails = await getAllApprovedArrangement(empId);

      approvedWFHDetails.value = wfhDetails;

      console.log('WFH Details:', wfhDetails);
    } catch (error) {
      console.error(error);
    }
  }
});
</script>

<template>
  <main>
    <Calendar :wfh-details="approvedWFHDetails" />
  </main>
</template>
