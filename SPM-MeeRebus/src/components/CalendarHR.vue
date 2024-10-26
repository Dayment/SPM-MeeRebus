<template>
  <div class="calendar-container">
    <div class="row justify-content-center">
      <div class="col-md-12">
        <!-- Header for the Month and Year with Dropdowns -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <button class="btn btn-primary" @click="previousMonth">
            Previous
          </button>

          <!-- Month Dropdown -->
          <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              id="dropdownMonth"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ currentMonth }}
            </button>
            <ul
              class="dropdown-menu scrollable-dropdown"
              aria-labelledby="dropdownMonth"
            >
              <li v-for="(month, index) in months" :key="month">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="selectMonth(index)"
                  data-bs-dismiss="dropdown"
                >
                  {{ month }}
                </a>
              </li>
            </ul>
          </div>

          <!-- Year Dropdown -->
          <div class="dropdown">
            <button
              class="btn btn-secondary dropdown-toggle"
              type="button"
              id="dropdownYear"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              {{ currentYear }}
            </button>
            <ul
              class="dropdown-menu scrollable-dropdown"
              aria-labelledby="dropdownYear"
            >
              <li v-for="year in years" :key="year">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="selectYear(year)"
                  data-bs-dismiss="dropdown"
                >
                  {{ year }}
                </a>
              </li>
            </ul>
          </div>
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
            <ul
              class="dropdown-menu scrollable-dropdown"
              aria-labelledby="dropdownTeam"
            >
              <li v-for="team in teams" :key="team">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="selectTeam(team)"
                  data-bs-dismiss="dropdown"
                >
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
            <ul
              class="dropdown-menu scrollable-dropdown"
              aria-labelledby="dropdownsyssTeam"
            >
              <li v-for="syssTeam in syssTeams" :key="syssTeam">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="selectsyssTeam(syssTeam)"
                  data-bs-dismiss="dropdown"
                >
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
            <ul
              class="dropdown-menu scrollable-dropdown"
              aria-labelledby="dropdownengTeam"
            >
              <li v-for="engTeam in engTeams" :key="engTeam">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="selectengTeam(engTeam)"
                  data-bs-dismiss="dropdown"
                >
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
            <ul
              class="dropdown-menu scrollable-dropdown"
              aria-labelledby="dropdownhrTeam"
            >
              <li v-for="hrTeam in hrTeams" :key="hrTeam">
                <a
                  class="dropdown-item"
                  href="#"
                  @click="selectengTeam(hrTeam)"
                  data-bs-dismiss="dropdown"
                >
                  {{ hrTeam }}
                </a>
              </li>
            </ul>
          </div>
          <button class="btn btn-primary" @click="nextMonth">Next</button>
        </div>
      </div>

      <!-- Days of the Week -->
      <div class="row text-center bg-light mb-2">
        <div class="col day-header" v-for="day in daysOfWeek" :key="day">
          {{ day }}
        </div>
      </div>

      <!-- Days of the Month -->
      <div class="calendar-grid">
        <!-- Empty cells for previous month's days -->
        <div
          class="day-box"
          v-for="n in firstDayOfMonth"
          :key="'empty-' + n"
        ></div>

        <!-- Render days of the current month -->
        <div
          class="day-box border"
          v-for="day in daysInMonth"
          :key="day"
          @click="selectDate(day)"
          :class="{
            'selected-day': isSelectedDay(day),
            'today-border': isToday(day),
            'arranged-day': isArrangedDay(day) !== null,
          }"
          :style="{ backgroundColor: getArrangementColor(day) }"
        >
          <!-- Insert arrangement details here. Reason, etc -->
          <div v-if="isArrangedDayObj(day) !== null">
            <p>
              <strong>Staff ID: </strong> {{ isArrangedDayObj(day).staff_id }}
            </p>
            <p><strong>Reason:</strong> {{ isArrangedDayObj(day).reason }}</p>
            <p><strong>Status:</strong> {{ isArrangedDayObj(day).status }}</p>
          </div>
          <!-- :style="{backgroundColor: isToday(day) ? 'white' : ''}" OLD STYLE -->
          <div class="day-content">{{ day }}</div>
        </div>
      </div>
    </div>
  </div>

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

<script>
import axios from 'axios';
export default {
  data() {
    const today = new Date();
    return {
      selectedDate: today,
      currentYear: today.getFullYear(),
      currentMonthIndex: today.getMonth(),
      daysOfWeek: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
      ],
      months: [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
      ],
      years: this.generateYears(),
      arrangements: [],
      teams: [
        'Sales',
        'Consultancy',
        'System Solutioning',
        'Engineering',
        'HR',
        'Finance',
        'IT',
      ],
      selectedTeam: 'HR',
      syssTeams: ['Developers', 'Support Team'],
      selectedsyssTeam: 'Developers',
      engTeams: [
        'Senior Engineers',
        'Junior Engineers',
        'Call Centre',
        'Operation Planning Team',
      ],
      selectedengTeam: 'Senior Engineers',
      hrTeams: ['HR Team', 'L&D team', 'Admin Team'],
      selectedhrTeam: 'HR Team',
    };
  },
  computed: {
    currentMonth() {
      return this.months[this.currentMonthIndex];
    },
    daysInMonth() {
      return new Date(
        this.currentYear,
        this.currentMonthIndex + 1,
        0,
      ).getDate();
    },
    firstDayOfMonth() {
      return new Date(this.currentYear, this.currentMonthIndex, 1).getDay();
    },
  },

  mounted() {
    // this.checkArrangementData(); // Check for arrangements on mount
    const staff_id = localStorage.getItem('employeeId');
    // this.checkTeamArrangementData(staff_id) // Check for team arrangemetns on mount
    this.checkCompanyArrangementData();
  },

  methods: {
    async checkArrangementData() {
      const storedArrangements = localStorage.getItem('empArrangement');
      if (storedArrangements) {
        // this.arrangements = JSON.parse(storedArrangements);
      } else {
        // await this.fetchArrangementData();
      }
    },
    async checkCompanyArrangementData() {
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/arrangement`,
        );
        localStorage.setItem(
          'companyArrangements',
          JSON.stringify(response.data),
        );
        this.arrangements = response.data;
        console.log(this.arrangements);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    isArrangedDay(day) {
      // Creating the string for the date to do checking with the arrangement date
      const formattedDate = `${this.currentYear}-${String(
        this.currentMonthIndex + 1,
      ).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

      const arrangement = this.arrangements.find((arrangement) => {
        const arrangementDate = new Date(arrangement.date);
        if (!isNaN(arrangementDate.getTime())) {
          const arrangementISO = arrangementDate.toISOString().split('T')[0];
          return arrangementISO === formattedDate; // Check for matching date
        }
        return false; // Skip invalid dates
      });
      // Return status or null if no arrangement
      return arrangement ? arrangement.status : null;
    },
    // Using this for conditional rendering in the V-if. Might refactor with above code if have time
    isArrangedDayObj(day) {
      // Creating the string for the date to do checking with the arrangement date
      const formattedDate = `${this.currentYear}-${String(
        this.currentMonthIndex + 1,
      ).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

      const arrangement = this.arrangements.find((arrangement) => {
        const arrangementDate = new Date(arrangement.date);
        if (!isNaN(arrangementDate.getTime())) {
          const arrangementISO = arrangementDate.toISOString().split('T')[0];
          return arrangementISO === formattedDate; // Check for matching date
        }
        return false; // Skip invalid dates
      });
      // Return status or null if no arrangement
      return arrangement || null;
    },

    // Set the CSS colour depending on arrangement status
    getArrangementColor(day) {
      const status = this.isArrangedDay(day);

      if (status === 1) {
        return 'lightgreen'; // Accepted arrangements
      } else if (status === 0) {
        return 'orange'; // Pending arrangements
      } else if (status === 2) {
        return 'red'; // Denied arrangements
      }

      return ''; // Default background color (no arrangements)
    },
    async fetchArrangementData() {
      try {
        // const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/arrangement`);
        // this.arrangements = response.data;
        localStorage.getItem('empArrangement');
        checkHR = localStorage.getItem('empData');
        if (
          checkHR.dept == 'HR' ||
          checkHR.position == 'MD' ||
          checkHR.position == 'Director'
        ) {
          const response = await axios.get(
            `${import.meta.env.VITE_BACKEND_URL}/arrangement`,
          );
          localStorage.setItem('arrangement', JSON.stringify(response.data));
        }
      } catch (error) {
        console.error('Error fetching arrangement data:', error);
      }
    },

    previousMonth() {
      if (this.currentMonthIndex === 0) {
        this.currentMonthIndex = 11;
        this.currentYear--;
      } else {
        this.currentMonthIndex--;
      }
    },
    nextMonth() {
      if (this.currentMonthIndex === 11) {
        this.currentMonthIndex = 0;
        this.currentYear++;
      } else {
        this.currentMonthIndex++;
      }
    },
    selectDate(day) {
      this.selectedDate = new Date(
        this.currentYear,
        this.currentMonthIndex,
        day,
      );
    },
    isToday(day) {
      const today = new Date();
      return (
        today.getFullYear() === this.currentYear &&
        today.getMonth() === this.currentMonthIndex &&
        today.getDate() === day
      );
    },
    isSelectedDay(day) {
      return (
        this.selectedDate.getFullYear() === this.currentYear &&
        this.selectedDate.getMonth() === this.currentMonthIndex &&
        this.selectedDate.getDate() === day
      );
    },
    selectMonth(index) {
      this.currentMonthIndex = index;
    },
    selectYear(year) {
      this.currentYear = year;
    },
    generateYears() {
      const currentYear = new Date().getFullYear();
      const years = [];
      for (let i = currentYear - 10; i <= currentYear + 5; i++) {
        years.push(i);
      }
      return years;
    },
    selectTeam(team) {
      this.selectedTeam = team;
      if (team !== 'System Solutioning') {
        this.selectedsyssTeam = 'Developers'; // Reset sys team selection when not IT
      } else if (team !== 'Engineering') {
        this.selectedengTeam = 'Senior Engineers'; // Reset eng team selection when not IT
      } else if (team !== 'HR') {
        this.selectedhrTeam = 'HR Team'; // Reset hr team selection when not IT
      }
    },
    selectsyssTeam(syssTeam) {
      this.selectedsyssTeam = syssTeam;
    },
    selectengTeam(engTeam) {
      this.selectedengTeam = engTeam;
    },
    selectengTeam(hrTeam) {
      this.selectedhrTeam = hrTeam;
    },
  },
};
</script>

<style scoped>
/* Calendar Container spans 100% of the width */
.calendar-container {
  width: 80vw;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Scrollable dropdown menu */
.scrollable-dropdown {
  max-height: 200px; /* Adjust the height as necessary */
  overflow-y: auto;
}

/* Grid layout for the calendar days */
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr); /* 7 days in a week */
  grid-auto-rows: auto; /* Allow rows to adjust based on content */
  padding-bottom: 20px; /* Add padding to the bottom */
}

/* Day box styling */
.day-box {
  display: flex;
  flex-direction: column;
  justify-content: flex-end; /* Align content to the bottom */
  align-items: flex-end; /* Align day number to the right */
  background-color: white;
  border: 1px solid #dee2e6;
  padding: 5px; /* Extra space for content inside the box */
  box-sizing: border-box;
  transition: background-color 0.2s ease-in-out;
  min-height: 150px; /* Adjust this based on how much content you plan to add */
}

/* Colour for approved WFH */
.arranged-day {
  background-color: lightgreen;
  border: 2px solid darkgreen;
}

/* Highlight today's date with a border */
.today-border {
  border: 2px solid #007bff !important; /* Change this color as needed */
}

/* Day header for weekdays */
.day-header {
  font-weight: bold;
  padding: 10px;
}

/* Styling for the day number and content */
.day-content {
  font-size: 14px; /* Decrease font size */
  margin: 0; /* Remove margin */
}

/* Highlight selected day */
.selected-day {
  font-weight: bold;
}

/* Add hover effect on day boxes */
.day-box:hover {
  cursor: pointer;
  background-color: #f8f9fa;
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
