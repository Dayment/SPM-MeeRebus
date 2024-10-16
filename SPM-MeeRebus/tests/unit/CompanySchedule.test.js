/**
 * @vitest-environment happy-dom
 */

// THE ABOVE PART IS A MUST!!!!!!!!!!!!!!!!!!!!!
// vitest is running in node environment so happy dom will emulate a web browser
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import CompanySchedule from '@/views/CompanySchedule.vue'
import { getAllEmployee, getDeptApprovedArrangement2 } from '@/api/api'

// Mock the API calls
vi.mock('@/api/api', () => ({
    getAllEmployee: vi.fn(),
    getDeptApprovedArrangement2: vi.fn()
}))

// Mock the router
vi.mock('vue-router', () => ({
    useRouter: () => ({
    push: vi.fn()
    })
}))

describe('CompanySchedule', () => {
    let wrapper

    beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks()

    // Mock localStorage
    global.localStorage = {
    getItem: vi.fn(() => '160075'),
    setItem: vi.fn()
    }

    // Mock API responses
    getAllEmployee.mockResolvedValue({})
    getDeptApprovedArrangement2.mockResolvedValue([
        {
        date: '2024-09-22',
        employee: {
        staff_fname: 'Oliver',
        staff_lname: 'Chan',
        dept: 'Engineering',
        position: 'Senior Engineers'
        },
        reason: 'No Reason Provided'
        },
        {
        date: '2024-11-02',
        employee: {
        staff_fname: 'James',
        staff_lname: 'Tan',
        dept: 'HR',
        position: 'L&D Team'
        },
        reason: 'No Reason Provided'
        }
    ])

    // Mount the component
    wrapper = mount(CompanySchedule)
    })

    it('renders correctly', () => {
    expect(wrapper.find('.dropdown').exists()).toBe(true)
    expect(wrapper.find('.table-container').exists()).toBe(true)
    })

    it('loads WFH details on mount', async () => {
    await nextTick()
    expect(getDeptApprovedArrangement2).toHaveBeenCalled()
    expect(wrapper.vm.approvedWFHDetails.length).toBe(2)
    })

    it('filters WFH details by team', async () => {
        await nextTick()
        
        // Select Engineering team
        await wrapper.vm.selectTeam('Engineering')
        
        await wrapper.vm.$forceUpdate()
        await nextTick() // Wait for the next tick to allow the filteredWFHDetails to update
        
        console.log('Selected Team:', wrapper.vm.selectedTeam)
        console.log('Filtered WFH Details:', wrapper.vm.filteredWFHDetails)
        
        expect(wrapper.vm.selectedTeam).toBe('Engineering')
        expect(wrapper.vm.filteredWFHDetails.length).toBe(1)
        expect(wrapper.vm.filteredWFHDetails[0].employee.dept).toBe('Engineering')
    })

    it('filters WFH details by sub-team', async () => {
        await nextTick()
        
        // Select HR Team sub-team
        // await wrapper.find('#dropdownhrTeam').trigger('click')
        // const HRTeamOption = wrapper.findAll('.dropdown-item').find(el => el.text() === 'HR Team')
        // await HRTeamOption.trigger('click')
        await wrapper.vm.selectTeam('HR')
        await wrapper.vm.selecthrTeam('L&D Team')

        await wrapper.vm.$forceUpdate()
        await nextTick() // Wait for the next tick to allow the filteredWFHDetails to update

        console.log('Selected Team:', wrapper.vm.selectedhrTeam)
        console.log('Filtered WFH Details:', wrapper.vm.filteredWFHDetails)
        
        expect(wrapper.vm.selectedTeam).toBe('HR')
        expect(wrapper.vm.selectedhrTeam).toBe('L&D Team')
        expect(wrapper.vm.filteredWFHDetails.length).toBe(1)
        expect(wrapper.vm.filteredWFHDetails[0].employee.position).toBe('L&D Team')
        })

    it('filters WFH details by search query', async () => {
    await nextTick()
    
    wrapper.vm.searchQuery = 'Oliver'
    await nextTick()
    
    expect(wrapper.vm.filteredWFHDetails.length).toBe(1)
    expect(wrapper.vm.filteredWFHDetails[0].employee.staff_fname).toBe('Oliver')
    })

    it('filters WFH details by date range', async () => {
    await nextTick()
    
    wrapper.vm.startDate = '2024-09-22'
    wrapper.vm.endDate = '2024-10-01'
    await nextTick()
    
    expect(wrapper.vm.filteredWFHDetails.length).toBe(1)
    expect(wrapper.vm.filteredWFHDetails[0].date).toBe('2024-09-22')
    })
})