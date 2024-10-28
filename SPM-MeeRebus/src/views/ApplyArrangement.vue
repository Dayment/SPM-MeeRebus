<template>
  <div class="apply-arrangement">
    <h2>Apply for WFH Arrangement</h2>
    <br />

    <!-- Ad-Hoc Requests Info -->
    <!-- <RequestInfo :remainingRequests="remainingAdHocRequests" /> -->

    <WFHForm
      :blockedDays="blockedDays"
      :minDate="minDate"
      :maxDate="maxDate"
      @submitRequest="submitWFHRequest"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import RequestInfo from '../components/RequestInfo.vue';
import WFHForm from '../components/WFHForm.vue';
import { createWFHRequest, getExistingEvents } from '../api/api';

export default {
  name: 'ApplyArrangement',
  components: {
    RequestInfo,
    WFHForm,
  },
  data() {
    return {
      remainingAdHocRequests: 0,
      //min and max date to show error message
      minDate: '',
      maxDate: '',
      eventlist: {},
      blockedDays: [],
      updatedEventList: [],
      staff_id: localStorage.getItem('employeeId') || null, //consider using global user context object
    };
  },
  methods: {
    async submitWFHRequest(payload) {
      try {
        payload.staff_id = this.staff_id;

        const date = payload.date; // Assuming payload.date is already in 'yyyy-mm-dd' format
        this.eventObj = await getExistingEvents(); // Get list of events
        // Format the eventObj keys (which are date strings) to 'yyyy-mm-dd'
        this.updatedEventObj = Object.fromEntries(
          Object.entries(this.eventObj).map(([dateString, data]) => {
            const dateObj = new Date(dateString); // Convert the key (date) to Date object
            const formattedDate = `${dateObj.getFullYear()}-${String(
              dateObj.getMonth() + 1,
            ).padStart(2, '0')}-${String(dateObj.getDate()).padStart(2, '0')}`; // Format the date

            return [formattedDate, data]; // Return the formatted date and the original data
          }),
        );

        // Now extract the keys (formatted dates) to check for conflicts
        this.updatedEventList = Object.keys(this.updatedEventObj); // Extract all the keys (formatted dates)

        // Check if the selected date is already in the formatted event list

        // staff_id enters as a string
        // console.log(this.staff_id);
        // console.log(typeof(this.staff_id));
        if (this.updatedEventList.includes(date)) {
          alert(
            'This date already exists in the events list. Please choose another date.',
          );
        } else if(this.staff_id == "130002"){
            await createWFHRequest(payload);
            alert('WFH request approved!');
        } else {
          await createWFHRequest(payload);
          alert('WFH request submitted! It is now pending approval.');
        }
      } catch (error) {
        console.log(error.message);
        alert('Failed to submit WFH request. Please try again.');
      }
    },
  },
  onMounted() {
    const today = new Date();
    this.minDate = today.toISOString().split('T')[0];
    const oneYearFromNow = new Date(today.setFullYear(today.getFullYear() + 1));
    this.maxDate = oneYearFromNow.toISOString().split('T')[0];
  },
};
</script>

<style scoped>
.apply-arrangement {
  max-width: 600px;
  margin: 0 auto;
}
</style>
