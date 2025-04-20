// Глобальные функции
function submitRating(materialId) {
    // Получаем выбранное значение рейтинга
    const selectedRating = document.querySelector('input[name="rating"]:checked');
    
    if (!selectedRating) {
        showNotification('Пожалуйста, выберите оценку', 'error');
        return;
    }

    const rating = parseInt(selectedRating.value);
    
    fetch(`/materials/${materialId}/rate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
        body: JSON.stringify({ rating: rating })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        // Обновляем отображение рейтинга
        updateRatingDisplay(materialId, data.average_rating, data.rating_count);
        
        // Показываем уведомление об успехе
        showNotification('Оценка успешно сохранена', 'success');
    })
    .catch(error => {
        console.error('Error submitting rating:', error);
        showNotification(error.message, 'error');
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Trigger animation
    requestAnimationFrame(() => {
        notification.style.animation = 'slideIn 0.3s ease forwards';
    });

    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function updateRatingDisplay(materialId, averageRating, ratingCount) {
    const displayContainer = document.querySelector('.rating-display');
    if (displayContainer) {
        // Обновляем звезды
        const stars = displayContainer.querySelectorAll('.star');
        stars.forEach((star, index) => {
            if (index < Math.floor(averageRating)) {
                star.style.color = '#ffd700';
            } else {
                star.style.color = '#ddd';
            }
        });

        // Обновляем текстовое отображение
        const avgRatingSpan = displayContainer.querySelector('.ms-2');
        const countSpan = displayContainer.querySelector('.rating-count');
        
        if (avgRatingSpan) {
            avgRatingSpan.textContent = averageRating.toFixed(1);
        }
        if (countSpan) {
            countSpan.textContent = `(${ratingCount} оценок)`;
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    const ratingStars = document.querySelectorAll('.rating-stars');
    
    ratingStars.forEach(container => {
        const stars = container.querySelectorAll('.star');
        const materialId = container.dataset.materialId;
        let currentRating = parseInt(container.dataset.currentRating) || 0;
        
        // Initial setup of stars
        updateStarsDisplay(stars, currentRating);
        
        stars.forEach((star, index) => {
            // Hover effects
            star.addEventListener('mouseenter', () => {
                updateStarsDisplay(stars, index + 1);
                animateStars(stars, index + 1);
            });
            
            star.addEventListener('mouseleave', () => {
                updateStarsDisplay(stars, currentRating);
                resetStarsAnimation(stars);
            });
            
            // Click handling
            star.addEventListener('click', async () => {
                const rating = index + 1;
                await submitRating(materialId, rating);
            });
        });
    });
    
    function updateStarsDisplay(stars, rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.add('active');
                star.style.color = '#FFD700';
                star.style.textShadow = '0 0 15px rgba(255, 215, 0, 0.7)';
            } else {
                star.classList.remove('active');
                star.style.color = '#ddd';
                star.style.textShadow = 'none';
            }
        });
    }
    
    function animateStars(stars, rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.style.transform = 'scale(1.2)';
                star.style.transition = 'all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
            }
        });
    }
    
    function resetStarsAnimation(stars) {
        stars.forEach(star => {
            star.style.transform = 'scale(1)';
        });
    }
    
    function celebrateRating(container) {
        const particles = document.createElement('div');
        particles.className = 'rating-particles';
        container.appendChild(particles);
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.className = 'rating-particle';
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.backgroundColor = getRandomColor();
            particles.appendChild(particle);
        }
        
        setTimeout(() => {
            particles.remove();
        }, 1000);
    }
    
    function getRandomColor() {
        const colors = ['#FFD700', '#FFA500', '#FF6B6B', '#4CAF50', '#64B5F6'];
        return colors[Math.floor(Math.random() * colors.length)];
    }
}); 