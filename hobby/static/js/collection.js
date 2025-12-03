// Инициализация сохраненных хобби из localStorage
let savedHobbies = JSON.parse(localStorage.getItem('savedHobbies')) || [];

// Функция сохранения/удаления хобби
function toggleSaveHobby(ideaId, ideaData) {
    // Проверяем, сохранено ли уже это хобби
    const isSaved = savedHobbies.some(hobby => hobby.id === ideaId);

    if (isSaved) {
        // Удаляем из сохраненных
        savedHobbies = savedHobbies.filter(hobby => hobby.id !== ideaId);
        showNotification('Хобби удалено из коллекции', 'info');
    } else {
        // Добавляем в сохраненные
        savedHobbies.push({
            id: ideaId,
            title: ideaData.title,
            category: ideaData.category,
            description: ideaData.description,
            time_required: ideaData.time_required,
            budget: ideaData.budget,
            location: ideaData.location,
            difficulty: ideaData.difficulty,
            votes: ideaData.votes || 0,
            created_at: ideaData.created_at || new Date().toLocaleDateString('ru-RU')
        });
        showNotification('Хобби добавлено в коллекцию!', 'success');
    }

    // Сохраняем в localStorage
    localStorage.setItem('savedHobbies', JSON.stringify(savedHobbies));

    // Обновляем отображение кнопок сохранения на всех страницах
    updateAllSaveButtons();

    // Если мы на странице коллекции, обновляем ее
    if (window.location.pathname === '/collection') {
        loadCollectionFromStorage();
    }
}

// Функция для кнопок "Сохранить" на всех страницах
function initializeSaveButtons() {
    // Обработчики для карточек на главной странице
    document.querySelectorAll('.idea-card .btn-action').forEach(button => {
        if (button.innerHTML.includes('Сохранить') || button.innerHTML.includes('fa-bookmark')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const ideaCard = this.closest('.idea-card');
                const ideaId = ideaCard.dataset.id ||
                              Array.from(document.querySelectorAll('.idea-card')).indexOf(ideaCard) + 1;

                // Собираем данные об идее
                const ideaData = {
                    title: ideaCard.querySelector('h4').textContent,
                    category: ideaCard.querySelector('.idea-category').textContent,
                    description: ideaCard.querySelector('.idea-description').textContent.replace('...', ''),
                    time_required: getTimeValue(ideaCard),
                    budget: getBudgetValue(ideaCard),
                    location: getLocationValue(ideaCard),
                    difficulty: 'medium' // По умолчанию
                };

                toggleSaveHobby(ideaId, ideaData);
                updateButtonState(this, ideaId);
            });
        }
    });

    // Обработчики для страницы генератора
    const generateSaveBtn = document.querySelector('.btn-action[onclick*="addToMyIdeas"]');
    if (generateSaveBtn) {
        const originalOnClick = generateSaveBtn.getAttribute('onclick');
        generateSaveBtn.removeAttribute('onclick');
        generateSaveBtn.addEventListener('click', function() {
            // Получаем данные идеи со страницы
            const ideaData = {
                title: document.querySelector('.idea-title').textContent,
                category: document.querySelector('.idea-category').textContent,
                description: document.querySelector('.idea-description p').textContent,
                time_required: document.querySelector('.meta-item:nth-child(1)').textContent.replace('До 1 часа', 'short').replace('1-3 часа', 'medium').replace('Более 3 часов', 'long'),
                budget: document.querySelector('.meta-item:nth-child(2)').textContent.replace('Бесплатно', 'free').replace('Низкий', 'low').replace('Средний', 'medium').replace('Высокий', 'high'),
                location: document.querySelector('.meta-item:nth-child(3)').textContent.replace('Дома', 'indoor').replace('На улице', 'outdoor').replace('Любое', 'both'),
                difficulty: document.querySelector('.meta-item:nth-child(4)').textContent.replace('Легкая', 'easy').replace('Средняя', 'medium').replace('Сложная', 'hard'),
                votes: parseInt(document.querySelector('.idea-votes').textContent) || 0
            };

            const ideaId = Date.now(); // Уникальный ID
            toggleSaveHobby(ideaId, ideaData);
        });
    }
}

// Вспомогательные функции для получения значений
function getTimeValue(card) {
    const timeText = card.querySelector('.idea-meta span:nth-child(1)').textContent;
    if (timeText.includes('До 1 часа')) return 'short';
    if (timeText.includes('1-3 часа')) return 'medium';
    if (timeText.includes('Более 3 часов')) return 'long';
    return 'medium';
}

function getBudgetValue(card) {
    const budgetText = card.querySelector('.idea-meta span:nth-child(2)').textContent;
    if (budgetText.includes('Бесплатно')) return 'free';
    if (budgetText.includes('Низкий')) return 'low';
    if (budgetText.includes('Средний')) return 'medium';
    if (budgetText.includes('Высокий')) return 'high';
    return 'low';
}

function getLocationValue(card) {
    const locationText = card.querySelector('.idea-meta span:nth-child(3)').textContent;
    if (locationText.includes('Дома')) return 'indoor';
    if (locationText.includes('На улице')) return 'outdoor';
    if (locationText.includes('Любое')) return 'both';
    return 'indoor';
}

// Обновление состояния кнопок сохранения
function updateAllSaveButtons() {
    // На главной странице
    document.querySelectorAll('.idea-card').forEach(card => {
        const ideaId = card.dataset.id ||
                      Array.from(document.querySelectorAll('.idea-card')).indexOf(card) + 1;
        const saveButton = card.querySelector('.btn-action[onclick*="addToMyIdeas"], .btn-action:has(.fa-bookmark)');

        if (saveButton) {
            updateButtonState(saveButton, ideaId);
        }
    });
}

function updateButtonState(button, ideaId) {
    const isSaved = savedHobbies.some(hobby => hobby.id === ideaId);

    if (isSaved) {
        button.innerHTML = '<i class="fas fa-bookmark"></i> В коллекции';
        button.classList.add('saved');
    } else {
        button.innerHTML = '<i class="far fa-bookmark"></i> Сохранить';
        button.classList.remove('saved');
    }
}

// Загрузка коллекции на странице коллекции
function loadCollectionFromStorage() {
    const savedHobbiesGrid = document.getElementById('saved-hobbies-grid');
    const emptyCollection = document.getElementById('empty-collection');

    if (!savedHobbiesGrid || !emptyCollection) return;

    // Очищаем сетку
    savedHobbiesGrid.innerHTML = '';

    if (savedHobbies.length === 0) {
        emptyCollection.style.display = 'block';
        savedHobbiesGrid.style.display = 'none';
        return;
    }

    emptyCollection.style.display = 'none';
    savedHobbiesGrid.style.display = 'grid';

    // Добавляем сохраненные хобби в сетку
    savedHobbies.forEach((hobby, index) => {
        const ideaCard = document.createElement('div');
        ideaCard.className = 'idea-card';
        ideaCard.dataset.id = hobby.id;

        // Форматируем время
        const timeText = hobby.time_required === 'short' ? 'До 1 часа' :
                        hobby.time_required === 'medium' ? '1-3 часа' :
                        hobby.time_required === 'long' ? 'Более 3 часов' : hobby.time_required;

        // Форматируем бюджет
        const budgetText = hobby.budget === 'free' ? 'Бесплатно' :
                          hobby.budget === 'low' ? 'Низкий' :
                          hobby.budget === 'medium' ? 'Средний' :
                          hobby.budget === 'high' ? 'Высокий' : hobby.budget;

        // Форматируем место
        const locationText = hobby.location === 'indoor' ? 'Дома' :
                            hobby.location === 'outdoor' ? 'На улице' :
                            hobby.location === 'both' ? 'Любое' : hobby.location;

        ideaCard.innerHTML = `
            <div class="idea-category">${hobby.category}</div>
            <h4>${hobby.title}</h4>
            <p class="idea-meta">
                <span><i class="fas fa-clock"></i> ${timeText}</span>
                <span><i class="fas fa-wallet"></i> ${budgetText}</span>
                <span><i class="fas fa-map-marker-alt"></i> ${locationText}</span>
            </p>
            <p class="idea-description">${hobby.description.substring(0, 150)}${hobby.description.length > 150 ? '...' : ''}</p>
            <div class="idea-actions">
                <button onclick="removeFromCollection(${hobby.id})" class="btn-action small saved">
                    <i class="fas fa-trash"></i> Удалить
                </button>
            </div>
        `;

        savedHobbiesGrid.appendChild(ideaCard);
    });
}

// Удаление из коллекции
function removeFromCollection(ideaId) {
    savedHobbies = savedHobbies.filter(hobby => hobby.id !== ideaId);
    localStorage.setItem('savedHobbies', JSON.stringify(savedHobbies));
    showNotification('Идея удалена из коллекции', 'info');
    loadCollectionFromStorage();
}

// Показ уведомлений
function showNotification(message, type = 'info') {
    // Создаем элемент уведомления
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;

    const icons = {
        'success': 'fa-check-circle',
        'info': 'fa-info-circle',
        'warning': 'fa-exclamation-triangle'
    };

    notification.innerHTML = `
        <div class="notification-icon">
            <i class="fas ${icons[type] || 'fa-info-circle'}"></i>
        </div>
        <div class="notification-content">
            <p>${message}</p>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;

    // Добавляем на страницу
    document.body.appendChild(notification);

    // Показываем с анимацией
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Автоматическое скрытие
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeSaveButtons();
    updateAllSaveButtons();

    // Если мы на странице коллекции, загружаем ее
    if (window.location.pathname === '/collection') {
        loadCollectionFromStorage();
    }
});
