/**
 * Charts module — Chart.js radar and bar chart factories.
 */

const CHART_COLORS = {
    teal: 'rgba(80, 227, 194, 1)',
    tealFaded: 'rgba(80, 227, 194, 0.15)',
    gold: 'rgba(251, 191, 36, 1)',
    goldFaded: 'rgba(251, 191, 36, 0.15)',
    coral: 'rgba(251, 113, 133, 1)',
    coralFaded: 'rgba(251, 113, 133, 0.15)',
    navy: 'rgba(19, 34, 87, 1)',
    slate: 'rgba(148, 163, 184, 0.5)',
    gridLine: 'rgba(51, 65, 85, 0.5)',
    gridLabel: 'rgba(148, 163, 184, 0.8)',
};

// Formatted category labels for display
const CATEGORY_LABELS = {
    'pressing_intensity': 'Pressing',
    'attacking_quality': 'Attacking',
    'defensive_solidity': 'Defence',
    'big_game_performance': 'Big Games',
    'youth_development': 'Youth Dev',
    'squad_health': 'Squad Health',
    'transfer_acumen': 'Transfers',
    'media_stability': 'Media',
    'stakeholder_alignment': 'Stakeholders',
};

// Default Chart.js settings for our dark theme
Chart.defaults.color = CHART_COLORS.gridLabel;
Chart.defaults.borderColor = CHART_COLORS.gridLine;
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";

/**
 * Create a radar chart for a single manager.
 */
function createRadarChart(canvasId, managerData, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    const cats = managerData.peer_categories;
    const labels = Object.keys(cats).map(k => CATEGORY_LABELS[k] || k);
    const values = Object.values(cats);

    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: managerData.name,
                data: values,
                backgroundColor: options.fillColor || CHART_COLORS.tealFaded,
                borderColor: options.borderColor || CHART_COLORS.teal,
                borderWidth: 2,
                pointBackgroundColor: options.borderColor || CHART_COLORS.teal,
                pointRadius: 3,
                pointHoverRadius: 5,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: {
                duration: options.animate === false ? 0 : 800,
                easing: 'easeOutQuart',
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#f8fafc',
                    bodyColor: '#94a3b8',
                    borderColor: CHART_COLORS.teal,
                    borderWidth: 1,
                    padding: 10,
                    callbacks: {
                        label: (ctx) => `${ctx.raw.toFixed(1)} / 10`
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    ticks: {
                        stepSize: 2,
                        display: false,
                    },
                    grid: {
                        color: CHART_COLORS.gridLine,
                    },
                    angleLines: {
                        color: CHART_COLORS.gridLine,
                    },
                    pointLabels: {
                        font: { size: options.labelSize || 10, weight: '500' },
                        color: CHART_COLORS.gridLabel,
                    }
                }
            }
        }
    });
}

/**
 * Create a comparison radar with two managers overlaid.
 */
function createComparisonRadar(canvasId, manager1, manager2) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return null;

    // Destroy existing chart if any
    const existing = Chart.getChart(canvas);
    if (existing) existing.destroy();

    const cats1 = manager1.peer_categories;
    const cats2 = manager2.peer_categories;
    const labels = Object.keys(cats1).map(k => CATEGORY_LABELS[k] || k);

    const ctx = canvas.getContext('2d');
    return new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: manager1.name,
                    data: Object.values(cats1),
                    backgroundColor: CHART_COLORS.tealFaded,
                    borderColor: CHART_COLORS.teal,
                    borderWidth: 2,
                    pointBackgroundColor: CHART_COLORS.teal,
                    pointRadius: 3,
                },
                {
                    label: manager2.name,
                    data: Object.values(cats2),
                    backgroundColor: CHART_COLORS.coralFaded,
                    borderColor: CHART_COLORS.coral,
                    borderWidth: 2,
                    pointBackgroundColor: CHART_COLORS.coral,
                    pointRadius: 3,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            animation: { duration: 600, easing: 'easeOutQuart' },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 16,
                        font: { size: 12 },
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    titleColor: '#f8fafc',
                    bodyColor: '#94a3b8',
                    borderColor: CHART_COLORS.teal,
                    borderWidth: 1,
                    callbacks: {
                        label: (ctx) => `${ctx.dataset.label}: ${ctx.raw.toFixed(1)}`
                    }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    ticks: { stepSize: 2, display: false },
                    grid: { color: CHART_COLORS.gridLine },
                    angleLines: { color: CHART_COLORS.gridLine },
                    pointLabels: {
                        font: { size: 11, weight: '500' },
                        color: CHART_COLORS.gridLabel,
                    }
                }
            }
        }
    });
}

/**
 * Get a score-based color (red → yellow → green).
 */
function scoreColor(score, max = 100) {
    const pct = score / max;
    if (pct >= 0.7) return CHART_COLORS.teal;
    if (pct >= 0.5) return CHART_COLORS.gold;
    return CHART_COLORS.coral;
}
