<template>
    <div class="calendar-container">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <!-- Header for the Month and Year -->
          <div class="d-flex justify-content-between align-items-center mb-3">
            <button class="btn btn-primary" @click="previousMonth">Previous</button>
            <h3>{{ currentMonth }} {{ currentYear }}</h3>
            <button class="btn btn-primary" @click="nextMonth">Next</button>
          </div>
  
          <!-- Days of the Week -->
          <div class="row text-center bg-light mb-2">
            <div class="col day-header" v-for="day in daysOfWeek" :key="day">{{ day }}</div>
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
              :class="{ 'bg-primary text-white': isToday(day), 'selected-day': isSelectedDay(day) }"
            >
              <div class="day-content">{{ day }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      const today = new Date();
      return {
        selectedDate: today, // stores the currently selected date
        currentYear: today.getFullYear(),
        currentMonthIndex: today.getMonth(),
        daysOfWeek: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      };
    },
    computed: {
      currentMonth() {
        return new Date(this.currentYear, this.currentMonthIndex).toLocaleString(
          'default',
          { month: 'long' }
        );
      },
      daysInMonth() {
        return new Date(
          this.currentYear,
          this.currentMonthIndex + 1,
          0
        ).getDate();
      },
      firstDayOfMonth() {
        return new Date(this.currentYear, this.currentMonthIndex, 1).getDay();
      },
    },
    methods: {
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
          day
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
    },
  };
  </script>
  
  <style scoped>
  /* Calendar Container spans 80% of the screen height and width */
  .calendar-container {
    width: 80vw;
    height: 80vh;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  /* Grid layout for the calendar days */
  .calendar-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr); /* 7 days in a week */
    grid-auto-rows: 1fr; /* Make each row of equal height */
    gap: 10px; /* Space between the day boxes */
    height: 100%; /* Full height for the grid */
  }
  
  /* Day box styling */
  .day-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align the day number to the top */
    background-color: white;
    border: 1px solid #dee2e6;
    padding: 10px; /* Extra space for content inside the box */
    box-sizing: border-box;
    transition: background-color 0.2s ease-in-out;
    min-height: 100px; /* Adjust this based on how much content you plan to add */
  }
  
  /* Day header for weekdays */
  .day-header {
    font-weight: bold;
    padding: 10px;
  }
  
  /* Styling for the day number and content */
  .day-content {
    font-size: 18px;
    margin-bottom: 5px;
  }
  
  /* Highlight selected day */
  .selected-day {
    background-color: #f0ad4e !important;
    color: white;
    font-weight: bold;
  }
  
  /* Highlight today's date */
  .bg-primary {
    background-color: #007bff !important;
    color: white;
  }
  
  /* Add hover effect on day boxes */
  .day-box:hover {
    cursor: pointer;
    background-color: #f8f9fa;
  }
  </style>
  