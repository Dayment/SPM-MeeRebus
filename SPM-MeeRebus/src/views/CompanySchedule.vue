<script setup>
import { ref, computed, onMounted } from 'vue'; 
import { useRouter } from 'vue-router';
import { getAllEmployee, getTeamApprovedArrangement, getDeptApprovedArrangement2 } from '../api/api';
import Calendar from '../components/Calendar.vue';  
import axios from 'axios';

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
      // const wfhDetails = await getAllApprovedArrangement(empId);
      const wfhDetails = await getDeptApprovedArrangement2()

      approvedWFHDetails.value = wfhDetails;

      console.log('WFH Details:', wfhDetails);
    } catch (error) {
      console.error(error);
    }
  }
});

const teams = ref(['Sales', 'Consultancy', 'System Solutioning', 'Engineering', 'HR', 'Finance', 'IT']);
const selectedTeam = ref('HR');
const syssTeams = ref(['Developers', 'Support Team']);
const selectedsyssTeam = ref('Developers');
const engTeams = ref(['Senior Engineers', 'Junior Engineers', 'Call Centre', 'Operation Planning Team']);
const selectedengTeam = ref('Senior Engineers');
const hrTeams = ref(['HR Team', 'L&D team', 'Admin Team']);
const selectedhrTeam = ref('HR Team');

const selectTeam = (team) => {
  selectedTeam.value = team;
  if (team !== 'System Solutioning') {
    selectedsyssTeam.value = 'Developers'; // Reset sys team selection when not IT
  }
  if (team !== 'Engineering') {
    selectedengTeam.value = 'Senior Engineers'; // Reset eng team selection when not IT
  }
  if (team !== 'HR') {
    selectedhrTeam.value = 'HR Team'; // Reset hr team selection when not IT
  }
};

const selectsyssTeam = (syssTeam) => {
  selectedsyssTeam.value = syssTeam;
};

const selectengTeam = (engTeam) => {
  selectedengTeam.value = engTeam;
};

const selecthrTeam = (hrTeam) => {
  selectedhrTeam.value = hrTeam;
};

const filteredWFHDetails = computed(() => {
  return approvedWFHDetails.value.filter((wfh) => {
    const fullName = `${wfh.employee.staff_fname} ${wfh.employee.staff_lname}`.toLowerCase();
    const dept = wfh.employee.dept.toLowerCase();
    const position = wfh.employee.position.toLowerCase();
    const reason = (wfh.reason || 'No Reason Provided').toLowerCase();
    const wfhDate = new Date(wfh.date);

    const isWithinDateRange =
      (!startDate.value || new Date(startDate.value) <= wfhDate) &&
      (!endDate.value || wfhDate <= new Date(endDate.value));

    const matchesTeamAndSubTeam = () => {
      if (selectedTeam.value === 'System Solutioning') {
        return dept.includes('system solutioning') && position.includes(selectedsyssTeam.value.toLowerCase());
      } else if (selectedTeam.value === 'Engineering') {
        return dept.includes('engineering') && position.includes(selectedengTeam.value.toLowerCase());
      } else if (selectedTeam.value === 'HR') {
        return dept.includes('hr') && position.includes(selectedhrTeam.value.toLowerCase());
      } else {
        return dept.includes(selectedTeam.value.toLowerCase());
      }
    };

    return (
      isWithinDateRange &&
      matchesTeamAndSubTeam() &&
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
    <!-- Team Dropdown -->
    <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              id="dropdownTeam"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              >
                {{ selectedTeam }}
              </button>
              <ul class="dropdown-menu scrollable-dropdown" aria-labelledby="dropdownTeam">
                <li v-for="team in teams" :key="team">
                  <a class="dropdown-item" 
                  href="#" @click="selectTeam(team)" data-bs-dismiss="dropdown">
          {{ team }}
        </a>
      </li>
    </ul>
  </div>
  <!-- New Conditional Dropdown for systems solutioning Team -->
  <div v-if="selectedTeam === 'System Solutioning'" class="dropdown">
      <button
        class="btn btn-secondary dropdown-toggle"
        type="button"
        id="dropdownsyssTeam"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ selectedsyssTeam }}
      </button>
      <ul class="dropdown-menu scrollable-dropdown" aria-labelledby="dropdownsyssTeam">
        <li v-for="syssTeam in syssTeams" :key="syssTeam">
          <a class="dropdown-item" 
            href="#" 
            @click="selectsyssTeam(syssTeam)" 
            data-bs-dismiss="dropdown">
            {{ syssTeam }}
          </a>
        </li>
      </ul>
    </div>

    <!-- New Conditional Dropdown for engineering Team -->
  <div v-else-if="selectedTeam === 'Engineering'" class="dropdown">
      <button
        class="btn btn-secondary dropdown-toggle"
        type="button"
        id="dropdownengTeam"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ selectedengTeam }}
      </button>
      <ul class="dropdown-menu scrollable-dropdown" aria-labelledby="dropdownengTeam">
        <li v-for="engTeam in engTeams" :key="engTeam">
          <a class="dropdown-item" 
            href="#" 
            @click="selectengTeam(engTeam)" 
            data-bs-dismiss="dropdown">
            {{ engTeam }}
          </a>
        </li>
      </ul>
    </div>

    <!-- New Conditional Dropdown for HR Team -->
  <div v-else-if="selectedTeam === 'HR'" class="dropdown">
      <button
        class="btn btn-secondary dropdown-toggle"
        type="button"
        id="dropdownhrTeam"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        {{ selectedhrTeam }}
      </button>
      <ul class="dropdown-menu scrollable-dropdown" aria-labelledby="dropdownhrTeam">
        <li v-for="hrTeam in hrTeams" :key="hrTeam">
          <a class="dropdown-item" 
            href="#" 
            @click="selecthrTeam(hrTeam)" 
            data-bs-dismiss="dropdown">
            {{ hrTeam }}
          </a>
        </li>
      </ul>
    </div>
    <Calendar :wfh-details="filteredWFHDetails" />
    
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

.dropdown{
  text-align: center;
  align-items: center;
}

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
