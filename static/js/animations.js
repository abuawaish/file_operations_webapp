// animations.js - Enhanced animations for the file operations system

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations
    initFloatingShapes();
    initHoverEffects();
    initScrollAnimations();
    initButtonRippleEffects();
    initParallaxEffect();
});

// Floating background shapes animation
function initFloatingShapes() {
    const shapes = document.querySelectorAll('.shape');
    shapes.forEach(shape => {
        const speed = Math.random() * 20 + 10;
        const direction = Math.random() > 0.5 ? 1 : -1;

        shape.style.animation = `float ${speed}s infinite linear ${direction > 0 ? 'normal' : 'reverse'}`;
    });
}

// Enhanced hover effects
function initHoverEffects() {
    const cards = document.querySelectorAll('.card, .operation-card, .action-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1)';
        });
    });
}

// Scroll animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated');

                // Add different animations based on element type
                if (entry.target.classList.contains('card')) {
                    entry.target.classList.add('animate__fadeInUp');
                } else if (entry.target.classList.contains('btn')) {
                    entry.target.classList.add('animate__pulse');
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with data-animate attribute
    document.querySelectorAll('[data-animate]').forEach(el => {
        observer.observe(el);
    });
}

// Button ripple effects
function initButtonRippleEffects() {
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Parallax effect for background
function initParallaxEffect() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const shapes = document.querySelectorAll('.shape');

        shapes.forEach((shape, index) => {
            const speed = 0.5 + (index * 0.1);
            const yPos = -(scrolled * speed);
            shape.style.transform = `translateY(${yPos}px) ${shape.style.transform}`;
        });
    });
}

// Typing animation for text
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Confetti effect for success
function showConfetti() {
    const confettiCount = 100;
    const confettiContainer = document.createElement('div');
    confettiContainer.style.position = 'fixed';
    confettiContainer.style.top = '0';
    confettiContainer.style.left = '0';
    confettiContainer.style.width = '100%';
    confettiContainer.style.height = '100%';
    confettiContainer.style.pointerEvents = 'none';
    confettiContainer.style.zIndex = '9999';
    document.body.appendChild(confettiContainer);

    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.position = 'absolute';
        confetti.style.width = '10px';
        confetti.style.height = '10px';
        confetti.style.backgroundColor = getRandomColor();
        confetti.style.borderRadius = '50%';
        confetti.style.left = `${Math.random() * 100}vw`;
        confetti.style.top = '-10px';
        confetti.style.opacity = '0.8';
        confettiContainer.appendChild(confetti);

        // Animate confetti
        const animation = confetti.animate([
            { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
            { transform: `translateY(${window.innerHeight}px) rotate(${360 + Math.random() * 360}deg)`, opacity: 0 }
        ], {
            duration: 1000 + Math.random() * 2000,
            easing: 'cubic-bezier(0.215, 0.61, 0.355, 1)'
        });

        animation.onfinish = () => confetti.remove();
    }

    // Remove container after animation
    setTimeout(() => {
        confettiContainer.remove();
    }, 3000);
}

function getRandomColor() {
    const colors = [
        '#667eea', '#764ba2', '#f093fb', '#f5576c',
        '#43e97b', '#38f9d7', '#fa709a', '#fee140',
        '#f6d365', '#fda085', '#4facfe', '#00f2fe'
    ];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Export functions for use in templates
window.Animations = {
    showConfetti,
    typeWriter,
    initFloatingShapes,
    initHoverEffects
};

// Add CSS for ripple effect
const style = document.createElement('style');
style.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    }

    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);