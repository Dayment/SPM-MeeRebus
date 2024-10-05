<template>
  <form @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="wfh-time">WFH time:</label>
      <select v-model="wfhtime" id="wfh-time" class="form-control" required>
        <option value="AM">AM</option>
        <option value="PM">PM</option>
        <option value="Full Day">Full Day</option>
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
        required
      />
    </div>

    <!-- Reason Input -->
    <div class="form-group">
      <label for="reason">Reason for WFH:</label>
      <input
        type="text"
        id="reason"
        v-model="reason"
        class="form-control"
        placeholder="Enter the reason for WFH"
        required
      />
    </div>

    <!-- Request Type Dropdown -->
    <div class="form-group">
      <label for="request-type">Request Type:</label>
      <select
        v-model="requestType"
        id="request-type"
        class="form-control"
        required
      >
        <option value="Adhoc">Adhoc</option>
        <option value="Recurring">Recurring</option>
      </select>
    </div>

    <div v-if="invalidMessage" class="alert alert-danger">
      {{ invalidMessage }}
    </div>

    <!-- Review Section -->
    <div
      class="review-section"
      v-if="selectedDate && wfhtime && reason && requestType && !invalidMessage"
    >
      <h3>Review Your Selection</h3>
      <p>
        <strong>Selected WFH Date and Time:</strong> {{ selectedDate }}
        {{ wfhtime }}
      </p>
      <p><strong>Reason:</strong> {{ reason }}</p>
      <p><strong>Request Type:</strong> {{ requestType }}</p>
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
      invalidMessage: '',
      reason: '',
      requestType: '',
    };
  },
  computed: {
    invalidMessage() {
      if (
        !this.selectedDate ||
        !this.wfhtime ||
        !this.reason ||
        !this.requestType
      ) {
        return 'Please complete all fields.';
      }

      const selectedDateObj = new Date(
        `${this.selectedDate}T${this.wfhtime === 'AM' ? '09:00' : '14:00'}`,
      );
      const today = new Date();
      const oneYearFromNow = new Date();
      oneYearFromNow.setFullYear(today.getFullYear() + 1);

      if (selectedDateObj < today || selectedDateObj > oneYearFromNow) {
        return 'Invalid WFH date. Please select a valid date.';
      }

      if (this.blockedDays.includes(this.selectedDate)) {
        return 'This day is blocked. Please select another date.';
      }

      return ''; 
    },

    isFormValid() {
      return !this.invalidMessage;
    },
  },
  methods: {
    handleSubmit() {
      const payload = {
        date: this.selectedDate,
        time: this.wfhtime, // AM, PM or Full Day
        reason: this.reason,
        requestType: this.requestType, // ad-hoc or recurring
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
