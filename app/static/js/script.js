const skipped = (ctx, value) => ctx.p0.skip || ctx.p1.skip ? value : undefined;
const above50 = (ctx, value) => ctx.p1.parsed.y > 50 ? value : undefined;
const below50 = (ctx, value) => ctx.p1.parsed.y < 50 ? value : undefined;

const genericOptions = {
    fill: false,
    interaction: {
        intersect: false
    },
    radius: 3,
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

const config = {
    type: 'line',
    data: {
        labels: ["9AM", "12PM", "3PM", "6PM", "9PM", "12AM", "3AM", "6AM", "9AM"],
        datasets: [
            {
                label: 'My First Dataset',
                data: [13, 78, 23, 56, 65, 78, 45, 23, 19],
                borderColor: 'green',
                segment: {
                    borderColor: ctx => skipped(ctx, 'rgb(0,0,0,0.2)') || above50(ctx, 'rgba(255, 0, 21, 0.5)') || below50(ctx, 'rgba(0, 204, 255, 0.5)'),
                    borderDash: ctx => skipped(ctx, [6, 6]),
                }
            }
        ]
    },
    options: genericOptions
};

var myChart = new Chart(
    document.getElementById('myChart'),
    config
);