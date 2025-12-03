// Основные функции JavaScript

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов
    const animatedElements = document.querySelectorAll('.feature-card, .idea-card');

    animatedElements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';

        setTimeout(() => {
            element.style.transition = 'opacity 0.5s, transform 0.5s';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Обработка форм с подтверждением
    const forms = document.querySelectorAll('form[data-confirm]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.getAttribute('data-confirm');
            if (message && !confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Динамическое обновление счетчиков
    const voteButtons = document.querySelectorAll('.vote-btn');
    voteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const ideaId = this.dataset.id;
            const counter = document.querySelector(`.votes-count[data-id="${ideaId}"]`);

            if (counter) {
                let current = parseInt(counter.textContent);
                counter.textContent = current + 1;

                // Визуальная обратная связь
                this.innerHTML = '<i class="fas fa-check"></i> Голос учтен';
                this.disabled = true;
                this.classList.add('voted');
            }
        });
    });
});

// Функция для копирования текста
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Текст скопирован в буфер обмена!');
    }).catch(err => {
        console.error('Ошибка копирования: ', err);
    });
}

// Показ уведомлений
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// Фильтрация идей на клиенте (опционально)
function filterIdeas(filterType, value) {
    const ideaCards = document.querySelectorAll('.idea-card');

    ideaCards.forEach(card => {
        const cardValue = card.dataset[filterType];

        if (value === '' || cardValue === value) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Анимация загрузки
function showLoading(element) {
    const loader = document.createElement('div');
    loader.className = 'loading-spinner';
    loader.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

    element.innerHTML = '';
    element.appendChild(loader);
    element.style.textAlign = 'center';
    element.style.padding = '40px';
}