# init_db.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Idea
from datetime import datetime

with app.app_context():
    # Удаляем все существующие идеи
    Idea.query.delete()

    # Добавляем новые идеи (упрощенный список из 30+ идей)
    ideas = [
        # ТВОРЧЕСТВО
        Idea(
            title="Рисование акварелью",
            description="Создайте акварельный пейзаж по видеоуроку",
            category="Творчество",
            time_required="medium",
            budget="low",
            location="indoor",
            difficulty="medium",
            votes=45,
            is_approved=True
        ),
        Idea(
            title="Каллиграфия для начинающих",
            description="Освойте искусство красивого письма",
            category="Творчество",
            time_required="short",
            budget="low",
            location="indoor",
            difficulty="easy",
            votes=38,
            is_approved=True
        ),
        Idea(
            title="Создание арт-дневника",
            description="Ведите дневник с рисунками и коллажами",
            category="Творчество",
            time_required="long",
            budget="low",
            location="indoor",
            difficulty="easy",
            votes=32,
            is_approved=True
        ),
        Idea(
            title="Лепка из полимерной глины",
            description="Создайте украшения из запекаемой глины",
            category="Творчество",
            time_required="long",
            budget="medium",
            location="indoor",
            difficulty="medium",
            votes=28,
            is_approved=True
        ),
        Idea(
            title="Скрапбукинг альбома",
            description="Оформите фотоальбом в технике скрапбукинг",
            category="Творчество",
            time_required="long",
            budget="medium",
            location="indoor",
            difficulty="medium",
            votes=34,
            is_approved=True
        ),

        # ФОТОГРАФИЯ
        Idea(
            title="Фотопрогулка по городу",
            description="Сфотографируйте 10 интересных мест",
            category="Фотография",
            time_required="medium",
            budget="free",
            location="outdoor",
            difficulty="easy",
            votes=52,
            is_approved=True
        ),
        Idea(
            title="Макросъемка природы",
            description="Снимите капли росы и насекомых крупным планом",
            category="Фотография",
            time_required="short",
            budget="free",
            location="outdoor",
            difficulty="medium",
            votes=41,
            is_approved=True
        ),
        Idea(
            title="Ночная съемка звезд",
            description="Запечатлейте ночное небо со штатива",
            category="Фотография",
            time_required="long",
            budget="low",
            location="outdoor",
            difficulty="hard",
            votes=35,
            is_approved=True
        ),

        # КУЛИНАРИЯ
        Idea(
            title="Приготовить домашнюю пиццу",
            description="Сделайте пиццу с любимыми начинками",
            category="Кулинария",
            time_required="medium",
            budget="low",
            location="indoor",
            difficulty="easy",
            votes=62,
            is_approved=True
        ),
        Idea(
            title="Испечь хлеб на закваске",
            description="Приготовьте домашний хлеб с нуля",
            category="Кулинария",
            time_required="long",
            budget="low",
            location="indoor",
            difficulty="hard",
            votes=47,
            is_approved=True
        ),
        Idea(
            title="Мастер-класс по суши",
            description="Научитесь готовить роллы дома",
            category="Кулинария",
            time_required="medium",
            budget="medium",
            location="indoor",
            difficulty="hard",
            votes=39,
            is_approved=True
        ),
        Idea(
            title="Дегустация чаев",
            description="Попробуйте разные сорта чая",
            category="Кулинария",
            time_required="short",
            budget="low",
            location="indoor",
            difficulty="easy",
            votes=43,
            is_approved=True
        ),

        # АКТИВНЫЙ ОТДЫХ
        Idea(
            title="Пикник в необычном месте",
            description="Организуйте пикник на крыше или у реки",
            category="Активный отдых",
            time_required="medium",
            budget="low",
            location="outdoor",
            difficulty="easy",
            votes=70,
            is_approved=True
        ),
        Idea(
            title="Велосипедная прогулка",
            description="Прокатитесь на велосипеде по парку",
            category="Активный отдых",
            time_required="medium",
            budget="free",
            location="outdoor",
            difficulty="easy",
            votes=56,
            is_approved=True
        ),
        Idea(
            title="Поход в горы",
            description="Однодневный поход в ближайшие горы",
            category="Активный отдых",
            time_required="long",
            budget="low",
            location="outdoor",
            difficulty="hard",
            votes=44,
            is_approved=True
        ),
        Idea(
            title="Йога в парке",
            description="Позанимайтесь йогой на свежем воздухе",
            category="Активный отдых",
            time_required="short",
            budget="free",
            location="outdoor",
            difficulty="medium",
            votes=52,
            is_approved=True
        ),

        # ЧТЕНИЕ
        Idea(
            title="Чтение книги в парке",
            description="Возьмите книгу и читайте на свежем воздухе",
            category="Чтение",
            time_required="long",
            budget="free",
            location="outdoor",
            difficulty="easy",
            votes=65,
            is_approved=True
        ),
        Idea(
            title="Аудиокниги на прогулке",
            description="Слушайте аудиокнигу во время ходьбы",
            category="Чтение",
            time_required="medium",
            budget="free",
            location="outdoor",
            difficulty="easy",
            votes=51,
            is_approved=True
        ),
        Idea(
            title="Создание книжного клуба",
            description="Организуйте клуб для обсуждения книг",
            category="Чтение",
            time_required="medium",
            budget="free",
            location="both",
            difficulty="easy",
            votes=37,
            is_approved=True
        ),

        # ПРИРОДА
        Idea(
            title="Создание гербария",
            description="Соберите и засушите листья для гербария",
            category="Природа",
            time_required="long",
            budget="low",
            location="both",
            difficulty="easy",
            votes=32,
            is_approved=True
        ),
        Idea(
            title="Наблюдение за птицами",
            description="Определите 5 видов птиц в парке",
            category="Природа",
            time_required="medium",
            budget="low",
            location="outdoor",
            difficulty="medium",
            votes=28,
            is_approved=True
        ),
        Idea(
            title="Фотографирование заката",
            description="Сделайте серию фото заката",
            category="Природа",
            time_required="short",
            budget="free",
            location="outdoor",
            difficulty="easy",
            votes=57,
            is_approved=True
        ),

        # ОБРАЗОВАНИЕ
        Idea(
            title="Изучение языка на Duolingo",
            description="Занимайтесь языком 30 минут в день",
            category="Образование",
            time_required="short",
            budget="free",
            location="indoor",
            difficulty="medium",
            votes=59,
            is_approved=True
        ),
        Idea(
            title="Онлайн-курс по программированию",
            description="Пройдите бесплатный курс Python",
            category="Образование",
            time_required="long",
            budget="free",
            location="indoor",
            difficulty="hard",
            votes=44,
            is_approved=True
        ),
        Idea(
            title="Изучение астрономии",
            description="Научитесь находить созвездия",
            category="Образование",
            time_required="short",
            budget="free",
            location="outdoor",
            difficulty="medium",
            votes=37,
            is_approved=True
        ),

        # РУКОДЕЛИЕ
        Idea(
            title="Вязание шарфа",
            description="Свяжите простой шарф спицами",
            category="Рукоделие",
            time_required="long",
            budget="low",
            location="indoor",
            difficulty="medium",
            votes=53,
            is_approved=True
        ),
        Idea(
            title="Изготовление свечей",
            description="Создайте ароматические свечи",
            category="Рукоделие",
            time_required="medium",
            budget="low",
            location="indoor",
            difficulty="easy",
            votes=46,
            is_approved=True
        ),
        Idea(
            title="Бисероплетение",
            description="Сделайте браслет из бисера",
            category="Рукоделие",
            time_required="medium",
            budget="low",
            location="indoor",
            difficulty="medium",
            votes=39,
            is_approved=True
        ),
        Idea(
            title="Изготовление мыла",
            description="Создайте мыло ручной работы",
            category="Рукоделие",
            time_required="medium",
            budget="medium",
            location="indoor",
            difficulty="medium",
            votes=42,
            is_approved=True
        ),

        # МУЗЫКА
        Idea(
            title="Игра на укулеле",
            description="Научитесь играть простые песни",
            category="Музыка",
            time_required="long",
            budget="medium",
            location="indoor",
            difficulty="hard",
            votes=29,
            is_approved=True
        ),
        Idea(
            title="Создание плейлистов",
            description="Составьте плейлисты для разных настроений",
            category="Музыка",
            time_required="short",
            budget="free",
            location="indoor",
            difficulty="easy",
            votes=44,
            is_approved=True
        ),

        # СПОРТ
        Idea(
            title="Тренировка дома",
            description="Сделайте комплекс упражнений с весом тела",
            category="Спорт",
            time_required="short",
            budget="free",
            location="indoor",
            difficulty="easy",
            votes=52,
            is_approved=True
        ),
        Idea(
            title="Йога для начинающих",
            description="20-минутный комплекс йоги",
            category="Спорт",
            time_required="short",
            budget="free",
            location="indoor",
            difficulty="easy",
            votes=58,
            is_approved=True
        ),
        Idea(
            title="Пробежка интервалами",
            description="Чередуйте бег и ходьбу",
            category="Спорт",
            time_required="short",
            budget="free",
            location="outdoor",
            difficulty="medium",
            votes=47,
            is_approved=True
        ),
    ]

    db.session.add_all(ideas)
    db.session.commit()
    print(f"✅ Добавлено {len(ideas)} идей в базу данных!")
    print("🎯 Теперь на главной странице показывается 12 самых популярных идей")