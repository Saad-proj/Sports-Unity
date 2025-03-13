// Fetch data from the template
const universities = {{ total_universities }};
const players = {{ total_players }};
const events = {{ total_events }};
const eventsThisMonth = {{ events_this_month }};
const matches = {{ total_matches }};
const nextMatch = "{{ next_match.date|date:'Y-m-d H:i:s' if next_match else 'No upcoming match' }}";

// Total Universities Chart
new Chart(document.getElementById("universitiesChart"), {
  type: "doughnut",
  data: {
    labels: ["Total Universities"],
    datasets: [
      {
        data: [universities],
        backgroundColor: ["#36A2EB"],
      },
    ],
  },
});

// Total Players Chart
new Chart(document.getElementById("playersChart"), {
  type: "bar",
  data: {
    labels: ["Total Players"],
    datasets: [
      {
        data: [players],
        backgroundColor: ["#FF6384"],
      },
    ],
  },
});

// Total Events Chart
new Chart(document.getElementById("eventsChart"), {
  type: "pie",
  data: {
    labels: ["Total Events"],
    datasets: [
      {
        data: [events],
        backgroundColor: ["#FFCE56"],
      },
    ],
  },
});

// Events This Month Chart
new Chart(document.getElementById("eventsThisMonthChart"), {
  type: "line",
  data: {
    labels: ["Events This Month"],
    datasets: [
      {
        data: [eventsThisMonth],
        backgroundColor: ["#4BC0C0"],
      },
    ],
  },
});

// Total Matches Chart
new Chart(document.getElementById("matchesChart"), {
  type: "polarArea",
  data: {
    labels: ["Total Matches"],
    datasets: [
      {
        data: [matches],
        backgroundColor: ["#9966FF"],
      },
    ],
  },
});

// Next Match Chart
new Chart(document.getElementById("nextMatchChart"), {
  type: "radar",
  data: {
    labels: ["Next Match"],
    datasets: [
      {
        label: nextMatch,
        data: [1],
        backgroundColor: ["#FF9F40"],
      },
    ],
  },
});

console.log("Universities:", universities);
console.log("Players:", players);
console.log("Events:", events);
console.log("Events This Month:", eventsThisMonth);
console.log("Matches:", matches);
console.log("Next Match:", nextMatch);
