document.addEventListener('DOMContentLoaded', function() {
    const ratingForms = document.querySelectorAll('#rating-form');
    
    ratingForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const materialId = this.action.split('/').pop();
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrf_token')
                }
            })
            .then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    alert('Произошла ошибка при сохранении оценки');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при сохранении оценки');
            });
        });
    });
}); 