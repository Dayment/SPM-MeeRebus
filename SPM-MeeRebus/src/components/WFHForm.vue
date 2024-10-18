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
    <!-- File Upload Section -->
    <div class="mb-3">
      <label for="file-upload" class="form-label"
        >Upload Supporting Document (Optional)</label
      >
      <input
        type="file"
        id="file-upload"
        class="form-control"
        @change="onFileChange"
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

    <div v-if="requestType === 'Recurring'">
      <div class="form-group">
        <label for="recurrence-frequency">Recurrence Frequency:</label>
        <select
          v-model="recurrenceFrequency"
          id="recurrence-frequency"
          class="form-control"
          required
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
        </select>
      </div>

      <div class="form-group">
        <label for="recurrence-end-date">Recurrence End Date:</label>
        <input
          type="date"
          id="recurrence-end-date"
          v-model="recurrenceEndDate"
          class="form-control"
          :min="selectedDate"
          :max="maxDate"
          required
        />
      </div>
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
      <p><strong>Selected WFH Date and Time:</strong> {{ selectedDate }}</p>
      <p><strong>Timeslot:</strong> {{ wfhtime }}</p>
      <p><strong>Reason:</strong> {{ reason }}</p>
      <p><strong>Request Type:</strong> {{ requestType }}</p>
      <p><strong>Supporting documents:</strong> {{ uploadedFile.name }}</p>
      <p><strong>Reccurence frequency:</strong> {{ recurrenceFrequency }}</p>
      <p>
        <strong>Reccuring arrangement will end on:</strong>
        {{ recurrenceEndDate }}
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
      invalidMessage: '',
      reason: '',
      requestType: '',
      recurrenceFrequency: '',
      recurrenceEndDate: '',
      uploadedFile: null,
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

      const date_obj = new Date(
        `${this.selectedDate}T${this.wfhtime === 'AM' ? '09:00' : '14:00'}`,
      );
      const today = new Date();
      const oneYearFromNow = new Date();
      oneYearFromNow.setFullYear(today.getFullYear() + 1);

      if (date_obj < today || date_obj > oneYearFromNow) {
        return 'Invalid WFH date. Please select a valid date.';
      }

      if (this.blockedDays.includes(this.selectedDate)) {
        return 'This day is blocked. Please select another date.';
      }
      if (this.requestType === 'recurring') {
        if (!this.recurrenceFrequency || !this.recurrenceEndDate) {
          return 'Please complete all recurring request fields.';
        }
        if (new Date(this.recurrenceEndDate) < date_obj) {
          return 'Recurrence end date must be after the start date.';
        }
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

      if (this.requestType == 'Recurring') {
        payload.recurrenceFrequency = this.recurrenceFrequency;
        payload.recurrenceEndDate = this.recurrenceEndDate;
      }

      this.$emit('submitRequest', payload);
    },
    onFileChange(event) {
      this.uploadedFile = event.target.files[0];
      console.log(this.uploadedFile);
      //turn into link here
    },
  },
};
</script>

<style scoped>
.review-section {
  margin: 20px 0;
}
</style>
