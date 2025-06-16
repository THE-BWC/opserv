import '../sass/project.scss';

/* Project specific Javascript goes here. */

// This function displays the current time in EST (Eastern Standard Time) and updates it every second.
function displayEstTime() {
  let clock = document.getElementById('clock');

  if (clock !== null) {
    clock.innerHTML = Intl.DateTimeFormat('en', {
      timeStyle: 'long',
      hourCycle: 'h24',
      timeZone: 'America/New_York',
    }).format(new Date());
    setTimeout(displayEstTime, 1000);
  }
}

// Initialize the clock display when the window loads
window.addEventListener('load', (event) => {
  displayEstTime();
});
