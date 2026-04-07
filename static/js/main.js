// Modern JavaScript for PlantCare Application
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initScrollAnimations();
    initImageHandling();
    initFilterEnhancements();
    initSmoothScrolling();
    initCardAnimations();
    initTabs();
    initFilterCheckboxPills();
});

// Navigation Enhancement
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navOverlay = document.getElementById('navOverlay');
    const navbar = document.querySelector('.navbar');

    // Mobile overlay menu toggle
    if (hamburger && navOverlay) {
        hamburger.addEventListener('click', function() {
            const isOpen = navOverlay.classList.toggle('open');
            hamburger.classList.toggle('active', isOpen);
            navOverlay.setAttribute('aria-hidden', String(!isOpen));
            document.body.style.overflow = isOpen ? 'hidden' : '';
            hamburger.setAttribute('aria-expanded', String(isOpen));
        });

        // Close when overlay links clicked
        navOverlay.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navOverlay.classList.remove('open');
                hamburger.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // Navbar scroll effect - Fixed
    if (navbar) {
        let lastScrollY = window.scrollY;
        let ticking = false;
        
        function updateNavbar() {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
            
            // Only hide navbar when scrolling down past hero section
            const filterBar = document.querySelector('.filter-bar');
            if (currentScrollY > lastScrollY && currentScrollY > 400) {
                navbar.classList.add('hidden');
                if (filterBar) filterBar.style.top = '0px';
            } else {
                navbar.classList.remove('hidden');
                if (filterBar) filterBar.style.top = 'var(--nav-h)';
            }
            
            lastScrollY = currentScrollY;
            ticking = false;
        }
        
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateNavbar);
                ticking = true;
            }
        });
    }
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                
                // Stagger animations for cards
                if (entry.target.classList.contains('plant-card') || 
                    entry.target.classList.contains('feature-card')) {
                    const delay = Array.from(entry.target.parentNode.children).indexOf(entry.target) * 100;
                    entry.target.style.animationDelay = `${delay}ms`;
                }
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll(`
        .feature-card,
        .plant-card,
        .care-section,
        .hero-content,
        .section-title
    `);

    animateElements.forEach(el => {
        el.classList.add('animate-on-scroll');
        observer.observe(el);
    });
}

// Enhanced Image Handling
function initImageHandling() {
    // Lazy loading for images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Add loading class
                    img.classList.add('loading');
                    
                    // Load image
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    
                    img.addEventListener('load', () => {
                        img.classList.remove('lazy', 'loading');
                        img.classList.add('loaded');
                    });
                    
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Image error handling with retry
    document.querySelectorAll('img').forEach(img => {
        let retryCount = 0;
        const maxRetries = 2;
        
        function handleImageError() {
            if (retryCount < maxRetries) {
                retryCount++;
                setTimeout(() => {
                    img.src = img.src + '?retry=' + retryCount;
                }, 1000 * retryCount);
            } else {
                // Show placeholder after max retries
                img.style.display = 'none';
                const placeholder = img.parentElement.querySelector('.plant-placeholder, .plant-placeholder-large');
                if (placeholder) {
                    placeholder.style.display = 'flex';
                    placeholder.classList.add('error-state');
                }
            }
        }
        
        img.addEventListener('error', handleImageError);
        
        img.addEventListener('load', function() {
            // Hide placeholder when image loads successfully
            const placeholder = this.parentElement.querySelector('.plant-placeholder, .plant-placeholder-large');
            if (placeholder) {
                placeholder.style.display = 'none';
            }
            this.classList.add('loaded');
        });
    });
}

// Filter Enhancements
function initFilterEnhancements() {
    const filterForm = document.querySelector('.filters-form');
    const searchInput = document.querySelector('.search-input');
    const filterSelects = document.querySelectorAll('.filter-select');
    const filterCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    
    if (!filterForm) return;

    // Search input enhancements
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const searchBtn = document.querySelector('.search-btn');
            
            if (searchBtn) {
                searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            }
            
            searchTimeout = setTimeout(() => {
                if (searchBtn) {
                    searchBtn.innerHTML = '<i class="fas fa-search"></i>';
                }
            }, 500);
        });

        // Search suggestions (if you want to add this feature later)
        searchInput.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        searchInput.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    }

    // Filter change animations
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            this.classList.add('changed');
            setTimeout(() => {
                this.classList.remove('changed');
            }, 300);
        });
    });

    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.closest('.checkbox-label');
            if (label) {
                label.classList.toggle('checked', this.checked);
            }
        });
    });

    // Filter results counter animation
    const resultsInfo = document.querySelector('.results-info');
    if (resultsInfo) {
        const observer = new MutationObserver(() => {
            resultsInfo.classList.add('updated');
            setTimeout(() => {
                resultsInfo.classList.remove('updated');
            }, 300);
        });
        
        observer.observe(resultsInfo, { childList: true, subtree: true });
    }
}

// Smooth Scrolling
function initSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}


// Tab switching for plant detail page
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    if (!tabBtns.length) return;

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.dataset.tab;

            // Update buttons
            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            this.classList.add('active');
            this.setAttribute('aria-selected', 'true');

            // Update panels
            document.querySelectorAll('.tab-panel').forEach(panel => {
                panel.classList.remove('active');
            });
            const target = document.getElementById('tab-' + targetTab);
            if (target) target.classList.add('active');
        });
    });
}

// Filter checkbox pills — visual sync on page load
function initFilterCheckboxPills() {
    document.querySelectorAll('.filter-checkbox-pill input[type="checkbox"]').forEach(cb => {
        const pill = cb.closest('.filter-checkbox-pill');
        // Sync checked state (already done via Django template class, this covers edge cases)
        cb.addEventListener('change', function() {
            pill.classList.toggle('checked', this.checked);
        });
    });
}

// Card Animations
function initCardAnimations() {
    const cards = document.querySelectorAll('.plant-card, .feature-card');
    
    cards.forEach(card => {
        // Hover effect enhancements
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Click ripple effect
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            ripple.classList.add('ripple');
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Performance optimizations
const debouncedResize = debounce(() => {
    // Handle resize events
    window.dispatchEvent(new Event('optimizedResize'));
}, 250);

window.addEventListener('resize', debouncedResize);

// Preload critical images
function preloadImages() {
    const criticalImages = [
        // Add URLs of critical images here
    ];
    
    criticalImages.forEach(src => {
        const img = new Image();
        img.src = src;
    });
}

// Initialize preloading
preloadImages();

// Add CSS for additional animations
const additionalStyles = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(163, 163, 128, 0.25);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .changed {
        animation: highlight 0.3s ease;
    }
    
    @keyframes highlight {
        0% { background-color: var(--soft-accent); }
        100% { background-color: transparent; }
    }
    
    .updated {
        animation: bounce 0.3s ease;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .error-state {
        background: linear-gradient(135deg, #F2F8F2, #E4EEE4) !important;
    }
    
    .error-state i {
        color: #B85C5C !important;
    }
    
    .loading-shimmer {
        background: linear-gradient(90deg, #F5F3E6 25%, #E8E4D4 50%, #F5F3E6 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Export functions for potential external use
window.PlantCareApp = {
    initNavigation,
    initScrollAnimations,
    initImageHandling,
    initFilterEnhancements,
    debounce,
    throttle
};
// Stats Counter Animation
function initStatsCounter() {
    const statItems = document.querySelectorAll('.stat-item');
    
    if (statItems.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumber = entry.target.querySelector('.stat-number');
                const finalNumber = parseInt(statNumber.textContent);
                
                // Animate counter
                animateCounter(statNumber, 0, finalNumber, 1500);
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    statItems.forEach(item => observer.observe(item));
}

function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    const suffix = element.textContent.replace(/[0-9]/g, '');
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (end - start) * easeOutQuart);
        
        element.textContent = current + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = end + suffix;
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Enhanced Image Loading with Blur Effect
function initAdvancedImageLoading() {
    const images = document.querySelectorAll('img[src]');
    
    images.forEach(img => {
        // Add blur effect while loading
        img.style.filter = 'blur(5px)';
        img.style.transition = 'filter 0.3s ease';
        
        if (img.complete) {
            img.style.filter = 'blur(0px)';
        } else {
            img.addEventListener('load', () => {
                img.style.filter = 'blur(0px)';
            });
        }
    });
}

// Particle Effect for Hero Section
function initParticleEffect() {
    const hero = document.querySelector('.hero');
    if (!hero || window.innerWidth < 768) return;
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '0.1';
    
    hero.appendChild(canvas);
    
    function resizeCanvas() {
        canvas.width = hero.offsetWidth;
        canvas.height = hero.offsetHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    const particles = [];
    const particleCount = 50;
    
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.size = Math.random() * 2 + 1;
            this.opacity = Math.random() * 0.5 + 0.2;
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            
            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }
        
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(163, 163, 128, ${this.opacity})`;
            ctx.fill();
        }
    }
    
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        
        requestAnimationFrame(animate);
    }
    
    animate();
}

// Enhanced Scroll Progress Indicator - REMOVED
// This was causing the line issue, so it's been removed

// Initialize new features
document.addEventListener('DOMContentLoaded', function() {
    initAdvancedImageLoading();
});

// Add CSS for enhanced animations
const enhancedStyles = `
    .animate-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .animate-on-scroll.animated {
        opacity: 1;
        transform: translateY(0);
    }
    
    .plant-card.animate-on-scroll {
        transform: translateY(30px) scale(0.95);
    }
    
    .plant-card.animate-on-scroll.animated {
        transform: translateY(0) scale(1);
    }
    
    .feature-card.animate-on-scroll {
        transform: translateY(30px) rotateX(10deg);
    }
    
    .feature-card.animate-on-scroll.animated {
        transform: translateY(0) rotateX(0deg);
    }
    
    @media (prefers-reduced-motion: reduce) {
        .animate-on-scroll {
            transition: none;
            opacity: 1;
            transform: none;
        }
    }
`;

const enhancedStyleSheet = document.createElement('style');
enhancedStyleSheet.textContent = enhancedStyles;
document.head.appendChild(enhancedStyleSheet);