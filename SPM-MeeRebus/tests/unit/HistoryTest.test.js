/**
 * @vitest-environment happy-dom
 */

// THE ABOVE PART IS A MUST!!!!!!!!!!!!!!!!!!!!!
// vitest is running in node environment so happy dom will emulate a web browser
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
// it = Test in vitest API docs vi = Mock function
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import History from "@/views/AppHistory.vue"
vi.mock('axios')

describe('Testing Application History', () => {
    let router;

    beforeEach(() => {
        router = createRouter({
        history: createWebHistory(),
        routes: [{ path: '/', name: 'history' }]
        })

        // Mock localStorage
        Object.defineProperty(window, 'localStorage', {
        value: {
            getItem: vi.fn(),
            setItem: vi.fn(),
            removeItem: vi.fn()
        },
        writable: true
        })

        vi.clearAllMocks()
    })

    afterEach(() => {
        // Restore Date after each test
        vi.useRealTimers()
        
    })

    it('mounts successfully', () => {
        const wrapper = mount(History, {
        global: {
            plugins: [router]
        }
        })
        expect(wrapper.exists()).toBe(true)
    })

    it('loads WFH details from localStorage', async () => {
        const mockWFHDetails = [
            {
                "arrangement_id": 11,
                "date": "2024-12-01T09:00:00",
                "reason_man": "No",
                "reason_staff": "Just for testing",
                "reporting_manager": 210001,
                "staff_id": 150065,
                "status": 2,
                "time": 3
            },
            {
                "arrangement_id": 10,
                "date": "2024-11-01T09:00:00",
                "reason_man": null,
                "reason_staff": "Just for testing",
                "reporting_manager": 210001,
                "staff_id": 150065,
                "status": 0,
                "time": 1
            },
            {
                "arrangement_id": 15,
                "date": "2025-01-01T09:00:00",
                "reason_man": null,
                "reason_staff": "Just for testing",
                "reporting_manager": 210001,
                "staff_id": 150065,
                "status": 1,
                "time": 1
            },
            {
                "arrangement_id": 16,
                "date": "2025-11-01T09:00:00",
                "reason_man": null,
                "reason_staff": "Just for testing",
                "reporting_manager": 210001,
                "staff_id": 150065,
                "status": 3,
                "time": 1
            }
        ]
        
        localStorage.getItem.mockReturnValue(JSON.stringify(mockWFHDetails))
        
        const wrapper = mount(History, {
            global: {
                plugins: [router]
            }
        })
        
        // Wait for the next tick to ensure all reactive updates have been processed
        await wrapper.vm.$nextTick()
        
        // console.log('arrangements:', wrapper.vm.arrangements)
        
        // Check if arrangements is defined and has the expected structure
        expect(wrapper.vm.arrangements).toBeDefined()
        // I expect to return array even if only 1 object
        expect(Array.isArray(wrapper.vm.arrangements)).toBe(true)
        expect(wrapper.vm.arrangements).toHaveLength(mockWFHDetails.length)
        
        if (wrapper.vm.arrangements.length > 0) {
            const firstItem = wrapper.vm.arrangements[0]
            expect(firstItem).toHaveProperty('arrangement_id')
            expect(firstItem).toHaveProperty('status')
            expect(firstItem).toHaveProperty('date')
            expect(firstItem).toHaveProperty('reason_staff')
            expect(firstItem).toHaveProperty('reason_man')
        }
        
        // Test the filteredArrangements computed property
        expect(wrapper.vm.filteredArrangements).toHaveLength(mockWFHDetails.length)
        
        // Test filtering by status
        wrapper.vm.selectedStatus = '0'
        await wrapper.vm.$nextTick()
        expect(wrapper.vm.filteredArrangements).toHaveLength(1)
        expect(wrapper.vm.filteredArrangements[0].status).toBe(0)
        
        // Test date filtering
        wrapper.vm.selectedStatus = ''
        wrapper.vm.startDate = '2024-11-30'
        wrapper.vm.endDate = '2024-12-02'
        await wrapper.vm.$nextTick()
        expect(wrapper.vm.filteredArrangements).toHaveLength(1)
        expect(wrapper.vm.filteredArrangements[0].arrangement_id).toBe(11)

        // Check cancel button exists
        // wrapper.vm.selectedStatus = '0'
        // wrapper.vm.startDate = ''
        // wrapper.vm.endDate = ''
        // await wrapper.vm.$nextTick()
        // const cancelButton = wrapper.find('button.btn-danger');
        // expect(cancelButton.exists()).toBe(true);

        // Make sure cancel button does not show up for already cancelled WFH
        // wrapper.vm.selectedStatus = '3'
        // wrapper.vm.startDate = ''
        // wrapper.vm.endDate = ''
        // await wrapper.vm.$nextTick()
        // const cancelButton2 = wrapper.find('button.btn-danger');
        // expect(cancelButton2.exists()).toBe(false);

    })

    it('displays correct status labels', () => {
        const wrapper = mount(History, {
            global: {
                plugins: [router]
            }
        })

        expect(wrapper.vm.getStatusLabel(0)).toBe('Pending')
        expect(wrapper.vm.getStatusLabel(1)).toBe('Accepted')
        expect(wrapper.vm.getStatusLabel(2)).toBe('Rejected')
        expect(wrapper.vm.getStatusLabel(3)).toBe('Cancelled/Withdrawn')
    })

    it('should not display the cancel button for arrangements with status other than 0 or 1', async () => {
        const mockArrangement = [{
            arrangement_id: 2,
            date: '2024-12-02T09:00:00',
            reason_man: null,
            reason_staff: 'Test Reason',
            reporting_manager: 210001,
            staff_id: 150065,
            status: 2, 
            time: 3
        }];

        localStorage.getItem.mockReturnValue(JSON.stringify(mockArrangement))


        const wrapper = mount(History, {
            global: {
                plugins: [router]
            },
        });

        // Wait for any updates to be processed
        await wrapper.vm.$nextTick();
        // console.log(wrapper.html()); 

        // Check if the cancel button does not exist
        const cancelButton = wrapper.find('button.btn-danger'); 
        expect(cancelButton.exists()).toBe(false);
        
    });
    // This keeps failing for some reason, I don't see the problem, someone else can help to take a look at this
    it('it should display cancel button for status 0 or 1 and date is today and beyond', async () => {
        
        const mockArrangement = [{
            arrangement_id: 2,
            date: '2024-12-02T09:00:00',
            reason_man: null,
            reason_staff: 'Test Reason',
            reporting_manager: 210001,
            staff_id: 150065,
            status: 0, 
            time: 3
        }];
        localStorage.getItem.mockReturnValue(JSON.stringify(mockArrangement))

        const wrapper = mount(History, {
            global: {
                plugins: [router]
            },
        });

        await wrapper.vm.$nextTick();

        vi.useFakeTimers()

        // Make sure that mocked today's date is before requested arrangement date
        vi.setSystemTime(new Date('2000-12-01T00:00:00'))

        await wrapper.vm.$nextTick();

        
        // console.log(wrapper.html());
        // console.log(wrapper.vm.filteredArrangements)

        const cancelButton = wrapper.find('button.btn-danger')
        expect(cancelButton.exists()).toBe(true)
    });


    it('should not display the cancel button for WFH approved in the past', async () => {
        // Mock arrangement data with status 1 (approved) and a past date
        const mockArrangement = [{
            arrangement_id: 3,
            date: '2023-10-01T09:00:00', 
            reason_man: null,
            reason_staff: 'Test Reason',
            reporting_manager: 210001,
            staff_id: 150065,
            status: 1, 
            time: 3
        }];
        localStorage.getItem.mockReturnValue(JSON.stringify(mockArrangement))

        const wrapper = mount(History, {
            global: {
                plugins: [router]
            },
        });


        await wrapper.vm.$nextTick();

        // console.log(wrapper.html());
        // console.log(wrapper.vm.filteredArrangements)

        vi.useFakeTimers()
        // Make sure that mocked today's date is after requested arrangement date
        vi.setSystemTime(new Date('3000-12-01T00:00:00'))

        await wrapper.vm.$nextTick();
        const cancelButton = wrapper.find('button.btn-danger')
        expect(cancelButton.exists()).toBe(false)

    });

})