/**
 * Head-to-head comparison module.
 */

let compareChart = null;

function initComparison(managers) {
    const leftSelect = document.getElementById('compare-left');
    const rightSelect = document.getElementById('compare-right');
    const shareSelect = document.getElementById('share-select');

    // Populate dropdowns
    managers.forEach(m => {
        const opt1 = new Option(m.name, m.slug);
        const opt2 = new Option(m.name, m.slug);
        const opt3 = new Option(m.name, m.slug);
        leftSelect.appendChild(opt1);
        rightSelect.appendChild(opt2);
        shareSelect.appendChild(opt3);
    });

    // Pre-select top 2
    if (managers.length >= 2) {
        leftSelect.value = managers[0].slug;
        rightSelect.value = managers[1].slug;
        renderComparison(managers);
    }

    leftSelect.addEventListener('change', () => renderComparison(managers));
    rightSelect.addEventListener('change', () => renderComparison(managers));
}

function renderComparison(managers) {
    const leftSlug = document.getElementById('compare-left').value;
    const rightSlug = document.getElementById('compare-right').value;

    if (!leftSlug || !rightSlug || leftSlug === rightSlug) {
        document.getElementById('compare-stats').innerHTML =
            '<p style="color:var(--text-muted);text-align:center;padding:2rem;">Select two different managers</p>';
        return;
    }

    const m1 = managers.find(m => m.slug === leftSlug);
    const m2 = managers.find(m => m.slug === rightSlug);
    if (!m1 || !m2) return;

    // Radar chart
    compareChart = createComparisonRadar('compare-chart', m1, m2);

    // Stats comparison
    const stats = [
        { label: 'Final Score', key: 'final_score', max: 100 },
        { label: 'Peer Score', key: 'peer_score', max: 10 },
        { label: 'Fit Index', key: 'fit_index', max: 100 },
        { label: 'Potential', key: 'potential_index', max: 100 },
        { label: 'Spurs-Fit Total', key: 'spursfit_total', max: 100 },
    ];

    // Add peer categories
    if (m1.peer_categories) {
        Object.keys(m1.peer_categories).forEach(cat => {
            stats.push({
                label: CATEGORY_LABELS[cat] || cat,
                key: `peer_cat_${cat}`,
                max: 10,
                getValue: (m) => m.peer_categories[cat],
            });
        });
    }

    let html = '';
    stats.forEach(s => {
        const v1 = s.getValue ? s.getValue(m1) : m1[s.key];
        const v2 = s.getValue ? s.getValue(m2) : m2[s.key];
        const w1 = v1 > v2 ? ' stat-winner' : '';
        const w2 = v2 > v1 ? ' stat-winner' : '';

        html += `
            <div class="stat-row">
                <span class="stat-label">${s.label}</span>
                <span class="stat-value${w1}">${v1.toFixed(1)}</span>
                <span class="stat-value${w2}">${v2.toFixed(1)}</span>
            </div>
        `;
    });

    document.getElementById('compare-stats').innerHTML = `
        <div class="stat-row" style="border-bottom:2px solid var(--border-color);">
            <span class="stat-label" style="font-weight:600;">Metric</span>
            <span class="stat-value" style="color:var(--spurs-teal);font-size:0.75rem;">${m1.name.split(' ').pop()}</span>
            <span class="stat-value" style="color:var(--danger);font-size:0.75rem;">${m2.name.split(' ').pop()}</span>
        </div>
        ${html}
    `;
}
