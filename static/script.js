// Student Records System - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function () {
    console.log('Student Records System loaded successfully!');

  // Form validation enhancement
    const studentForm = document.getElementById('studentForm');
    if (studentForm) {
        studentForm.addEventListener('submit', function (e) {
            const name = document.getElementById('name').value.trim();
            const studentNumber = document.getElementById('student_number').value.trim();

        if (!name || !studentNumber) {
            e.preventDefault();
            showToast('Please fill in all fields', 'error');
            return false;
        }

        if (name.length > 100) {
            e.preventDefault();
            showToast('Name is too long (maximum 100 characters)', 'error');
            return false;
        }

        if (studentNumber.length > 20) {
            e.preventDefault();
            showToast('Student number is too long (maximum 20 characters)', 'error');
            return false;
        }

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = 'Adding ...';
            submitBtn.disabled = true;

            // Re-enable button after 3 seconds in case submission fails
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 3000);
        });
    }

    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Enhanced delete confirmation
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const studentName = this.closest('.student-card').querySelector('.student-name').textContent;
            if (!confirm(`Are you sure you want to delete "${studentName}"? This action cannot be undone.`)) {
                e.preventDefault();
            }
        });
    });

    // Search functionality enhancement
    const searchInput = document.querySelector('input[name="query"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length >= 2 || this.value.length === 0) {
                    this.form.submit();
                }
            }, 500);
        });
    }

    // Add smooth animations to student cards
    const studentCards = document.querySelectorAll('.student-card');
    studentCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});    

    // Utility function to show toast messages
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${type === 'error' ? '#f72585' : '#4361ee'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
    `;

    document.body.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);

    // Animate out and remove after 4 seconds
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 4000);
}

// Keyboard shortcuts
document.addEventListener('keydown', function (e) {
    // Focus search input when pressing Ctrl+K or Cmd+K
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="query"]');
        if (searchInput) {
        searchInput.focus();
        }
    }

    // Focus name input when pressing Ctrl+N or Cmd+N
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        const nameInput = document.getElementById('name');
        if (nameInput) {
            nameInput.focus();
        }
    }
});
