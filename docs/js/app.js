/**
 * Main application — loads data, renders all sections.
 */

let managersData = [];
let currentSort = { key: 'rank', asc: true };

async function init() {
    try {
        const response = await fetch('data/scores.json');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        managersData = data.managers;

        renderTable(managersData);
        renderCards(managersData);
        renderDetails(managersData);
        initComparison(managersData);
        initSocial(managersData);
        initAnimations();

        // Initialize Lucide icons
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    } catch (err) {
        console.error('Failed to load data:', err);
        document.getElementById('rankings-body').innerHTML =
            `<tr><td colspan="7" style="text-align:center;padding:2rem;color:var(--text-muted);">
                Failed to load data. Run <code>python -m scripts.pipeline</code> first.
            </td></tr>`;
    }
}

// ==================== RANKINGS TABLE ====================

function renderTable(managers) {
    const tbody = document.getElementById('rankings-body');
    tbody.innerHTML = managers.map(m => {
        const rankClass = m.rank <= 3 ? `rank-${m.rank}` : 'rank-other';
        const availClass = m.available ? 'available' : 'unavailable';
        const availText = m.available ? 'Available' : 'Unavailable';

        return `
            <tr onclick="scrollToDetail('${m.slug}')" title="Click to view ${m.name}'s full profile">
                <td><span class="rank-badge ${rankClass}">${m.rank}</span></td>
                <td>
                    <div class="manager-name">${m.name}</div>
                    <div class="manager-club">${m.current_club} &middot; ${m.age}</div>
                </td>
                <td class="score-cell" style="color:${scoreColor(m.final_score)}">${m.final_score.toFixed(1)}</td>
                <td class="score-cell">${m.peer_score.toFixed(1)}</td>
                <td class="score-cell">${m.fit_index.toFixed(0)}</td>
                <td class="score-cell">${m.potential_index.toFixed(0)}</td>
                <td><span class="availability-badge ${availClass}">${availText}</span></td>
            </tr>
        `;
    }).join('');

    // Stagger animation
    staggerFadeIn(Array.from(tbody.querySelectorAll('tr')));

    // Sort handlers
    document.querySelectorAll('#rankings-table thead th[data-sort]').forEach(th => {
        th.addEventListener('click', () => sortTable(th.dataset.sort, managers));
    });
}

function sortTable(key, managers) {
    if (currentSort.key === key) {
        currentSort.asc = !currentSort.asc;
    } else {
        currentSort.key = key;
        currentSort.asc = key === 'name' ? true : false; // Default descending for scores
    }

    const sorted = [...managers].sort((a, b) => {
        let va, vb;
        if (key === 'name') {
            va = a.name; vb = b.name;
            return currentSort.asc ? va.localeCompare(vb) : vb.localeCompare(va);
        }
        va = a[key]; vb = b[key];
        return currentSort.asc ? va - vb : vb - va;
    });

    // Update sorted class
    document.querySelectorAll('#rankings-table thead th').forEach(th => {
        th.classList.toggle('sorted', th.dataset.sort === key);
    });

    renderTable(sorted);
}

// ==================== MANAGER CARDS ====================

function renderCards(managers) {
    const grid = document.getElementById('cards-grid');
    grid.innerHTML = managers.map(m => `
        <div class="manager-card fade-in" onclick="scrollToDetail('${m.slug}')">
            <div class="card-header">
                <div>
                    <div class="card-name">${m.name}</div>
                    <div class="card-tagline">${m.narrative?.tagline || ''}</div>
                </div>
                <div class="card-score">${m.final_score.toFixed(1)}</div>
            </div>
            <div class="card-radar">
                <canvas id="radar-${m.slug}"></canvas>
            </div>
            <div class="card-meta">
                <span>#${m.rank} &middot; ${m.current_club}</span>
                <span>${m.available ? 'Available' : 'Unavailable'}</span>
            </div>
        </div>
    `).join('');

    // Create radar charts after DOM is ready
    requestAnimationFrame(() => {
        managers.forEach(m => {
            createRadarChart(`radar-${m.slug}`, m, { labelSize: 9 });
        });
    });
}

// ==================== DETAILED PROFILES ====================

function renderDetails(managers) {
    const container = document.getElementById('details-container');
    container.innerHTML = managers.map(m => {
        const verdictClass = getVerdictClass(m.narrative?.verdict);
        const peerCats = m.peer_categories || {};
        const fitCats = m.fit_categories || {};

        // Score bars for peer categories
        const peerBars = Object.entries(peerCats).map(([cat, val]) => `
            <div class="score-bar-container">
                <div class="score-bar-label">
                    <span>${CATEGORY_LABELS[cat] || cat}</span>
                    <span>${val.toFixed(1)}</span>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" data-width="${val * 10}%" style="width:0;"></div>
                </div>
            </div>
        `).join('');

        // Fit category bars
        const fitBars = Object.entries(fitCats).map(([cat, val]) => `
            <div class="score-bar-container">
                <div class="score-bar-label">
                    <span>${cat.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}</span>
                    <span>${val.toFixed(1)}/25</span>
                </div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" data-width="${val * 4}%" style="width:0;"></div>
                </div>
            </div>
        `).join('');

        const strengths = (m.narrative?.strengths || []).map(s => `<li>${s}</li>`).join('');
        const concerns = (m.narrative?.concerns || []).map(c => `<li>${c}</li>`).join('');

        return `
            <div class="detail-section fade-in" id="detail-${m.slug}">
                <div class="detail-header">
                    <div>
                        <div class="detail-name">${m.name}</div>
                        <div style="color:var(--spurs-teal);font-style:italic;">${m.narrative?.tagline || ''}</div>
                        <div style="color:var(--text-muted);font-size:0.85rem;margin-top:0.25rem;">
                            ${m.current_club} &middot; Age ${m.age} &middot; ${m.nationality}
                        </div>
                    </div>
                    <div class="detail-scores">
                        <div class="detail-score-box">
                            <div class="detail-score-value count-up" data-target="${m.final_score}" data-decimals="1">0.0</div>
                            <div class="detail-score-label">Final</div>
                        </div>
                        <div class="detail-score-box">
                            <div class="detail-score-value count-up" data-target="${m.peer_score}" data-decimals="1">0.0</div>
                            <div class="detail-score-label">Peer</div>
                        </div>
                        <div class="detail-score-box">
                            <div class="detail-score-value count-up" data-target="${m.fit_index}" data-decimals="0">0</div>
                            <div class="detail-score-label">Fit</div>
                        </div>
                        <div class="detail-score-box">
                            <div class="detail-score-value count-up" data-target="${m.potential_index}" data-decimals="0">0</div>
                            <div class="detail-score-label">Potential</div>
                        </div>
                    </div>
                </div>

                <div class="detail-body">
                    <div>
                        <div class="detail-narrative">${m.narrative?.summary || ''}</div>

                        <h4 style="margin-top:1.5rem;margin-bottom:0.5rem;font-size:0.9rem;">Strengths</h4>
                        <ul class="strengths-list">${strengths}</ul>

                        <h4 style="margin-top:1rem;margin-bottom:0.5rem;font-size:0.9rem;">Concerns</h4>
                        <ul class="concerns-list">${concerns}</ul>

                        <div class="detail-verdict ${verdictClass}" style="margin-top:1.5rem;">
                            ${m.narrative?.verdict || 'UNDER EVALUATION'}
                        </div>
                    </div>
                    <div>
                        <h4 style="margin-bottom:0.75rem;font-size:0.9rem;">Peer Analysis (0-10)</h4>
                        ${peerBars}

                        <h4 style="margin-top:1.5rem;margin-bottom:0.75rem;font-size:0.9rem;">Spurs-Fit Index (0-25 each)</h4>
                        ${fitBars}
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function getVerdictClass(verdict) {
    if (!verdict) return 'verdict-outsider';
    const v = verdict.toUpperCase();
    if (v.includes('STRONGLY')) return 'verdict-strong';
    if (v.includes('RECOMMENDED')) return 'verdict-recommended';
    if (v.includes('CAUTION') || v.includes('RESERVATION')) return 'verdict-caution';
    return 'verdict-outsider';
}

function scrollToDetail(slug) {
    const el = document.getElementById(`detail-${slug}`);
    if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Flash highlight
        el.style.borderColor = 'var(--spurs-teal)';
        el.style.boxShadow = '0 0 20px rgba(80, 227, 194, 0.2)';
        setTimeout(() => {
            el.style.borderColor = '';
            el.style.boxShadow = '';
        }, 1500);
    }
}

// ==================== INIT ====================
document.addEventListener('DOMContentLoaded', init);
