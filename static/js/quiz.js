document.addEventListener('DOMContentLoaded', function() {
    // Enable form validation
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Add animation to quiz cards
    const quizCards = document.querySelectorAll('.quiz-card');
    quizCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('shadow');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('shadow');
        });
    });
    
    // Timer functionality for quiz pages
    const timerElement = document.getElementById('quiz-timer');
    if (timerElement) {
        let seconds = 0;
        
        setInterval(() => {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            
            timerElement.textContent = `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
        }, 1000);
    }
    
    // Enable tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
});
