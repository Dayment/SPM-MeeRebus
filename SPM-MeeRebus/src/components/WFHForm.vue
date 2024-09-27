<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="wfh-type">WFH Type:</label>
      <select v-model="wfhType" id="wfh-type" class="form-control" required>
        <option value="regular">Regular</option>
        <option value="ad-hoc">Ad-hoc</option>
      </select>
    </div>

    <!-- Frequency Selector for Regular WFH -->
    <div v-if="wfhType === 'regular'" class="form-group">
      <label for="frequency">Frequency:</label>
      <select v-model="frequency" id="frequency" class="form-control">
        <option value="weekly">Weekly</option>
        <option value="fortnightly">Fortnightly</option>
      </select>
    </div>

    <!-- Date Selector -->
    <div class="form-group">
      <label for="days">Select WFH Date:</label>
      <input
        type="date"
        id="days"
        v-model="selectedDate"
        class="form-control"
        :min="minDate"
        :max="maxDate"
        @change="validateDate"
        required
      />
    </div>

    <!-- Time Selector -->
    <div class="form-group">
      <label for="time">Select Time:</label>
      <input
        type="time"
        id="time"
        v-model="selectedTime"
        class="form-control"
        required
        @change="validateDate"
      />
    </div>

    <div v-if="invalidDateMessage" class="alert alert-danger">
      {{ invalidDateMessage }}
    </div>

    <!-- Review Section -->
    <div
      class="review-section"
      v-if="selectedDate && selectedTime && !invalidDateMessage"
    >
      <h3>Review Your Selection</h3>
      <p>
        <strong>Selected WFH Date and Time:</strong> {{ selectedDate }}
        {{ selectedTime }}
      </p>
      <p>
        <strong>Type:</strong>
        {{ wfhType === 'regular' ? 'Regular' : 'Ad-hoc' }}
      </p>
      <p v-if="wfhType === 'regular'">
        <strong>Frequency:</strong> {{ frequency }}
      </p>
    </div>

    <button
      type="submit"
      class="btn btn-primary"
    >
      Submit WFH Request
    </button>
  </form>
</template>

<script>
export default {
  name: 'WFHForm',
  props: {
    blockedDays: {
      type: Array,
      required: true,
    },
    minDate: {
      type: String,
      required: true,
    },
    maxDate: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      wfhType: 'regular',
      frequency: 'weekly',
      selectedDate: '',
      selectedTime: '',
      invalidDateMessage: '',
    };
  },
  methods: {
    validateDate() {
      if (!this.selectedDate || !this.selectedTime) {
        this.invalidDateMessage = 'Please select both a date and time.';
        return;
      }

      const selectedDateObj = new Date(
        `${this.selectedDate}T${this.selectedTime}`,
      );
      const today = new Date();
      const oneYearFromNow = new Date();
      oneYearFromNow.setFullYear(today.getFullYear() + 1);

      if (selectedDateObj < today || selectedDateObj > oneYearFromNow) {
        this.invalidDateMessage =
          'Invalid WFH date. Please select a valid date.';
      } else if (this.blockedDays.includes(this.selectedDate)) {
        this.invalidDateMessage =
          'This day is blocked. Please select another date.';
      } else {
        this.invalidDateMessage = '';
      }
    },

    handleSubmit() {
      const combinedDateTime = `${this.selectedDate} ${this.selectedTime}:00`; // Combine date and time
      const payload = {
        date: combinedDateTime, // Format: 'YYYY-MM-DD HH:MM:SS'
        type: this.wfhType,
        frequency: this.wfhType === 'regular' ? this.frequency : null,
      };
      this.$emit('submitRequest', payload);
    },
  },
};
</script>

<style scoped>
.review-section {
  margin: 20px 0;
}
</style>
