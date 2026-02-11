/**
 * Animations module — scroll reveals and count-up numbers.
 */

function initAnimations() {
    // Scroll-triggered fade-in
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

    // Count-up animations for score elements
    const countObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                const target = parseFloat(entry.target.dataset.target);
                const decimals = entry.target.dataset.decimals ? parseInt(entry.target.dataset.decimals) : 1;
                countUp(entry.target, target, 1200, decimals);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.count-up').forEach(el => countObserver.observe(el));

    // Animate score bars
    const barObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fill = entry.target.querySelector('.score-bar-fill');
                if (fill) {
                    fill.style.width = fill.dataset.width;
                }
            }
        });
    }, { threshold: 0.3 });

    document.querySelectorAll('.score-bar-container').forEach(el => barObserver.observe(el));
}

function countUp(element, target, duration = 1200, decimals = 1) {
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = eased * target;
        element.textContent = current.toFixed(decimals);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target.toFixed(decimals);
        }
    }

    requestAnimationFrame(update);
}

/**
 * Stagger fade-in for a list of elements.
 */
function staggerFadeIn(elements, delay = 80) {
    elements.forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(15px)';
        el.style.transition = `opacity 0.4s ease ${i * delay}ms, transform 0.4s ease ${i * delay}ms`;
        requestAnimationFrame(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    });
}
