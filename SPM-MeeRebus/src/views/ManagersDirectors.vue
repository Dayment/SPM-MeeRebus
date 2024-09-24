<script setup>
import { ref, computed, onMounted } from 'vue'; 
import { useRouter } from 'vue-router';
import { getAllEmployee, getAllApprovedArrangement } from '../api/api';
import Calendar from '../components/Calendar.vue';

const router = useRouter();
const approvedWFHDetails = ref([]);
const searchQuery = ref(''); 
const startDate = ref(null); 
const endDate = ref(null); 

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

const filteredWFHDetails = computed(() => {
  return approvedWFHDetails.value.filter((wfh) => {
    const fullName =
      `${wfh.employee.staff_fname} ${wfh.employee.staff_lname}`.toLowerCase();
    const dept = wfh.employee.dept.toLowerCase();
    const position = wfh.employee.position.toLowerCase();
    const reason = (wfh.reason || 'No Reason Provided').toLowerCase();
    const wfhDate = new Date(wfh.date);

    const isWithinDateRange =
      (!startDate.value || new Date(startDate.value) <= wfhDate) &&
      (!endDate.value || wfhDate <= new Date(endDate.value));

    return (
      isWithinDateRange &&
      (fullName.includes(searchQuery.value.toLowerCase()) ||
        dept.includes(searchQuery.value.toLowerCase()) ||
        position.includes(searchQuery.value.toLowerCase()) ||
        reason.includes(searchQuery.value.toLowerCase()))
    );
  });
});
</script>

<template>
  <main>
    <Calendar :wfh-details="approvedWFHDetails" />

    <div class="filter-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search by name, department, position, or reason"
        class="filter-input-search"
      />
      <br />
      <label for="start-date">Start Date: </label>
      <input
        v-model="startDate"
        type="date"
        id="start-date"
        class="filter-input ml-2"
      />

      <label for="end-date">End Date: </label>
      <input
        v-model="endDate"
        type="date"
        id="end-date"
        class="filter-input ml-2"
      />
    </div>

    <div class="table-container">
      <h2>WFH Arrangements</h2>
      <table class="table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Full Name</th>
            <th>Department</th>
            <th>Position</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(wfh, index) in filteredWFHDetails"
            :key="wfh.arrangement_id"
          >
            <td>{{ new Date(wfh.date).toLocaleString() }}</td>
            <td>
              {{ wfh.employee.staff_fname + ' ' + wfh.employee.staff_lname }}
            </td>
            <td>{{ wfh.employee.dept }}</td>
            <td>{{ wfh.employee.position }}</td>
            <td>{{ wfh.reason || 'No Reason Provided' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>

<style scoped>
/* Styling for filter input */
.filter-container {
  margin: 20px 0;
  text-align: center;
}

.filter-input-search {
  padding: 8px;
  margin: 10px;
  width: 50%;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.filter-input {
  padding: 8px;
  margin-right: 10px;
  width: auto;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Styling for the table */
.table-container {
  margin: 20px auto;
  max-width: 90vw;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

.table th {
  background-color: #f4f4f4;
}

.table td {
  background-color: #fff;
}

.table-container h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
