<template>
    <div class="container d-flex justify-content-center align-items-center" style="height: 100vh;">
        <div class="col-md-4">
            <h2 class="text-center">Please key in your Employee ID to log in</h2>
            <!-- submit.prevent just makes sure they can't login without inputting anything. Won't show alert like invalid ID though, bootstrap built in popup exists -->
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label for="empId">Employee ID:</label>
                    <input type="number" id="empId" v-model="empId" class="form-control" placeholder="Please key in your employee ID" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
            <!-- Error alert using Bootstrap if invalid employee ID submitted -->
            <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
                {{ errorMessage }}
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import eventBus from '../eventBus'; 

export default {
    name: 'LoginView',
    data() {
        return {
            empId: '',
            errorMessage: ''
            
        }
    },
    methods: {
        async handleLogin() {
            this.errorMessage = ''; 
            const isValid = await this.checkValidID();

            if (isValid) {
                console.log('Logged in with Employee ID:', this.empId);
                localStorage.setItem('employeeId', this.empId);
                // await this.getArrangementData(); 
                eventBus.isLoggedIn = true; 
                // await this.checkEmployeeRole(); 

                const employeeData = JSON.parse(localStorage.getItem('employeeData'));
                if (employeeData && employeeData.role === 1) {
                    eventBus.isHR = true; 
                }
                if (employeeData && employeeData.position === "Director" || employeeData.position === "MD"){
                    eventBus.isDir = true;
                }
                if  (employeeData && employeeData.role === 3) {
                    eventBus.isManager = true; 
                }


                this.$router.push('/home');
            } else {
                this.errorMessage = 'Invalid Employee ID or not authorized to log in from this location. Please try again.';
            }
        },
        async checkValidID() {
            try {
                const response = await axios.get(`http://48.218.168.55:5000/employee/${this.empId}`);
                localStorage.setItem('employeeData', JSON.stringify(response.data));
                console.log(response.data);
                
                // if ((response.data.role == 1 || response.data.position == "MD") && response.data.position != "Director") {
                //     // Only if HR, get all the arrangement data
                //     eventBus.isHR = true; 
                //     localStorage.setItem('isHR', true);

                //     await this.getArrangementData();
                    
                //     await this.getOwnUnderlingArrangementData();

                //     // Get their own arrangement as well
                //     await this.getOwnArrangementData(response.data.staff_id)
                // }else if (response.data.role == 3 && response.data.position == "Director"){
                //     eventBus.isDir = true; 
                //     localStorage.setItem('isDir', true);
                    
                //     await this.getOwnUnderlingArrangementData();

                // }else if( response.data.role == 3 && response.data.position == "Sale Manager" || response.data.position == "Finance Manager"){
                //     await this.getOwnUnderlingArrangementData();
                //     await this.getOwnArrangementData(response.data.staff_id);
                // }else{
                //     // Get own WFH arrangment
                //     await this.getOwnArrangementData(response.data.staff_id)
                // }

                if (response.data.role == 1 && response.data.position != "MD" && response.data.position != "Director") {
                    // Only if HR, get all the arrangement data
                    eventBus.isHR = true; 
                    localStorage.setItem('isHR', true);

                    await this.getArrangementData();
                    
                    await this.getOwnUnderlingData(response.data.staff_id);

                    // Get their own arrangement as well
                    await this.getOwnArrangementData(response.data.staff_id)
                }else if (response.data.role == 1 && response.data.position == "Director" || response.data.position == "MD"){
                    eventBus.isHR = true; 
                    localStorage.setItem('isHR', true);
                    eventBus.isDir = true; 
                    localStorage.setItem('isDir', true);
                    eventBus.isManager = true; 
                    localStorage.setItem('isManager', true);

                    await this.getOwnUnderlingData(response.data.staff_id);

                }else if( response.data.role == 3 ){

                    eventBus.isManager = true; 
                    localStorage.setItem('isManager', true);

                    await this.getOwnUnderlingData(response.data.staff_id);
                    await this.getOwnArrangementData(response.data.staff_id);
                }else{
                    // Get own WFH arrangment
                    await this.getOwnArrangementData(response.data.staff_id)
                }
                
                return true;
            } catch (error) {
                console.error(error);
                // Check if the error response contains a specific message
                if (error.response && error.response.data && error.response.data.error) {
                    this.errorMessage = error.response.data.error;
                } else {
                    this.errorMessage = 'An unexpected error occurred. Please try again later.';
                }
                return false; 
            }
        },
        async getArrangementData() {
            try {
                const response = await axios.get('http://48.218.168.55:5000/arrangement');
                localStorage.setItem('arrangement', JSON.stringify(response.data));
                console.log(response.data);  
            } catch (error) {
                console.log(error);
            }
        },
        async getOwnArrangementData(staff_id) {
            try {
                const response = await axios.get(`http://48.218.168.55:5000/arrangement/emp/${staff_id}`);
                localStorage.setItem('empArrangement', JSON.stringify(response.data));
                console.log(response.data);  
            } catch (error) {
                console.log(error);
            }
        },
        async getOwnUnderlingData(staff_id) {
            try {
                const response = await axios.get(`http://48.218.168.55:5000//manager/underlings/${staff_id}`);
                localStorage.setItem('teamData', JSON.stringify(response.data));
                console.log(response.data);  
            } catch (error) {
                console.log(error);
            }
        },
        async checkEmployeeRole() {
            try {
                const employeeData = JSON.parse(localStorage.getItem('employeeData'));
                if (employeeData && employeeData.role === 1) {
                    eventBus.isHR = true; 
                }
                if (employeeData && employeeData.position === "Director"){
                    eventBus.isDir = true;
                }

            } catch (error) {
                console.error(error);
            }
        },
    }
}
</script>
