import random
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, session as flask_session, flash
from database import db
from models import Idea, DailyChallenge, UserIdea
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hobby_ideas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)

# Создание таблиц и начальных данных
with app.app_context():
    db.create_all()
    # Добавляем начальные идеи, если их нет
    if Idea.query.count() == 0:
        initial_ideas = [
            Idea(
                title="Нарисовать акварельный пейзаж",
                description="Возьмите акварельные краски и попробуйте нарисовать пейзаж за окном. Не стремитесь к идеалу - просто получайте удовольствие от процесса.",
                category="Творчество",
                time_required="medium",
                budget="low",
                location="indoor",
                difficulty="medium",
                votes=15,
                is_approved=True
            ),
            Idea(
                title="Прогулка с фотографией",
                description="Возьмите телефон или фотоаппарат и отправьтесь на прогулку. Сфотографируйте 10 интересных объектов в вашем районе.",
                category="Фотография",
                time_required="short",
                budget="free",
                location="outdoor",
                difficulty="easy",
                votes=22,
                is_approved=True
            ),

            # ... остальные идеи из предыдущего кода
        ]
        db.session.add_all(initial_ideas)
        db.session.commit()


# Функции-помощники
def get_filtered_ideas(filters):
    """Получение идей с учетом фильтров"""
    query = Idea.query.filter_by(is_approved=True)

    if filters.get('time'):
        query = query.filter_by(time_required=filters['time'])
    if filters.get('budget'):
        query = query.filter_by(budget=filters['budget'])
    if filters.get('location'):
        query = query.filter_by(location=filters['location'])
    if filters.get('category'):
        query = query.filter_by(category=filters['category'])
    if filters.get('difficulty'):
        query = query.filter_by(difficulty=filters['difficulty'])

    return query.all()


def get_daily_challenge():
    """Получение или создание ежедневного челленджа"""
    today = date.today()

    # Проверяем, есть ли челлендж на сегодня
    challenge = DailyChallenge.query.filter_by(date=today).first()

    if not challenge:
        # Выбираем случайную идею
        ideas = Idea.query.filter_by(is_approved=True).all()
        if ideas:
            random_idea = random.choice(ideas)
            challenge = DailyChallenge(date=today, idea_id=random_idea.id)
            db.session.add(challenge)
            db.session.commit()

    return challenge


@app.route('/')
def index():
    """Главная страница с популярными идеями"""
    # Получаем 12 самых популярных идей (было 4)
    popular_ideas = Idea.query.filter_by(is_approved=True) \
        .order_by(Idea.votes.desc()) \
        .limit(12) \
        .all()

    ideas_data = [idea.to_dict() for idea in popular_ideas]

    return render_template('index.html', popular_ideas=ideas_data)


# Маршрут для кнопки "Сообщество" - теперь это "Все идеи"
@app.route('/community')
def community():
    """Все одобренные идеи (ранее all_ideas)"""
    ideas = Idea.query.filter_by(is_approved=True).order_by(Idea.votes.desc()).all()
    ideas_data = [idea.to_dict() for idea in ideas]

    # Группируем по категориям для отображения
    categories = {}
    for idea in ideas_data:
        category = idea['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(idea)

    return render_template('ideas.html',
                           ideas=ideas_data,
                           categories=categories,
                           title="Все идеи сообщества")


# Маршрут для кнопки "Фильтры" - ведет на страницу генератора
@app.route('/filters')
def filters_page():
    """Страница фильтров (ведет на генератор)"""
    categories = db.session.query(Idea.category).filter_by(is_approved=True).distinct().all()
    categories = [c[0] for c in categories]

    return render_template('generate.html',
                           idea=None,
                           filters={},
                           categories=categories,
                           has_ideas=True)


# Маршрут для кнопки "Добавьте своё"
@app.route('/share')
def share():
    """Страница добавления идеи (то же что и add_idea)"""
    return render_template('add_idea.html')


# Генерация случайной идеи (обновленный маршрут)
@app.route('/generate', methods=['GET', 'POST'])
def generate_idea():
    """Генерация случайной идеи"""
    if request.method == 'POST':
        # Получаем фильтры из формы
        filters = {
            'time': request.form.get('time'),
            'budget': request.form.get('budget'),
            'location': request.form.get('location'),
            'category': request.form.get('category'),
            'difficulty': request.form.get('difficulty')
        }

        # Фильтруем None значения
        filters = {k: v for k, v in filters.items() if v}

        # Получаем отфильтрованные идеи
        filtered_ideas = get_filtered_ideas(filters)

        if not filtered_ideas:
            # Если нет идей по фильтрам, берем все
            filtered_ideas = Idea.query.filter_by(is_approved=True).all()

        if filtered_ideas:
            random_idea = random.choice(filtered_ideas)
            idea_data = random_idea.to_dict()

            # Сохраняем в сессии, если пользователь хочет добавить в коллекцию
            if 'user_session' not in flask_session:
                flask_session['user_session'] = str(uuid.uuid4())

            categories = db.session.query(Idea.category).filter_by(is_approved=True).distinct().all()
            categories = [c[0] for c in categories]

            return render_template('generate.html',
                                   idea=idea_data,
                                   filters=filters,
                                   categories=categories,
                                   has_ideas=True)
        else:
            categories = db.session.query(Idea.category).filter_by(is_approved=True).distinct().all()
            categories = [c[0] for c in categories]

            return render_template('generate.html',
                                   idea=None,
                                   filters=filters,
                                   categories=categories,
                                   has_ideas=False)

    # GET запрос - показать форму
    categories = db.session.query(Idea.category).filter_by(is_approved=True).distinct().all()
    categories = [c[0] for c in categories]

    return render_template('generate.html',
                           idea=None,
                           filters={},
                           categories=categories,
                           has_ideas=True)


# API для AJAX-генерации
@app.route('/api/generate_idea', methods=['POST'])
def api_generate_idea():
    """API для генерации идеи (для AJAX)"""
    filters = request.json.get('filters', {})
    filtered_ideas = get_filtered_ideas(filters)

    if not filtered_ideas:
        filtered_ideas = Idea.query.filter_by(is_approved=True).all()

    if filtered_ideas:
        random_idea = random.choice(filtered_ideas)
        return jsonify({
            'success': True,
            'idea': random_idea.to_dict()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Нет доступных идей'
        })


# Добавление в "Мои идеи"
@app.route('/add_to_my_ideas/<int:idea_id>', methods=['POST'])
def add_to_my_ideas(idea_id):
    """Добавление идеи в коллекцию пользователя"""
    if 'user_session' not in flask_session:
        flask_session['user_session'] = str(uuid.uuid4())

    # Проверяем, не добавлена ли уже эта идея
    existing = UserIdea.query.filter_by(
        idea_id=idea_id,
        user_session=flask_session['user_session']
    ).first()

    if not existing:
        user_idea = UserIdea(
            idea_id=idea_id,
            user_session=flask_session['user_session']
        )
        db.session.add(user_idea)
        db.session.commit()
        flash('Идея добавлена в вашу коллекцию!', 'success')
        return jsonify({'success': True, 'message': 'Идея добавлена в вашу коллекцию!'})

    return jsonify({'success': False, 'message': 'Эта идея уже в вашей коллекции'})


# "Мои идеи"
@app.route('/my_ideas')
def my_ideas():
    """Коллекция идей пользователя"""
    if 'user_session' not in flask_session:
        user_ideas = []
    else:
        user_ideas_records = UserIdea.query.filter_by(
            user_session=flask_session['user_session']
        ).order_by(UserIdea.added_at.desc()).all()

        user_ideas = [record.idea.to_dict() for record in user_ideas_records if record.idea.is_approved]

    return render_template('ideas.html', ideas=user_ideas, title="Мои идеи")


# Все идеи (для ссылки "Смотреть все идеи")
@app.route('/all_ideas')
def all_ideas():
    """Все одобренные идеи"""
    ideas = Idea.query.filter_by(is_approved=True).order_by(Idea.created_at.desc()).all()
    ideas_data = [idea.to_dict() for idea in ideas]

    return render_template('ideas.html',
                           ideas=ideas_data,
                           title="Все идеи")


# Голосование
@app.route('/vote/<int:idea_id>', methods=['POST'])
def vote_idea(idea_id):
    """Голосование за идею"""
    idea = Idea.query.get_or_404(idea_id)
    idea.votes += 1
    db.session.commit()

    return jsonify({'success': True, 'votes': idea.votes})


# Ежедневный челлендж (исправленный маршрут)
@app.route('/challenge')
def challenge():
    """Ежедневный челлендж"""
    challenge = get_daily_challenge()

    if challenge and challenge.idea:
        challenge_data = {
            'id': challenge.id,
            'date': challenge.date.strftime('%d.%m.%Y'),
            'idea': challenge.idea.to_dict(),
            'completed_count': challenge.completed_count
        }
        return render_template('challenge.html', challenge=challenge_data)
    else:
        return render_template('challenge.html', challenge=None)


# Отметка о выполнении челленджа
@app.route('/complete_challenge/<int:challenge_id>', methods=['POST'])
def complete_challenge(challenge_id):
    """Отметка о выполнении челленджа"""
    challenge = DailyChallenge.query.get_or_404(challenge_id)
    challenge.completed_count += 1
    db.session.commit()

    flash('Челлендж выполнен! Отличная работа!', 'success')
    return jsonify({'success': True, 'completed_count': challenge.completed_count})


# Добавление новой идеи
@app.route('/add_idea', methods=['GET', 'POST'])
def add_idea():
    """Добавление новой идеи пользователем"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        time_required = request.form.get('time_required')
        budget = request.form.get('budget')
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')

        if not all([title, description, category, time_required, budget, location, difficulty]):
            flash('Пожалуйста, заполните все поля', 'error')
            return render_template('add_idea.html')

        # Создаем новую идею
        new_idea = Idea(
            title=title[:100],
            description=description,
            category=category,
            time_required=time_required,
            budget=budget,
            location=location,
            difficulty=difficulty,
            is_approved=False  # Требует модерации
        )

        db.session.add(new_idea)
        db.session.commit()

        flash('Спасибо! Ваша идея отправлена на модерацию.', 'success')
        return render_template('add_idea.html')

    return render_template('add_idea.html')


# Статистика
@app.route('/stats')
def stats():
    """Статистика сайта"""
    total_ideas = Idea.query.filter_by(is_approved=True).count()
    total_votes = db.session.query(db.func.sum(Idea.votes)).scalar() or 0
    user_submitted = Idea.query.filter_by(is_approved=False).count()

    # Самые популярные категории
    from sqlalchemy import func
    popular_categories = db.session.query(
        Idea.category,
        func.count(Idea.id).label('count')
    ).filter_by(is_approved=True).group_by(Idea.category).order_by(func.count(Idea.id).desc()).limit(5).all()

    # Последние добавленные идеи
    recent_ideas = Idea.query.filter_by(is_approved=True).order_by(Idea.created_at.desc()).limit(5).all()

    stats_data = {
        'total_ideas': total_ideas,
        'total_votes': total_votes,
        'user_submitted': user_submitted,
        'popular_categories': popular_categories,
        'recent_ideas': [idea.to_dict() for idea in recent_ideas]
    }

    return render_template('stats.html', stats=stats_data)


# Новый маршрут для главной кнопки "Сгенерировать идею"
@app.route('/generate_random')
def generate_random():
    """Генерация полностью случайной идеи"""
    ideas = Idea.query.filter_by(is_approved=True).all()
    if ideas:
        random_idea = random.choice(ideas)
        return render_template('generate.html',
                               idea=random_idea.to_dict(),
                               filters={},
                               categories=[],
                               has_ideas=True)
    return redirect(url_for('generate_idea'))

@app.route('/collection')
def collection():
    """Страница коллекции пользователя"""
    return render_template('collection.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
