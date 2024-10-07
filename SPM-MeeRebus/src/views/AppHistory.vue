<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

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
        const matchesStatus = selectedStatus.value === '' || arrangement.status.toString() === selectedStatus.value;
        const arrangementDate = new Date(arrangement.date);
        const isAfterStartDate = !startDate.value || arrangementDate >= new Date(startDate.value);
        const isBeforeEndDate = !endDate.value || arrangementDate <= new Date(endDate.value);
        
        return matchesStatus && isAfterStartDate && isBeforeEndDate;
    });
});

const getStatusLabel = (status) => {
    const statusString = status.toString();
    const matchingOption = statusOptions.find(option => option.value === statusString);
    return matchingOption ? matchingOption.label : "Something went wrong";
};

const cancelArrangement = async (arrangementId) => {
    try {
        const response = await axios.put(`http://localhost:5000/arrangement/cancel/${arrangementId}`);
        if (response.status === 200) {
            // Update the local state to reflect the change (for demo purposes only)
            const arrangement = arrangements.value.find(a => a.arrangement_id === arrangementId);
            if (arrangement) {
                arrangement.status = 3; // Set status to 'Cancelled/Withdrawn'
            }
        }
    } catch (error) {
        console.error("Error while cancelling arrangement: ", error);
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
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="arrangement in filteredArrangements" :key="arrangement.arrangement_id">
                        <td>{{ new Date(arrangement.date).toLocaleString() }}</td>
                        <td>{{ getStatusLabel(arrangement.status) }}</td>
                        <td>{{ arrangement.reason_staff || 'No Reason Provided' }}</td>
                        <td>{{ arrangement.reason_man || 'N/A' }}</td>
                        <td>
                            <!-- Add Cancel Button for arrangements with status 0 or 1 -->
                            <button v-if="arrangement.status === 0 || arrangement.status === 1" @click="cancelArrangement(arrangement.arrangement_id)" class="btn btn-danger">
                                Cancel Arrangement
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
