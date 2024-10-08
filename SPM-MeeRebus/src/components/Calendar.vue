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

          <button class="btn btn-primary" @click="nextMonth">Next</button>
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
              // 'arranged-day': isArrangedDay(day) !== null
            }"
            :style="{backgroundColor: isToday(day) ? 'white' : ''}
            "
          > 
          <!-- Insert arrangement details here. Reason, etc -->
          <!-- <div v-if="isArrangedDayObj(day) !== null">
            <p><strong>Staff ID: </strong> {{ isArrangedDayObj(day).staff_id }}</p>
            <p><strong>Reason:</strong> {{ isArrangedDayObj(day).reason }}</p>
            <p><strong>Status:</strong> {{ isArrangedDayObj(day).status }}</p>
          </div> -->
          <!-- :style="{ backgroundColor: getArrangementColor(day) }" OLD STYLE -->

            <div class="day-content">{{ day }}</div>

            <div v-if="getWFHForDay(day)" class="wfh-task">
              <span class="task-title">
                {{ day }}
                ({{ this.formatWFHTime(getWFHForDay(day).time) }})
                {{ getWFHForDay(day)?.employee?.staff_fname || "You" }} :
                {{ getWFHForDay(day).reason || 'No Reason' }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    wfhDetails: {
      type: Array,
      default: () => [],
    },
  },
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
    this.checkArrangementData(); // Check for arrangements on mount
  },

  methods: {
    async checkArrangementData() {
      const storedArrangements = localStorage.getItem('empArrangement');
      if (storedArrangements) {
        this.arrangements = JSON.parse(storedArrangements);
      } else {
        // await this.fetchArrangementData();
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
    parseDate(dateString) {
      return new Date(dateString); // Converts ISO string to Date object
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
        // const response = await axios.get('http://127.0.0.1:5000/arrangement');
        // this.arrangements = response.data;
        localStorage.getItem('empArrangement');
        checkHR = localStorage.getItem('empData');
        if (checkHR.dept == 'HR') {
          const response = await axios.get('http://127.0.0.1:5000/arrangement');
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

    // fetch the WFH details for a specific day
    getWFHForDay(day) {
      const dateString = new Date(
        this.currentYear,
        this.currentMonthIndex,
        day + 1,
      ) //need to increment here due to conversion to iso string decrementing date by 1
        .toISOString()
        .split('T')[0];
      return this.wfhDetails.find(
        (wfh) => new Date(wfh.date).toISOString().split('T')[0] === dateString,
      );
    },

    formatWFHTime(time) {
      switch (time) {
        case 1:
          return 'AM';
        case 2:
          return 'PM';
        case 3:
          return 'All Day';
        default:
          return '';
      }
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

/* Styling for WFH task */
.wfh-task {
  background-color: #4a90e2;
  color: white;
  padding: 5px;
  border-radius: 4px;
  margin-top: 5px;
  font-size: 12px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
}

.task-time {
  margin-right: 5px;
}
</style>
