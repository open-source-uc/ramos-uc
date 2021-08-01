var do_analytics_work = true

/**
 * Google Analytics Event Helper
 * @param {string} action - Action that trigers the event
 * @param {Object} data   - Data related to the event
 */
export default function ga_event(action, data) {
    if (!do_analytics_work) return
    try {
        gtag("event", action, data)
    } catch (error) {
        do_analytics_work = false
        console.info("Something wrong happened with analytics, it will be disabled.")
    }
}
