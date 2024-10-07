import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000'; // move to env


export const getAllEmployee = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/employee`);
    return response.data;
  } catch (error) {
    console.error("Error fetching employee data:", error);
    throw error;
  }
};

export const getAllArrangement = async () => { 
  try {
    const response = await axios.get(`${API_BASE_URL}/arrangement`);
    return response.data;
  } catch (error) {
    console.error("Error fetching arrangement data:", error);
    throw error;
  }
};

export const getAllApprovedArrangement = async () => { 
    try {
      const response = await axios.get(`${API_BASE_URL}/arrangement/approved`);
      return response.data;
    } catch (error) {
      console.error("Error fetching arrangement data:", error);
      throw error;
    }
  };

export const getTeamApprovedArrangement = async (empId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/arrangement/posi/${empId}`);
      localStorage.setItem("teamArrangements", JSON.stringify(response.data));
      return response.data; 
    } catch (error) {
      console.error('Error fetching approved arrangements:', error);
      throw error; 
    }
  };

  export const getDeptApprovedArrangement = async (empId) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/arrangement/dept/${empId}`);
      localStorage.setItem("deptArrangements", JSON.stringify(response.data));
      return response.data; 
    } catch (error) {
      console.error('Error fetching approved arrangements:', error);
      throw error; 
    }
  };

  export const getDeptApprovedArrangement2 = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/arrangement/obj`);
      localStorage.setItem("deptArrangements", JSON.stringify(response.data));
      return response.data; 
    } catch (error) {
      console.error('Error fetching approved arrangements:', error);
      throw error; 
    }
  };
