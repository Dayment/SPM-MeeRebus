<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="wfh-time">WFH time:</label>
      <select v-model="wfhtime" id="wfh-time" class="form-control" required>
        <option value="1">AM</option>
        <option value="2">PM</option>
        <option value="3">All Day</option>
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
        <strong>time:</strong>
        {{ wfhtime === 'AM' ? 'PM' : 'Full day' }}
      </p>
      <p v-if="wfhtime === 'regular'">
        <strong>Frequency:</strong> {{ frequency }}
      </p>
    </div>

    <button type="submit" class="btn btn-primary">Submit WFH Request</button>
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
      wfhtime: '',

      selectedDate: '',
      invalidDateMessage: '',
    };
  },
  methods: {
    validateDate() {
      if (!this.selectedDate || !this.wfhtime) {
        this.invalidDateMessage = 'Please select both a date and time.';
        return;
      }
      (this.selectedTime == this.wfhtime) == 'AM' ? '09:00' : '14:00';

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
      // const combinedDateTime = `${this.selectedDate} ${this.selectedTime}:00`; // Combine date and time
      const payload = {
        date: this.selectedDate, // Format: 'YYYY-MM-DD HH:MM:SS'
        time: this.wfhtime,
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
