// Community Solver JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner me-2"></span>Processing...';
                submitBtn.disabled = true;
            }
        });
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .feature-card, .problem-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Add hover effects to interactive elements
    const interactiveElements = document.querySelectorAll('.btn, .card, .list-group-item');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('alert-dismissible')) {
                const closeBtn = alert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }
        }, 5000);
    });

    // Add smooth scrolling to anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add character counter for textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'form-text text-end';
            counter.innerHTML = `<span class="char-count">0</span>/${maxLength} characters`;
            textarea.parentNode.appendChild(counter);
            
            const charCount = counter.querySelector('.char-count');
            
            textarea.addEventListener('input', function() {
                const currentLength = this.value.length;
                charCount.textContent = currentLength;
                
                if (currentLength > maxLength * 0.9) {
                    charCount.style.color = '#dc3545';
                } else if (currentLength > maxLength * 0.8) {
                    charCount.style.color = '#fd7e14';
                } else {
                    charCount.style.color = '#6c757d';
                }
            });
        }
    });

    // Add form validation feedback
    const formInputs = document.querySelectorAll('.form-control, .form-select');
    formInputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.checkValidity()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            } else {
                this.classList.remove('is-valid');
                this.classList.add('is-invalid');
            }
        });
    });

    // Add loading animation to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.type === 'submit' || this.classList.contains('btn-primary')) {
                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.cssText = `
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.6);
                    transform: scale(0);
                    animation: ripple 0.6s linear;
                    pointer-events: none;
                `;
                
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = (event.clientX - rect.left - size / 2) + 'px';
                ripple.style.top = (event.clientY - rect.top - size / 2) + 'px';
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            }
        });
    });

    // Add CSS for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// API functions
async function fetchProblems() {
    try {
        const response = await fetch('/api/problems');
        const problems = await response.json();
        return problems;
    } catch (error) {
        console.error('Error fetching problems:', error);
        return [];
    }
}

async function voteSolution(solutionId) {
    try {
        const response = await fetch(`/vote_solution/${solutionId}`, {
            method: 'GET'
        });
        
        if (response.ok) {
            showNotification('Vote recorded successfully!', 'success');
            // Reload the page to show updated vote count
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showNotification('Error recording vote. Please try again.', 'danger');
        }
    } catch (error) {
        console.error('Error voting:', error);
        showNotification('Error recording vote. Please try again.', 'danger');
    }
}

// Chart helper functions
function createChart(canvasId, chartData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    return new Chart(ctx, chartData);
}

function updateChart(chart, newData) {
    if (chart && newData) {
        chart.data = newData.data;
        chart.options = newData.options;
        chart.update();
    }
}

// Search and filter functions
function filterProblems(category, severity) {
    const problemCards = document.querySelectorAll('.problem-card');
    
    problemCards.forEach(card => {
        const cardCategory = card.querySelector('.badge.bg-primary')?.textContent;
        const cardSeverity = card.querySelector('.badge.bg-danger, .badge.bg-warning, .badge.bg-info, .badge.bg-success')?.textContent;
        
        let showCard = true;
        
        if (category && category !== 'all' && cardCategory !== category) {
            showCard = false;
        }
        
        if (severity && severity !== 'all' && cardSeverity !== severity) {
            showCard = false;
        }
        
        card.style.display = showCard ? 'block' : 'none';
    });
}

// Export functions for global use
window.CommunitySolver = {
    showNotification,
    formatDate,
    formatDateTime,
    fetchProblems,
    voteSolution,
    createChart,
    updateChart,
    filterProblems
};
