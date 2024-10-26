<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const arrangements = ref([]);
const empDatas = ref([]);
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

const timeOptions = [
  { value: '1', label: 'AM' },
  { value: '2', label: 'PM' },
  { value: '3', label: 'Whole Day' },
];

// onMounted(() => {
// const storedArrangements = localStorage.getItem('empArrangement');
// if (storedArrangements) {
//     arrangements.value = JSON.parse(storedArrangements);
//     console.log(JSON.parse(storedArrangements));
// }
// const employeedata = localStorage.getItem('employeeData');
// if (employeedata) {
//     empDatas.value = JSON.parse(employeedata);
//     console.log(JSON.parse(employeedata));
// }

// });

onMounted(async () => {
  const employeedata = localStorage.getItem('employeeData');
  if (employeedata) {
    const test = JSON.parse(employeedata);
    const staff_id = test.staff_id;
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_BACKEND_URL}/arrangement/emp/${staff_id}`,
      );
      localStorage.setItem('empArrangement', JSON.stringify(response.data));
      const storedArrangements = localStorage.getItem('empArrangement');
      arrangements.value = JSON.parse(storedArrangements);
    } catch {}
  }
});

const filteredArrangements = computed(() => {
  const filtered = arrangements.value.filter((arrangement) => {
    const matchesStatus =
      selectedStatus.value === '' ||
      arrangement.status.toString() === selectedStatus.value;
    const arrangementDate = new Date(arrangement.date);
    const isAfterStartDate =
      !startDate.value || arrangementDate >= new Date(startDate.value);
    const isBeforeEndDate =
      !endDate.value || arrangementDate <= new Date(endDate.value);

    return matchesStatus && isAfterStartDate && isBeforeEndDate;
  });

  // Sort the filtered arrangements by date descending
  return filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
});

const getStatusLabel = (status) => {
  const statusString = status.toString();
  // Matches the value of status and turns that output into the label you see in the array above
  // For example, if statusString is "1", it will find { value: '1', label: 'Accepted' }.
  const matchingOption = statusOptions.find(
    (option) => option.value === statusString,
  );
  // If match exist, return the label,  otherwise return Something went wrong
  return matchingOption ? matchingOption.label : 'Something went wrong';
};

const getTimeLabel = (time) => {
  const timeString = time.toString();

  const matchingOption = timeOptions.find(
    (option) => option.value === timeString,
  );
  // If match exist, return the label,  otherwise return Something went wrong
  return matchingOption ? matchingOption.label : 'Something went wrong';
};

const cancelArrangement = async (arrangementId) => {
  try {
    const response = await axios.put(
      `${import.meta.env.VITE_BACKEND_URL}/arrangement/cancel/${arrangementId}`,
    );
    if (response.status === 200) {
      // Update the local state to reflect the change (for demo purposes only)
      const arrangement = arrangements.value.find(
        (a) => a.arrangement_id === arrangementId,
      );
      if (arrangement) {
        arrangement.status = 3; // Set status to 'Cancelled/Withdrawn'
      }
    }
  } catch (error) {
    console.error('Error while cancelling arrangement: ', error);
  }
};

function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center mb-4">
      <div class="col-md-4">
        <select class="form-select" v-model="selectedStatus">
          <option
            v-for="option in statusOptions"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <input
          type="date"
          class="form-control"
          v-model="startDate"
          placeholder="Start Date"
        />
      </div>
      <div class="col-md-4">
        <input
          type="date"
          class="form-control"
          v-model="endDate"
          placeholder="End Date"
        />
      </div>
    </div>
    <div class="table-container">
      <h2>Historical Arrangements</h2>
      <table class="table">
        <thead>
          <tr>
            <!-- <th>ID</th> -->
            <!-- <th>Name</th> -->
            <th>Date</th>
            <th>Status</th>
            <th>Time</th>
            <th>Application Reason</th>
            <th>Rejection Reason</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="arrangement in filteredArrangements"
            :key="arrangement.arrangement_id"
          >
            <!-- <td>{{ new Date(arrangement.date).toLocaleString() }}</td> -->
            <!-- <td>{{ arrangement.staff_id }}</td>
                        <td>{{ empDatas.staff_fname + ' ' + empDatas.staff_lname}}</td> -->
            <td>{{ formatDate(arrangement.date) }}</td>
            <td>{{ getStatusLabel(arrangement.status) }}</td>
            <td>{{ getTimeLabel(arrangement.time) }}</td>
            <td>{{ arrangement.reason_staff || 'No Reason Provided' }}</td>
            <td>{{ arrangement.reason_man || 'N/A' }}</td>
            <td>
              <!-- Add Cancel Button for arrangements with status 0 or 1 -->
              <button
                v-if="arrangement.status === 0"
                @click="cancelArrangement(arrangement.arrangement_id)"
                class="btn btn-danger"
              >
                Cancel Arrangement
              </button>
              <button
                v-if="arrangement.status === 1"
                @click="cancelArrangement(arrangement.arrangement_id)"
                class="btn btn-danger"
              >
                Withdraw Arrangement
              </button>
              <!-- Button trigger modal -->
              <!-- <button type="button" v-if="arrangement.status === 1" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#exampleModal">
                                Withdraw Arrangement
                            </button> -->

              <!-- Modal -->
              <!-- <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="exampleModalLabel">Withdrawal Reason</h5>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                    Textbox for input
                                    <textarea v-model="withdrawalReason" class="form-control" rows="3" placeholder="Enter your reason here..."></textarea>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button type="button" class="btn btn-primary">Submit</button>
                                    </div>
                                    </div>
                                </div>
                            </div> -->
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
