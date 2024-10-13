/**
 * @vitest-environment happy-dom
 */

// THE ABOVE PART IS A MUST!!!!!!!!!!!!!!!!!!!!!
// vitest is running in node environment so happy dom will emulate a web browser
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
// it = Test in vitest API docs vi = Mock function
import { describe, it, expect, vi, beforeEach } from 'vitest'
import HomeView from '@/views/HomeView.vue'
import Calendar from '@/components/Calendar.vue'

vi.mock('axios')

describe('Testing HomeView', () => {
    let router;

    beforeEach(() => {
        router = createRouter({
        history: createWebHistory(),
        routes: [{ path: '/', name: 'home' }]
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
    })

    it('mounts successfully', () => {
        const wrapper = mount(HomeView, {
        global: {
            plugins: [router],
            stubs: {
            Calendar: true
            }
        }
        })
        expect(wrapper.exists()).toBe(true)
    })

    it('redirects to home when no employeeId is present', async () => {
        vi.spyOn(router, 'push')
        
        localStorage.getItem.mockReturnValue(null)
        
        mount(HomeView, {
        global: {
            plugins: [router],
            stubs: {
            Calendar: true
            }
        }
        })
        
        await router.isReady()
        expect(router.push).toHaveBeenCalledWith('/')
    })

    it('loads WFH details from localStorage', async () => {
        const mockWFHDetails = [{ date: '2024-01-01', status: 1 }]
        localStorage.getItem.mockImplementation((key) => {
        if (key === 'employeeId') return '12345'
        if (key === 'empArrangement') return JSON.stringify(mockWFHDetails)
        })
        
        const wrapper = mount(HomeView, {
        global: {
            plugins: [router],
            stubs: {
            Calendar: true
            }
        }
        })
        
        // Wait and make sure page loaded all updates before proceeding
        await wrapper.vm.$nextTick()
        expect(wrapper.vm.approvedWFHDetails).toEqual(mockWFHDetails)
    })

    it('handles error when parsing WFH details fails', async () => {
        localStorage.getItem.mockImplementation((key) => {
        if (key === 'employeeId') return '12345'
        if (key === 'empArrangement') return 'invalid JSON'
        })
        
        const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
        
        mount(HomeView, {
        global: {
            plugins: [router],
            stubs: {
            Calendar: true
            }
        }
        })
        
        await new Promise(resolve => setTimeout(resolve, 0))
        expect(consoleSpy).toHaveBeenCalled()
        consoleSpy.mockRestore()
    })

    it('passes correct props to Calendar component', async () => {
        const mockWFHDetails = [{ date: '2024-01-01', status: 1 }]
        localStorage.getItem.mockImplementation((key) => {
        if (key === 'employeeId') return '12345'
        if (key === 'empArrangement') return JSON.stringify(mockWFHDetails)
        })
        
        const wrapper = mount(HomeView, {
        global: {
            plugins: [router],
            
        }
        })
        
        await wrapper.vm.$nextTick()
        const calendar = wrapper.findComponent(Calendar)
        expect(calendar.props('wfhDetails')).toEqual(mockWFHDetails)
    })
})