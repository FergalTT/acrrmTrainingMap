import mixpanel from 'mixpanel-browser';

// Initialize Mixpanel
const MIXPANEL_TOKEN = import.meta.env.VITE_MIXPANEL_TOKEN || '160de29a1dcd710d72e76395e7ff969d';

// Initialize Mixpanel on module load
mixpanel.init(MIXPANEL_TOKEN, {
  debug: import.meta.env.DEV, // Enable debug mode in development
  track_pageview: true, // Automatically track page views
  persistence: 'localStorage' // Use localStorage for persistence
});

/**
 * Track a custom event
 * @param {string} eventName - Name of the event to track
 * @param {Object} properties - Additional properties to track with the event
 */
export const trackEvent = (eventName, properties = {}) => {
  mixpanel.track(eventName, properties);
};

/**
 * Track a page view
 * @param {string} pageName - Name of the page viewed
 * @param {Object} properties - Additional properties to track
 */
export const trackPageView = (pageName, properties = {}) => {
  mixpanel.track_pageview({
    page: pageName,
    ...properties
  });
};

/**
 * Set user properties
 * @param {Object} properties - User properties to set
 */
export const setUserProperties = (properties) => {
  mixpanel.people.set(properties);
};

/**
 * Identify a user
 * @param {string} userId - Unique identifier for the user
 */
export const identifyUser = (userId) => {
  mixpanel.identify(userId);
};

/**
 * Track filter usage
 * @param {string} filterType - Type of filter used (trainingTypes, rotations, mmm, siteTypes)
 * @param {Array} selectedFilters - Array of selected filter values
 */
export const trackFilterUsage = (filterType, selectedFilters) => {
  trackEvent('Filter Applied', {
    filterType,
    selectedFilters,
    filterCount: selectedFilters.length
  });
};

/**
 * Track map interaction
 * @param {string} interactionType - Type of interaction (marker_click, zoom, pan)
 * @param {Object} details - Additional details about the interaction
 */
export const trackMapInteraction = (interactionType, details = {}) => {
  trackEvent('Map Interaction', {
    interactionType,
    ...details
  });
};

export default mixpanel;
