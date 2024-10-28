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
    <div class="review-section" v-if="showReviewSection">
      <h3>Review Your Selection</h3>
      <p><strong>Selected WFH Date and Time:</strong> {{ selectedDate }}</p>
      <p><strong>Timeslot:</strong> {{ wfhtime }}</p>
      <p><strong>Reason:</strong> {{ reason }}</p>
      <p><strong>Request Type:</strong> {{ requestType }}</p>
      <p><strong>Supporting documents:</strong> {{ uploadedFile?.name || 'None' }}</p>
      <p><strong>Recurrence frequency:</strong> {{ recurrenceFrequency || 'N/A' }}</p>
      <p><strong>Recurring arrangement will end on:</strong> {{ recurrenceEndDate || 'N/A' }}</p>
    </div>

    <button type="submit" class="btn btn-primary">Submit WFH Request</button>

    <div class="mt-4">
      <h3>Dates That Are Blocked Off</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Date</th>
            <th>Event Description</th>
            <th>Event ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(description, date) in DateDict" :key="date">
            <td>{{ date }}</td>
            <td>{{ description[0] }}</td>
            <td>{{ description[1] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </form>
</template>

<script>
import { getAllDatesWithEvents, convertFileToUrl } from '@/api/api';

export default {
  name: 'WFHForm',
  props: {
    blockedDays: Array,
    minDate: String,
    maxDate: String,
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
      DateDict: {},
      uploadedFile: null,
      uploadedFileUrl: '',
    };
  },
  async mounted() {
    const apiDateDict = await getAllDatesWithEvents();
    this.DateDict = this.formatDatesToYYYYMMDD(apiDateDict);
  },

  computed: {
    showReviewSection() {
      return (
        this.selectedDate &&
        this.wfhtime &&
        this.reason &&
        this.requestType 
      );
    },
  },

  watch: {
    selectedDate() {
      this.updateInvalidMessage();
    },
    wfhtime() {
      this.updateInvalidMessage();
    },
    reason() {
      this.updateInvalidMessage();
    },
    requestType() {
      this.updateInvalidMessage();
    },
    recurrenceFrequency() {
      this.updateInvalidMessage();
    },
    recurrenceEndDate() {
      this.updateInvalidMessage();
    },
  },

  methods: {
    formatDatesToYYYYMMDD(dateDict) {
      const formattedDict = {};
      for (const [dateString, description] of Object.entries(dateDict)) {
        const date = new Date(dateString);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();

        formattedDict[`${year}-${month}-${day}`] = description;
      }
      return formattedDict;
    },

    updateInvalidMessage() {
      if (!this.selectedDate || !this.wfhtime || !this.reason || !this.requestType) {
        this.invalidMessage = 'Please complete all fields.';
        return;
      }

      const date_obj = new Date(
        `${this.selectedDate}T${this.wfhtime === 'AM' ? '09:00' : '14:00'}`,
      );
      const today = new Date();
      const oneYearFromNow = new Date();
      oneYearFromNow.setFullYear(today.getFullYear() + 1);

      if (date_obj < today || date_obj > oneYearFromNow) {
        this.invalidMessage = 'Invalid WFH date. Please select a valid date.';
        return;
      }

      if (this.blockedDays.includes(this.selectedDate)) {
        this.invalidMessage = 'This day is blocked. Please select another date.';
        return;
      }

      if (this.requestType === 'Recurring') {
        if (!this.recurrenceFrequency || !this.recurrenceEndDate) {
          this.invalidMessage = 'Please complete all recurring request fields.';
          return;
        }
        if (new Date(this.recurrenceEndDate) < date_obj) {
          this.invalidMessage = 'Recurrence end date must be after the start date.';
          return;
        }
      }

      this.invalidMessage = '';
    },

    onFileChange(event) {
      this.uploadedFile = event.target.files[0];
    },

    async handleSubmit() {
      const payload = {
        date: this.selectedDate,
        time: this.wfhtime,
        reason: this.reason,
        requestType: this.requestType,
      };
      if (this.uploadedFile) {
        try {
          const res = await convertFileToUrl(this.uploadedFile);
          payload.fileUrl = res.url;
        } catch (error) {
          console.error('error uploading file : ', error);
          alert('failed to upload file');
          return;
        }
      }

      if (this.requestType === 'Recurring') {
        payload.recurrenceFrequency = this.recurrenceFrequency;
        payload.recurrenceEndDate = this.recurrenceEndDate;
      }

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