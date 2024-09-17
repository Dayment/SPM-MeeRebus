import { createClient } from '@supabase/supabase-js'

export const supabase = createClient('https://xysbrhskuhqgthgxeiac.supabase.co', 
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh5c2JyaHNrdWhxZ3RoZ3hlaWFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU3OTA1MzgsImV4cCI6MjA0MTM2NjUzOH0.P9Jd12v5yeOTeDltRs-_x-HlXN0ml4YS1N7NWY1WAwk')