<script setup>
import { ref, computed, onMounted } from 'vue';

const arrangements = ref([]);
const selectedStatus = ref('');
const startDate = ref('');
const endDate = ref('');

const statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: '0', label: 'Pending' },
    { value: '1', label: 'Accepted' },
    { value: '2', label: 'Rejected' },
    { value: '3', label: 'Cancelled/Withdrawn' },
];

onMounted(() => {
    const storedArrangements = localStorage.getItem('empArrangement');
    if (storedArrangements) {
        arrangements.value = JSON.parse(storedArrangements);
    }
});

const filteredArrangements = computed(() => {
    return arrangements.value.filter(arrangement => {
        // Check if status is selected so filter by pending, accepted, etc
        // selectedStatus.value === '' just means no filter 
        const matchesStatus = selectedStatus.value === '' || arrangement.status.toString() === selectedStatus.value;
        const arrangementDate = new Date(arrangement.date);
        // Filter for dates, !startDate.value means if no date selected in dropdown
        const isAfterStartDate = !startDate.value || arrangementDate >= new Date(startDate.value);
        const isBeforeEndDate = !endDate.value || arrangementDate <= new Date(endDate.value);
        
        // Returns arrangement if it matches the status we are filtering by and if date is within the filter
        return matchesStatus && isAfterStartDate && isBeforeEndDate;
    });
}); 

const getStatusLabel = (status) => {
    const statusString = status.toString();

    // Takes in a status selected from the dropdown, then use .find to see if exists in statusOptions arr
    const matchingOption = statusOptions.find(option => option.value === statusString);

    if (matchingOption) {
        return matchingOption.label;
    }else{
        return "Something went wrong"
    }
};
</script>

<template>
    <div class="container mt-5">
        <div class="row justify-content-center mb-4">
        <div class="col-md-4">
            <select class="form-select" v-model="selectedStatus">
            <option v-for="option in statusOptions" :key="option.value" :value="option.value">
                {{ option.label }}
            </option>
            </select>
        </div>
        <div class="col-md-4">
            <input type="date" class="form-control" v-model="startDate" placeholder="Start Date">
        </div>
        <div class="col-md-4">
            <input type="date" class="form-control" v-model="endDate" placeholder="End Date">
        </div>
        </div>
        <div class="table-container">
        <h2>Historical Arrangements</h2>
        <table class="table">
            <thead>
            <tr>
                <th>Date</th>
                <th>Status</th>
                <th>Application Reason</th>
                <th>Rejection Reason</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="arrangement in filteredArrangements" :key="arrangement.arrangement_id">
                <td>{{ new Date(arrangement.date).toLocaleString() }}</td>
                <td>{{ getStatusLabel(arrangement.status) }}</td>
                <td>{{ arrangement.reason_staff || 'No Reason Provided' }}</td>
                <td>{{ arrangement.reason_man || 'N/A' }}</td>
            </tr>
            </tbody>
        </table>
        </div>
    </div>
</template>