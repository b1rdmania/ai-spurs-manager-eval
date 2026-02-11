/**
 * Social card generation module.
 */

let currentManagers = [];

function initSocial(managers) {
    currentManagers = managers;
}

function generateShareCard() {
    const slug = document.getElementById('share-select').value;
    if (!slug) return;

    const manager = currentManagers.find(m => m.slug === slug);
    if (!manager) return;

    const card = document.getElementById('share-card-template');
    document.getElementById('share-card-name').textContent = manager.name;
    document.getElementById('share-card-tagline').textContent = manager.narrative?.tagline || '';
    document.getElementById('share-card-score').textContent = manager.final_score.toFixed(1);
    document.getElementById('share-card-peer').textContent = manager.peer_score.toFixed(1) + '/10';
    document.getElementById('share-card-fit').textContent = manager.fit_index.toFixed(0) + '/100';
    document.getElementById('share-card-potential').textContent = manager.potential_index.toFixed(0) + '/100';
    document.getElementById('share-card-verdict').textContent = manager.narrative?.verdict || '—';

    // Show the card
    card.classList.add('share-card-visible');
    card.style.display = 'flex';
    card.style.flexDirection = 'column';
    card.style.justifyContent = 'space-between';

    // Use html-to-image to generate PNG
    if (typeof htmlToImage !== 'undefined' && htmlToImage.toPng) {
        htmlToImage.toPng(card, {
            backgroundColor: '#132257',
            width: 600,
            height: 340,
            style: {
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
            }
        }).then(dataUrl => {
            // Show preview and download
            const wrapper = document.getElementById('share-card-wrapper');
            wrapper.innerHTML = `
                <div style="text-align:center;">
                    <img src="${dataUrl}" alt="Share card for ${manager.name}"
                         style="max-width:100%;border-radius:1rem;box-shadow:0 8px 30px rgba(0,0,0,0.3);margin-bottom:1rem;">
                    <br>
                    <a href="${dataUrl}" download="spurs-eval-${slug}.png"
                       class="share-btn" style="text-decoration:none;display:inline-block;">
                        Download PNG
                    </a>
                </div>
            `;
            card.style.display = 'none';
            card.classList.remove('share-card-visible');
        }).catch(err => {
            console.error('Share card generation failed:', err);
            card.style.display = 'none';
            card.classList.remove('share-card-visible');
        });
    } else {
        // Fallback: show the card inline
        const wrapper = document.getElementById('share-card-wrapper');
        const clone = card.cloneNode(true);
        clone.style.display = 'flex';
        clone.style.flexDirection = 'column';
        clone.style.justifyContent = 'space-between';
        clone.style.margin = '0 auto';
        clone.style.maxWidth = '100%';
        clone.classList.add('share-card-visible');
        wrapper.innerHTML = '';
        wrapper.appendChild(clone);
        card.style.display = 'none';
    }
}
