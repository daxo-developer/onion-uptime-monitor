async function loadData() {
    try {
        const response = await fetch('./analytics.json');
        const data = await response.json();
        
        const services = Object.keys(data);
        const totalServices = services.length;
        
        let totalUptime = 0;
        let totalLatency = 0;
        
        const uptimes = [];
        const p50 = [];
        const p95 = [];

        services.forEach(key => {
            const svc = data[key];
            totalUptime += svc.uptime_pct;
            totalLatency += svc.latency_p50_ms;
            
            uptimes.push(svc.uptime_pct);
            p50.push(svc.latency_p50_ms);
            p95.push(svc.latency_p95_ms);
        });

        updateKPIs(totalServices, totalUptime / totalServices, totalLatency / totalServices);
        renderUptimeChart(services, uptimes);
        renderLatencyChart(services, p50, p95);
        
        document.getElementById('last-updated').innerText = `Updated: ${new Date().toLocaleTimeString()}`;

    } catch (error) {
        console.error("Error loading analytics.json:", error);
        document.body.innerHTML += "<p style='color:red; text-align:center;'>Error: Could not load analytics.json. Ensure you are running a local server.</p>";
    }
}

function updateKPIs(total, avgUptime, avgLatency) {
    document.getElementById('kpi-total').innerText = total;
    document.getElementById('kpi-uptime').innerText = `${avgUptime.toFixed(2)}%`;
    document.getElementById('kpi-latency').innerText = `${avgLatency.toFixed(0)} ms`;
}

function renderUptimeChart(labels, data) {
    const ctx = document.getElementById('uptimeChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Uptime (%)',
                data: data,
                backgroundColor: data.map(val => val > 90 ? '#238636' : (val > 80 ? '#d29922' : '#da3633')),
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, max: 100, grid: { color: '#30363d' }, ticks: { color: '#8b949e' } },
                x: { grid: { display: false }, ticks: { color: '#8b949e', maxRotation: 45, minRotation: 45 } }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function renderLatencyChart(labels, p50Data, p95Data) {
    const ctx = document.getElementById('latencyChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'p50 (Median)',
                    data: p50Data,
                    backgroundColor: '#58a6ff',
                    borderRadius: 4
                },
                {
                    label: 'p95 (Tail)',
                    data: p95Data,
                    backgroundColor: '#da3633',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, grid: { color: '#30363d' }, ticks: { color: '#8b949e' } },
                x: { grid: { display: false }, ticks: { color: '#8b949e', maxRotation: 45, minRotation: 45 } }
            },
            plugins: { legend: { labels: { color: '#c9d1d9', boxWidth: 12 } } }
        }
    });
}

document.addEventListener('DOMContentLoaded', loadData);
