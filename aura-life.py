"""
AURA LIFE OS - Streamlit Edition
Version 3.0 Cloud Ready

Pour lancer : streamlit run aura_streamlit.py
Déploiement : Streamlit Cloud, Railway, Render

pip install streamlit sqlalchemy plotly pandas
"""

import os
import datetime
import random
from typing import Optional

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG (doit être en premier)
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Aura Life OS",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    /* Dark theme enhancements */
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #111111 100%);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Cards */
    .css-1r6slb0, .css-12w0qpk {
        background-color: #1a1a1a;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Custom card */
    .aura-card {
        background: linear-gradient(135deg, #1a1a1a, #0d0d0d);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Hero card */
    .hero-card {
        background: linear-gradient(135deg, rgba(50,215,226,0.1), rgba(0,113,227,0.1));
        border: 1px solid rgba(50,215,226,0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    
    /* Progress bar custom */
    .stProgress > div > div {
        background: linear-gradient(90deg, #32d7e2, #0071e3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0a 0%, #050505 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* XP Badge */
    .xp-badge {
        background: linear-gradient(135deg, #ffd60a, #ff9f0a);
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    
    /* Level badge */
    .level-badge {
        background: linear-gradient(135deg, #bf5af2, #ff375f);
        color: #fff;
        padding: 8px 16px;
        border-radius: 50%;
        font-weight: 700;
        font-size: 1.5rem;
    }
    
    /* Skill card */
    .skill-card {
        background: #161616;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Achievement unlocked */
    .achievement-unlocked {
        background: linear-gradient(135deg, rgba(255,214,10,0.2), rgba(255,159,10,0.1));
        border: 1px solid rgba(255,214,10,0.3);
    }
    
    /* Habit item */
    .habit-item {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #32d7e2, #0071e3);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5ee3ec, #2196f3);
        transform: translateY(-2px);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 8px 16px;
    }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE SETUP (conservé de l'original)
# ══════════════════════════════════════════════════════════════════════════════

os.makedirs('data', exist_ok=True)
DATABASE_URL = "sqlite:///./data/aura_life.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ══════════════════════════════════════════════════════════════════════════════
# MODELS (conservés de l'original)
# ══════════════════════════════════════════════════════════════════════════════

class Investment(Base):
    __tablename__ = "investments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    category = Column(String(50))
    amount = Column(Float, default=0)
    current_value = Column(Float, default=0)
    yield_pct = Column(Float, default=0)
    icon = Column(String(50), default="chart-line")
    color = Column(String(20), default="cyan")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    notes = Column(Text, default="")

class EnergyLog(Base):
    __tablename__ = "energy_logs"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    level = Column(Integer)
    mood = Column(String(50))
    activity = Column(String(100))
    sleep_hours = Column(Float, default=0)
    notes = Column(Text, default="")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text, default="")
    status = Column(String(50), default="idea")
    priority = Column(Integer, default=5)
    category = Column(String(50), default="general")
    deadline = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    icon = Column(String(50), default="check")
    color = Column(String(20), default="emerald")
    frequency = Column(String(20), default="daily")
    streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    skill_target = Column(String(50), default="Discipline")
    xp_reward = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HabitLog(Base):
    __tablename__ = "habit_logs"
    id = Column(Integer, primary_key=True)
    habit_id = Column(Integer)
    completed_at = Column(Date, default=datetime.date.today)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    target_value = Column(Float)
    current_value = Column(Float, default=0)
    unit = Column(String(50), default="€")
    deadline = Column(Date, nullable=True)
    category = Column(String(50), default="finance")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserProfile(Base):
    __tablename__ = "user_profile"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), default="Voyageur")
    title = Column(String(100), default="Apprenti de la Vie")
    level = Column(Integer, default=1)
    total_xp = Column(Integer, default=0)
    character_class = Column(String(50), default="Explorateur")
    talent_points = Column(Integer, default=0)
    prestige_level = Column(Integer, default=0)
    prestige_bonus = Column(Integer, default=0)
    vision = Column(Text, default="")
    values = Column(Text, default="")
    rules = Column(Text, default="")
    chronotype = Column(String(30), default="")
    sleep_goal = Column(Float, default=8.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    icon = Column(String(30))
    color = Column(String(20))
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(200))
    icon = Column(String(30))
    unlocked = Column(Integer, default=0)
    unlocked_at = Column(DateTime, nullable=True)

class JournalEntry(Base):
    __tablename__ = "journal"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    mood = Column(String(30))
    tags = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class XPLog(Base):
    __tablename__ = "xp_logs"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    source = Column(String(100))
    skill_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    quest_type = Column(String(20))
    xp_reward = Column(Integer, default=50)
    skill_target = Column(String(50))
    target_value = Column(Integer, default=1)
    current_value = Column(Integer, default=0)
    completed = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SleepLog(Base):
    __tablename__ = "sleep_logs"
    id = Column(Integer, primary_key=True)
    date = Column(Date, default=datetime.date.today)
    bedtime = Column(String(10))
    waketime = Column(String(10))
    duration = Column(Float)
    quality = Column(Integer)
    deep_sleep = Column(Float, default=0)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    note_type = Column(String(50), default="free")
    linked_id = Column(Integer, nullable=True)
    tags = Column(String(300), default="")
    backlinks = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

# Créer les tables
Base.metadata.create_all(bind=engine)

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_db():
    """Retourne une session de base de données"""
    return SessionLocal()

def init_skills(db):
    """Initialise les compétences par défaut"""
    if db.query(Skill).count() == 0:
        default_skills = [
            {"name": "Discipline", "icon": "🛡️", "color": "blue"},
            {"name": "Focus", "icon": "🎯", "color": "purple"},
            {"name": "Énergie", "icon": "⚡", "color": "yellow"},
            {"name": "Créativité", "icon": "🎨", "color": "pink"},
            {"name": "Santé", "icon": "❤️", "color": "red"},
            {"name": "Social", "icon": "👥", "color": "cyan"},
            {"name": "Business", "icon": "💼", "color": "green"},
            {"name": "Intelligence", "icon": "🧠", "color": "orange"},
        ]
        for s in default_skills:
            db.add(Skill(**s))
        db.commit()

def init_profile(db):
    """Initialise le profil utilisateur"""
    if db.query(UserProfile).count() == 0:
        db.add(UserProfile())
        db.commit()

def init_achievements(db):
    """Initialise les achievements"""
    if db.query(Achievement).count() == 0:
        achievements = [
            {"name": "Premier Pas", "description": "Compléter ta première habitude", "icon": "🚩"},
            {"name": "Série de 7", "description": "Maintenir une habitude 7 jours", "icon": "🔥"},
            {"name": "Série de 30", "description": "Maintenir une habitude 30 jours", "icon": "🏆"},
            {"name": "Niveau 5", "description": "Atteindre le niveau 5", "icon": "⭐"},
            {"name": "Niveau 10", "description": "Atteindre le niveau 10", "icon": "👑"},
            {"name": "Millionnaire XP", "description": "Accumuler 10000 XP", "icon": "💎"},
            {"name": "Penseur", "description": "Écrire 10 entrées de journal", "icon": "📖"},
            {"name": "Maître Skill", "description": "Avoir une compétence niveau 10", "icon": "🏅"},
        ]
        for a in achievements:
            db.add(Achievement(**a))
        db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# GAMIFICATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def xp_for_level(level: int) -> int:
    """XP nécessaire pour atteindre un niveau"""
    return int(100 * (level ** 1.5))

def level_from_xp(xp: int) -> int:
    """Calcule le niveau à partir de l'XP total"""
    level = 1
    while xp >= xp_for_level(level + 1):
        level += 1
    return level

def get_title(level: int) -> str:
    """Titre basé sur le niveau"""
    titles = {
        1: "Apprenti de la Vie",
        5: "Explorateur",
        10: "Aventurier",
        15: "Guerrier du Quotidien",
        20: "Maître de Soi",
        25: "Sage",
        30: "Légende Vivante",
        40: "Architecte de Destin",
        50: "Transcendant"
    }
    for lvl in sorted(titles.keys(), reverse=True):
        if level >= lvl:
            return titles[lvl]
    return titles[1]

def award_xp(db, amount: int, source: str, skill_name: str = None):
    """Attribue de l'XP au profil et à une compétence"""
    profile = db.query(UserProfile).first()
    if not profile:
        init_profile(db)
        profile = db.query(UserProfile).first()
    
    old_level = profile.level
    profile.total_xp += amount
    profile.level = level_from_xp(profile.total_xp)
    profile.title = get_title(profile.level)
    
    if skill_name:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if skill:
            skill.xp += amount
            skill.level = level_from_xp(skill.xp)
    
    db.add(XPLog(amount=amount, source=source, skill_name=skill_name or ""))
    db.commit()
    
    return profile.level > old_level

def check_achievements(db):
    """Vérifie et débloque les achievements"""
    profile = db.query(UserProfile).first()
    habits = db.query(Habit).all()
    journal_count = db.query(JournalEntry).count()
    skills = db.query(Skill).all()
    
    unlocks = []
    checks = [
        ("Premier Pas", any(h.streak > 0 for h in habits)),
        ("Série de 7", any(h.best_streak >= 7 for h in habits)),
        ("Série de 30", any(h.best_streak >= 30 for h in habits)),
        ("Niveau 5", profile and profile.level >= 5),
        ("Niveau 10", profile and profile.level >= 10),
        ("Millionnaire XP", profile and profile.total_xp >= 10000),
        ("Penseur", journal_count >= 10),
        ("Maître Skill", any(s.level >= 10 for s in skills)),
    ]
    
    for name, condition in checks:
        if condition:
            ach = db.query(Achievement).filter(Achievement.name == name, Achievement.unlocked == 0).first()
            if ach:
                ach.unlocked = 1
                ach.unlocked_at = datetime.datetime.utcnow()
                unlocks.append(name)
    
    db.commit()
    return unlocks

def generate_daily_quests(db):
    """Génère les quêtes quotidiennes"""
    today = datetime.date.today()
    existing = db.query(Quest).filter(
        Quest.quest_type == "daily",
        Quest.created_at >= datetime.datetime.combine(today, datetime.time.min)
    ).count()
    
    if existing == 0:
        daily_quests = [
            {"title": "Lève-tôt", "description": "Logger ton énergie", "quest_type": "daily", "xp_reward": 30, "skill_target": "Énergie", "target_value": 1},
            {"title": "Triple Habitude", "description": "Compléter 3 habitudes", "quest_type": "daily", "xp_reward": 50, "skill_target": "Discipline", "target_value": 3},
            {"title": "Pensée du Jour", "description": "Écrire dans le journal", "quest_type": "daily", "xp_reward": 25, "skill_target": "Intelligence", "target_value": 1},
        ]
        tomorrow = datetime.datetime.combine(today + datetime.timedelta(days=1), datetime.time.min)
        for q in daily_quests:
            q["expires_at"] = tomorrow
            db.add(Quest(**q))
        db.commit()

def generate_weekly_quest(db):
    """Génère la quête boss hebdomadaire"""
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    existing = db.query(Quest).filter(
        Quest.quest_type == "boss",
        Quest.created_at >= datetime.datetime.combine(week_start, datetime.time.min)
    ).count()
    
    if existing == 0:
        bosses = [
            {"title": "🐉 Boss: Procrastination", "description": "Compléter 20 habitudes cette semaine", "xp_reward": 500, "skill_target": "Discipline", "target_value": 20},
            {"title": "🐉 Boss: Chaos Mental", "description": "Écrire 5 entrées journal", "xp_reward": 400, "skill_target": "Intelligence", "target_value": 5},
            {"title": "🐉 Boss: Fatigue", "description": "Logger 7 nuits de sommeil", "xp_reward": 450, "skill_target": "Santé", "target_value": 7},
        ]
        boss = random.choice(bosses)
        boss["quest_type"] = "boss"
        boss["expires_at"] = datetime.datetime.combine(week_start + datetime.timedelta(days=7), datetime.time.min)
        db.add(Quest(**boss))
        db.commit()

# ══════════════════════════════════════════════════════════════════════════════
# COACH IA
# ══════════════════════════════════════════════════════════════════════════════

def generate_coach_tips(db):
    """Génère des conseils personnalisés"""
    tips = []
    today = datetime.date.today()
    
    # Analyse des habitudes
    habits = db.query(Habit).all()
    uncompleted = sum(1 for h in habits if not db.query(HabitLog).filter(
        HabitLog.habit_id == h.id, HabitLog.completed_at == today).first())
    
    if uncompleted > 0:
        tips.append(f"🔥 Tu as {uncompleted} habitude(s) non complétée(s) aujourd'hui")
    
    # Analyse de l'énergie
    last_energy = db.query(EnergyLog).order_by(EnergyLog.id.desc()).first()
    if last_energy and last_energy.level < 5:
        tips.append("⚡ Ton niveau d'énergie est bas. Prends une pause !")
    
    # Analyse des projets
    active_projects = db.query(Project).filter(Project.status == "active").count()
    if active_projects > 5:
        tips.append(f"📋 Tu as {active_projects} projets actifs. Focus sur 2-3 max.")
    
    if not tips:
        tips.append("✨ Tu es sur la bonne voie ! Continue comme ça.")
    
    return tips

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar():
    """Affiche la sidebar de navigation"""
    with st.sidebar:
        st.markdown("# 🌟 Aura Life OS")
        st.markdown("---")
        
        # Profil rapide
        db = get_db()
        init_profile(db)
        profile = db.query(UserProfile).first()
        db.close()
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"### Nv.{profile.level}")
        with col2:
            st.markdown(f"**{profile.name}**")
            st.caption(f"{profile.total_xp} XP")
        
        # Barre de progression vers prochain niveau
        current_xp = profile.total_xp
        current_level_xp = xp_for_level(profile.level)
        next_level_xp = xp_for_level(profile.level + 1)
        progress = (current_xp - current_level_xp) / (next_level_xp - current_level_xp) if next_level_xp > current_level_xp else 0
        safe_progress = max(0.0, min(float(progress), 1.0))
        st.progress(safe_progress)
        
        st.markdown("---")
        
        # Menu de navigation
        menu = st.radio(
            "Navigation",
            ["🏠 Dashboard", "💰 Finance", "⚡ Énergie", "🔥 Habitudes", 
             "🎯 Objectifs", "🧪 Projets", "📔 Journal", "😴 Sommeil",
             "⚔️ Quêtes", "📊 Analytics", "👤 Profil", "🤖 Coach IA"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.caption(f"📅 {datetime.date.today().strftime('%d %B %Y')}")
        
        return menu

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    """Page principale du Dashboard"""
    st.title("🏠 Cockpit Principal")
    st.caption("Vue d'ensemble de ta vie")
    
    db = get_db()
    
    # Initialisation
    init_profile(db)
    init_skills(db)
    init_achievements(db)
    generate_daily_quests(db)
    
    # Données
    profile = db.query(UserProfile).first()
    investments = db.query(Investment).all()
    total_finance = sum(i.amount for i in investments)
    freedom_pct = min(round(total_finance / 50000 * 100, 1), 100) if total_finance > 0 else 0
    
    last_energy = db.query(EnergyLog).order_by(EnergyLog.id.desc()).first()
    energy_level = last_energy.level if last_energy else 5
    
    active_projects = db.query(Project).filter(Project.status == "active").count()
    
    habits = db.query(Habit).all()
    today = datetime.date.today()
    completed_today = sum(1 for h in habits if db.query(HabitLog).filter(
        HabitLog.habit_id == h.id, HabitLog.completed_at == today).first())
    
    # Hero Card - Liberté Financière
    st.markdown("""
    <div class="hero-card">
        <h2 style='margin-bottom: 0.5rem;'>Indice de Liberté Financière</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.metric("Progression", f"{freedom_pct}%", f"{total_finance:,.0f} € / 50 000 €")
        st.progress(freedom_pct / 100)
    with col2:
        st.metric("Niveau", profile.level)
        st.metric("XP Total", f"{profile.total_xp:,}")
    
    st.markdown("---")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Patrimoine", f"{total_finance:,.0f} €", f"{len(investments)} actifs")
    
    with col2:
        delta_energy = "Optimal" if energy_level >= 7 else "Modéré" if energy_level >= 4 else "Faible"
        st.metric("⚡ Énergie", f"{energy_level}/10", delta_energy)
    
    with col3:
        st.metric("🧪 Projets Actifs", active_projects)
    
    with col4:
        st.metric("🔥 Habitudes", f"{completed_today}/{len(habits)}", f"Complétées")
    
    st.markdown("---")
    
    # Conseils du Coach
    st.subheader("🤖 Conseils du Coach")
    tips = generate_coach_tips(db)
    for tip in tips:
        st.info(tip)
    
    # Quêtes du jour
    st.markdown("---")
    st.subheader("⚔️ Quêtes du Jour")
    
    daily_quests = db.query(Quest).filter(
        Quest.quest_type == "daily",
        Quest.created_at >= datetime.datetime.combine(today, datetime.time.min)
    ).all()
    
    if daily_quests:
        for quest in daily_quests:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"**{quest.title}** - {quest.description}")
            with col2:
                st.caption(f"+{quest.xp_reward} XP")
            with col3:
                if quest.completed:
                    st.success("✅")
                else:
                    st.warning("🔄")
    else:
        st.info("Aucune quête active")
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FINANCE
# ══════════════════════════════════════════════════════════════════════════════

def page_finance():
    """Page de gestion des finances"""
    st.title("💰 Finance & Patrimoine")
    
    db = get_db()
    investments = db.query(Investment).all()
    total = sum(i.amount for i in investments)
    freedom = min(round(total / 50000 * 100, 1), 100) if total > 0 else 0
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Patrimoine Total", f"{total:,.0f} €")
    with col2:
        st.metric("Liberté Financière", f"{freedom}%")
    with col3:
        st.metric("Nombre d'Actifs", len(investments))
    
    st.progress(freedom / 100)
    
    st.markdown("---")
    
    # Formulaire d'ajout
    with st.expander("➕ Ajouter un investissement", expanded=False):
        with st.form("add_investment"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nom de l'actif")
                amount = st.number_input("Montant investi (€)", min_value=0.0, step=100.0)
            with col2:
                category = st.selectbox("Catégorie", 
                    ["Crypto", "Stocks", "RealEstate", "Savings", "Royaltiz", "Other"])
                current_value = st.number_input("Valeur actuelle (€)", min_value=0.0, step=100.0)
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("💾 Ajouter", use_container_width=True):
                db.add(Investment(
                    name=name, category=category, amount=amount,
                    current_value=current_value or amount, notes=notes
                ))
                db.commit()
                st.success("✅ Investissement ajouté !")
                st.rerun()
    
    # Liste des investissements
    st.subheader("📊 Portefeuille")
    
    if investments:
        # Répartition par catégorie
        df = pd.DataFrame([{"Catégorie": i.category, "Montant": i.amount} for i in investments])
        if not df.empty:
            fig = px.pie(df, values="Montant", names="Catégorie", 
                        title="Répartition du patrimoine",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tableau des actifs
        for inv in investments:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"**{inv.name}**")
                st.caption(inv.category)
            with col2:
                st.metric("Investi", f"{inv.amount:,.0f} €")
            with col3:
                gain = inv.current_value - inv.amount if inv.current_value else 0
                st.metric("Valeur", f"{inv.current_value:,.0f} €", f"{gain:+,.0f} €")
            with col4:
                if st.button("🗑️", key=f"del_inv_{inv.id}"):
                    db.query(Investment).filter(Investment.id == inv.id).delete()
                    db.commit()
                    st.rerun()
            st.markdown("---")
    else:
        st.info("Aucun investissement enregistré")
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ENERGIE
# ══════════════════════════════════════════════════════════════════════════════

def page_energy():
    """Page de suivi de l'énergie"""
    st.title("⚡ Énergie & Bien-être")
    
    db = get_db()
    logs = db.query(EnergyLog).order_by(EnergyLog.id.desc()).limit(20).all()
    
    last = logs[0] if logs else None
    current = last.level if last else 5
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Niveau Actuel", f"{current}/10")
    with col2:
        if logs:
            avg = round(sum(l.level for l in logs[:7]) / min(len(logs), 7), 1)
            st.metric("Moyenne 7j", avg)
    with col3:
        sleep_logs = [l.sleep_hours for l in logs if l.sleep_hours]
        avg_sleep = round(sum(sleep_logs) / len(sleep_logs), 1) if sleep_logs else 0
        st.metric("Sommeil Moyen", f"{avg_sleep}h")
    
    # Barre d'énergie visuelle
    energy_color = "🟢" if current >= 7 else "🟡" if current >= 4 else "🔴"
    st.markdown(f"### {energy_color} " + "█" * current + "░" * (10 - current))
    
    # Conseil
    if current >= 8:
        st.success("🚀 Énergie max ! Tâches difficiles recommandées.")
    elif current >= 6:
        st.info("💪 Bonne énergie. Focus productivité.")
    elif current >= 4:
        st.warning("☕ Énergie moyenne. Priorisez.")
    else:
        st.error("🌙 Repos recommandé.")
    
    st.markdown("---")
    
    # Formulaire
    with st.expander("➕ Logger mon énergie", expanded=True):
        with st.form("add_energy"):
            level = st.slider("Niveau d'énergie", 1, 10, 5)
            
            col1, col2 = st.columns(2)
            with col1:
                mood = st.selectbox("Humeur", 
                    ["😊 Excellent", "🙂 Bien", "😐 Neutre", "😔 Fatigué", "😫 Épuisé"])
            with col2:
                activity = st.selectbox("Activité principale",
                    ["💼 Travail", "🏃 Sport", "📚 Étude", "🎮 Loisir", "😴 Repos"])
            
            sleep_hours = st.number_input("Heures de sommeil (nuit dernière)", 0.0, 12.0, 7.0, 0.5)
            notes = st.text_area("Notes")
            
            if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                db.add(EnergyLog(
                    level=level, mood=mood.split()[1], activity=activity.split()[1],
                    sleep_hours=sleep_hours, notes=notes
                ))
                award_xp(db, 5, "Log énergie", "Énergie")
                db.commit()
                st.success("✅ Énergie enregistrée ! +5 XP")
                st.rerun()
    
    # Graphique d'évolution
    if logs:
        st.subheader("📈 Évolution")
        df = pd.DataFrame([{
            "Date": l.timestamp.strftime("%d/%m"),
            "Niveau": l.level
        } for l in reversed(logs[:14])])
        
        fig = px.line(df, x="Date", y="Niveau", markers=True)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            yaxis_range=[0, 10]
        )
        fig.update_traces(line_color='#32d7e2', marker_color='#32d7e2')
        st.plotly_chart(fig, use_container_width=True)
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HABITUDES
# ══════════════════════════════════════════════════════════════════════════════

def page_habits():
    """Page de gestion des habitudes"""
    st.title("🔥 Habitudes")
    
    db = get_db()
    habits = db.query(Habit).all()
    today = datetime.date.today()
    
    # Stats
    completed_today = sum(1 for h in habits if db.query(HabitLog).filter(
        HabitLog.habit_id == h.id, HabitLog.completed_at == today).first())
    best_streak = max((h.best_streak for h in habits), default=0)
    potential_xp = sum(h.xp_reward for h in habits if not db.query(HabitLog).filter(
        HabitLog.habit_id == h.id, HabitLog.completed_at == today).first())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Aujourd'hui", f"{completed_today}/{len(habits)}")
    with col2:
        st.metric("Meilleure Série", f"{best_streak} jours")
    with col3:
        st.metric("XP Potentiel", f"+{potential_xp}")
    
    st.markdown("---")
    
    # Liste des habitudes
    st.subheader("📋 Mes Habitudes")
    
    for habit in habits:
        log = db.query(HabitLog).filter(
            HabitLog.habit_id == habit.id, 
            HabitLog.completed_at == today
        ).first()
        is_done = log is not None
        
        col1, col2, col3, col4 = st.columns([1, 4, 2, 1])
        
        with col1:
            if st.checkbox("", value=is_done, key=f"habit_{habit.id}"):
                if not is_done:
                    # Compléter l'habitude
                    db.add(HabitLog(habit_id=habit.id, completed_at=today))
                    habit.streak += 1
                    if habit.streak > habit.best_streak:
                        habit.best_streak = habit.streak
                    award_xp(db, habit.xp_reward, f"Habitude: {habit.name}", habit.skill_target)
                    db.commit()
                    check_achievements(db)
                    st.rerun()
        
        with col2:
            status = "✅" if is_done else "⬜"
            st.markdown(f"{status} **{habit.name}**")
            st.caption(f"🔥 Série: {habit.streak} jours | +{habit.xp_reward} XP {habit.skill_target}")
        
        with col3:
            st.caption(f"Record: {habit.best_streak}j")
        
        with col4:
            if st.button("🗑️", key=f"del_habit_{habit.id}"):
                db.query(HabitLog).filter(HabitLog.habit_id == habit.id).delete()
                db.query(Habit).filter(Habit.id == habit.id).delete()
                db.commit()
                st.rerun()
    
    st.markdown("---")
    
    # Ajouter une habitude
    with st.expander("➕ Nouvelle Habitude"):
        with st.form("add_habit"):
            name = st.text_input("Nom de l'habitude")
            
            col1, col2 = st.columns(2)
            with col1:
                skill_target = st.selectbox("Compétence liée",
                    ["Discipline", "Focus", "Énergie", "Créativité", "Santé", "Social", "Business", "Intelligence"])
            with col2:
                xp_reward = st.selectbox("Récompense XP", [5, 10, 15, 25])
            
            frequency = st.selectbox("Fréquence", ["daily", "weekly"])
            
            if st.form_submit_button("💾 Créer", use_container_width=True):
                db.add(Habit(name=name, skill_target=skill_target, xp_reward=xp_reward, frequency=frequency))
                db.commit()
                st.success("✅ Habitude créée !")
                st.rerun()
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OBJECTIFS
# ══════════════════════════════════════════════════════════════════════════════

def page_goals():
    """Page de gestion des objectifs"""
    st.title("🎯 Objectifs")
    
    db = get_db()
    goals = db.query(Goal).all()
    
    # Stats
    completed = sum(1 for g in goals if g.current_value >= g.target_value)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Objectifs", len(goals))
    with col2:
        st.metric("Complétés", completed)
    
    st.markdown("---")
    
    # Liste des objectifs
    for goal in goals:
        progress = (goal.current_value / goal.target_value * 100) if goal.target_value > 0 else 0
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{goal.title}**")
            st.progress(min(progress / 100, 1.0))
            st.caption(f"{goal.current_value:,.0f} / {goal.target_value:,.0f} {goal.unit} ({progress:.0f}%)")
            if goal.deadline:
                days_left = (goal.deadline - datetime.date.today()).days
                st.caption(f"📅 {days_left} jours restants")
        
        with col2:
            new_val = st.number_input("Valeur", value=float(goal.current_value), 
                                       key=f"goal_val_{goal.id}", label_visibility="collapsed")
            if new_val != goal.current_value:
                goal.current_value = new_val
                db.commit()
                st.rerun()
            
            if st.button("🗑️", key=f"del_goal_{goal.id}"):
                db.query(Goal).filter(Goal.id == goal.id).delete()
                db.commit()
                st.rerun()
        
        st.markdown("---")
    
    # Ajouter un objectif
    with st.expander("➕ Nouvel Objectif"):
        with st.form("add_goal"):
            title = st.text_input("Titre")
            
            col1, col2 = st.columns(2)
            with col1:
                target_value = st.number_input("Valeur cible", min_value=0.0, step=100.0)
                current_value = st.number_input("Valeur actuelle", min_value=0.0, step=100.0)
            with col2:
                unit = st.text_input("Unité", "€")
                deadline = st.date_input("Deadline")
            
            category = st.selectbox("Catégorie", ["finance", "health", "career", "personal"])
            
            if st.form_submit_button("💾 Créer", use_container_width=True):
                db.add(Goal(title=title, target_value=target_value, current_value=current_value,
                           unit=unit, deadline=deadline, category=category))
                db.commit()
                st.success("✅ Objectif créé !")
                st.rerun()
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PROJETS
# ══════════════════════════════════════════════════════════════════════════════

def page_projects():
    """Page de gestion des projets"""
    st.title("🧪 Lab Projets")
    
    db = get_db()
    projects = db.query(Project).order_by(Project.priority.desc()).all()
    
    # Stats par statut
    by_status = {"idea": 0, "planning": 0, "active": 0, "paused": 0, "completed": 0}
    for p in projects:
        by_status[p.status] = by_status.get(p.status, 0) + 1
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💡 Idées", by_status["idea"])
    col2.metric("📋 Planifié", by_status["planning"])
    col3.metric("🚀 Actif", by_status["active"])
    col4.metric("⏸️ Pause", by_status["paused"])
    col5.metric("✅ Complété", by_status["completed"])
    
    st.markdown("---")
    
    # Tabs par statut
    tabs = st.tabs(["💡 Idées", "📋 Planning", "🚀 Actifs", "✅ Complétés"])
    
    status_map = {0: "idea", 1: "planning", 2: "active", 3: "completed"}
    
    for i, tab in enumerate(tabs):
        with tab:
            status = status_map[i]
            filtered = [p for p in projects if p.status == status]
            
            for project in filtered:
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    st.markdown(f"**{project.title}**")
                    if project.description:
                        st.caption(project.description[:100])
                with col2:
                    new_status = st.selectbox(
                        "Statut", ["idea", "planning", "active", "paused", "completed"],
                        index=["idea", "planning", "active", "paused", "completed"].index(project.status),
                        key=f"status_{project.id}",
                        label_visibility="collapsed"
                    )
                    if new_status != project.status:
                        project.status = new_status
                        if new_status == "completed":
                            project.completed_at = datetime.datetime.utcnow()
                            award_xp(db, 50, f"Projet: {project.title}", "Business")
                        db.commit()
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"del_proj_{project.id}"):
                        db.query(Project).filter(Project.id == project.id).delete()
                        db.commit()
                        st.rerun()
                st.markdown("---")
    
    # Ajouter un projet
    with st.expander("➕ Nouveau Projet"):
        with st.form("add_project"):
            title = st.text_input("Titre")
            description = st.text_area("Description")
            
            col1, col2 = st.columns(2)
            with col1:
                status = st.selectbox("Statut initial", ["idea", "planning", "active"])
                priority = st.slider("Priorité", 1, 10, 5)
            with col2:
                category = st.selectbox("Catégorie", ["business", "tech", "creative", "personal"])
                deadline = st.date_input("Deadline (optionnel)")
            
            if st.form_submit_button("💾 Créer", use_container_width=True):
                db.add(Project(title=title, description=description, status=status,
                              priority=priority, category=category, deadline=deadline))
                db.commit()
                st.success("✅ Projet créé !")
                st.rerun()
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: JOURNAL
# ══════════════════════════════════════════════════════════════════════════════

def page_journal():
    """Page du journal"""
    st.title("📔 Journal de Pensées")
    
    db = get_db()
    entries = db.query(JournalEntry).order_by(JournalEntry.id.desc()).limit(20).all()
    total = db.query(JournalEntry).count()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Entrées", total)
    with col2:
        st.metric("XP Mémoire", f"+{total * 5}")
    
    st.markdown("---")
    
    # Nouvelle entrée
    with st.expander("➕ Nouvelle Pensée", expanded=True):
        with st.form("add_journal"):
            content = st.text_area("Qu'est-ce qui te traverse l'esprit ?", height=150)
            
            col1, col2 = st.columns(2)
            with col1:
                mood = st.selectbox("Humeur", 
                    ["😊 Heureux", "😌 Calme", "🔥 Motivé", "🤔 Pensif", "😴 Fatigué"])
            with col2:
                tags = st.text_input("Tags (séparés par virgule)")
            
            if st.form_submit_button("💾 Enregistrer (+5 XP)", use_container_width=True):
                db.add(JournalEntry(content=content, mood=mood.split()[0], tags=tags))
                award_xp(db, 5, "Entrée journal", "Intelligence")
                db.commit()
                check_achievements(db)
                st.success("✅ Pensée capturée ! +5 XP")
                st.rerun()
    
    # Entrées récentes
    st.subheader("📝 Entrées Récentes")
    
    for entry in entries:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{entry.mood}** - {entry.created_at.strftime('%d/%m/%Y %H:%M')}")
                st.markdown(entry.content)
                if entry.tags:
                    st.caption(f"🏷️ {entry.tags}")
            with col2:
                if st.button("🗑️", key=f"del_journal_{entry.id}"):
                    db.query(JournalEntry).filter(JournalEntry.id == entry.id).delete()
                    db.commit()
                    st.rerun()
            st.markdown("---")
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SOMMEIL
# ══════════════════════════════════════════════════════════════════════════════

def page_sleep():
    """Page de suivi du sommeil"""
    st.title("😴 Sommeil & Biorythme")
    
    db = get_db()
    logs = db.query(SleepLog).order_by(SleepLog.date.desc()).limit(14).all()
    
    # Stats
    avg_duration = round(sum(l.duration for l in logs) / len(logs), 1) if logs else 0
    avg_quality = round(sum(l.quality for l in logs) / len(logs), 1) if logs else 0
    
    profile = db.query(UserProfile).first()
    goal = profile.sleep_goal if profile else 8.0
    debt = sum(max(0, goal - log.duration) for log in logs[:7]) if logs else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Durée Moyenne", f"{avg_duration}h")
    with col2:
        st.metric("Qualité", f"{avg_quality}/10")
    with col3:
        st.metric("Dette de Sommeil", f"{debt:.1f}h", "Élevée" if debt > 5 else "OK")
    
    # Conseils
    st.markdown("---")
    st.subheader("💡 Conseils")
    if debt > 5:
        st.warning("⚠️ Dette de sommeil élevée. Couche-toi plus tôt cette semaine.")
    if avg_quality < 6:
        st.info("💡 Qualité basse. Évite les écrans 1h avant le coucher.")
    if avg_duration < 7:
        st.info("😴 Tu dors moins de 7h. Vise 7-9h par nuit.")
    if debt <= 5 and avg_quality >= 6 and avg_duration >= 7:
        st.success("✨ Bon rythme de sommeil ! Continue ainsi.")
    
    st.markdown("---")
    
    # Logger une nuit
    with st.expander("➕ Logger ma nuit"):
        with st.form("add_sleep"):
            date = st.date_input("Date")
            
            col1, col2 = st.columns(2)
            with col1:
                bedtime = st.time_input("Heure de coucher", datetime.time(23, 0))
            with col2:
                waketime = st.time_input("Heure de lever", datetime.time(7, 0))
            
            quality = st.slider("Qualité (1-10)", 1, 10, 7)
            notes = st.text_area("Notes")
            
            if st.form_submit_button("💾 Enregistrer (+10 XP)", use_container_width=True):
                # Calculer durée
                bed_min = bedtime.hour * 60 + bedtime.minute
                wake_min = waketime.hour * 60 + waketime.minute
                if wake_min < bed_min:
                    wake_min += 24 * 60
                duration = round((wake_min - bed_min) / 60, 1)
                
                db.add(SleepLog(
                    date=date, bedtime=bedtime.strftime("%H:%M"),
                    waketime=waketime.strftime("%H:%M"),
                    duration=duration, quality=quality, notes=notes
                ))
                award_xp(db, 10, "Log sommeil", "Santé")
                db.commit()
                st.success("✅ Nuit enregistrée ! +10 XP")
                st.rerun()
    
    # Graphique
    if logs:
        st.subheader("📊 Historique")
        df = pd.DataFrame([{
            "Date": l.date.strftime("%d/%m"),
            "Durée": l.duration,
            "Qualité": l.quality
        } for l in reversed(logs)])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df["Date"], y=df["Durée"], name="Durée (h)", marker_color='#32d7e2'))
        fig.add_trace(go.Scatter(x=df["Date"], y=df["Qualité"], name="Qualité", 
                                  mode='lines+markers', yaxis='y2', marker_color='#bf5af2'))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            yaxis=dict(title="Durée (h)", range=[0, 12]),
            yaxis2=dict(title="Qualité", overlaying='y', side='right', range=[0, 10]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: QUÊTES
# ══════════════════════════════════════════════════════════════════════════════

def page_quests():
    """Page des quêtes"""
    st.title("⚔️ Quêtes & Missions")
    
    db = get_db()
    generate_daily_quests(db)
    generate_weekly_quest(db)
    
    today = datetime.date.today()
    
    # Boss de la semaine
    boss = db.query(Quest).filter(Quest.quest_type == "boss", Quest.completed == 0).first()
    
    if boss:
        st.markdown("### 🐉 Boss de la Semaine")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{boss.title}**")
            st.caption(boss.description)
            progress = (boss.current_value / boss.target_value * 100) if boss.target_value > 0 else 0
            st.progress(min(progress / 100, 1.0))
            st.caption(f"{boss.current_value}/{boss.target_value} ({progress:.0f}%)")
        with col2:
            st.metric("Récompense", f"+{boss.xp_reward} XP")
        st.markdown("---")
    
    # Quêtes du jour
    st.markdown("### 📋 Quêtes du Jour")
    
    daily = db.query(Quest).filter(
        Quest.quest_type == "daily",
        Quest.created_at >= datetime.datetime.combine(today, datetime.time.min)
    ).all()
    
    for quest in daily:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            icon = "✅" if quest.completed else "⬜"
            st.markdown(f"{icon} **{quest.title}**")
            st.caption(quest.description)
        with col2:
            st.caption(f"+{quest.xp_reward} XP")
        with col3:
            if not quest.completed:
                if st.button("Compléter", key=f"quest_{quest.id}"):
                    quest.completed = 1
                    award_xp(db, quest.xp_reward, f"Quête: {quest.title}", quest.skill_target)
                    db.commit()
                    st.rerun()
    
    # Stats
    st.markdown("---")
    completed_total = db.query(Quest).filter(Quest.completed == 1).count()
    st.metric("Total Quêtes Complétées", completed_total)
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

def page_analytics():
    """Page des analytics"""
    st.title("📊 Analytics Personnel")
    
    db = get_db()
    init_skills(db)
    
    # Stats globales
    active_days = db.query(HabitLog).distinct(HabitLog.completed_at).count()
    total_habits = db.query(HabitLog).count()
    profile = db.query(UserProfile).first()
    total_xp = profile.total_xp if profile else 0
    achievements_unlocked = db.query(Achievement).filter(Achievement.unlocked == 1).count()
    total_achievements = db.query(Achievement).count()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jours Actifs", active_days)
    with col2:
        st.metric("Habitudes Faites", total_habits)
    with col3:
        st.metric("XP Total", f"{total_xp:,}")
    with col4:
        st.metric("Achievements", f"{achievements_unlocked}/{total_achievements}")
    
    st.markdown("---")
    
    # Radar des compétences
    st.subheader("🎯 Radar des Compétences")
    
    skills = db.query(Skill).all()
    if skills:
        categories = [s.name for s in skills]
        values = [s.level for s in skills]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(50, 215, 226, 0.3)',
            line_color='#32d7e2'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(values) + 2]),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Détail des skills
        cols = st.columns(4)
        for i, skill in enumerate(skills):
            with cols[i % 4]:
                st.markdown(f"**{skill.icon} {skill.name}**")
                st.caption(f"Niveau {skill.level} • {skill.xp} XP")
                st.progress(min(skill.level / 10, 1.0))
    
    st.markdown("---")
    
    # XP des 7 derniers jours
    st.subheader("📈 XP des 7 Derniers Jours")
    
    xp_data = []
    today = datetime.date.today()
    for i in range(6, -1, -1):
        day = today - datetime.timedelta(days=i)
        day_start = datetime.datetime.combine(day, datetime.time.min)
        day_end = datetime.datetime.combine(day, datetime.time.max)
        day_xp = sum(log.amount for log in db.query(XPLog).filter(
            XPLog.created_at >= day_start, XPLog.created_at <= day_end
        ).all())
        xp_data.append({"Jour": day.strftime("%a"), "XP": day_xp})
    
    df = pd.DataFrame(xp_data)
    fig = px.bar(df, x="Jour", y="XP", color_discrete_sequence=['#32d7e2'])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PROFIL
# ══════════════════════════════════════════════════════════════════════════════

def page_profile():
    """Page du profil"""
    st.title("👤 Profil Cognitif")
    
    db = get_db()
    init_profile(db)
    init_skills(db)
    init_achievements(db)
    check_achievements(db)
    
    profile = db.query(UserProfile).first()
    skills = db.query(Skill).all()
    achievements = db.query(Achievement).all()
    xp_logs = db.query(XPLog).order_by(XPLog.id.desc()).limit(10).all()
    
    # Header profil
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #bf5af2, #ff375f); 
                    border-radius: 50%; width: 100px; height: 100px; 
                    display: flex; align-items: center; justify-content: center;
                    font-size: 2.5rem; font-weight: bold;'>
            {profile.level}
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"# {profile.name}")
        st.caption(f"🏷️ {profile.title}")
        st.caption(f"🎮 Classe: {profile.character_class}")
        
        # Barre XP
        current_xp = profile.total_xp
        current_level_xp = xp_for_level(profile.level)
        next_level_xp = xp_for_level(profile.level + 1)
        progress = (current_xp - current_level_xp) / (next_level_xp - current_level_xp) if next_level_xp > current_level_xp else 0
        
        st.progress(min(progress, 1.0))
        st.caption(f"{current_xp} / {next_level_xp} XP → Niveau {profile.level + 1}")
    
    st.markdown("---")
    
    # Compétences
    st.subheader("🎯 Compétences")
    cols = st.columns(4)
    for i, skill in enumerate(skills):
        with cols[i % 4]:
            st.markdown(f"**{skill.icon} {skill.name}**")
            st.progress(min(skill.level / 10, 1.0))
            st.caption(f"Nv.{skill.level} • {skill.xp} XP")
    
    st.markdown("---")
    
    # Achievements
    st.subheader("🏆 Achievements")
    cols = st.columns(4)
    for i, ach in enumerate(achievements):
        with cols[i % 4]:
            status = "🔓" if ach.unlocked else "🔒"
            st.markdown(f"{status} **{ach.icon} {ach.name}**")
            st.caption(ach.description)
    
    st.markdown("---")
    
    # Historique XP
    st.subheader("📊 Historique XP Récent")
    for log in xp_logs:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{log.source}**")
            st.caption(f"{log.skill_name or 'Global'} • {log.created_at.strftime('%d/%m %H:%M')}")
        with col2:
            st.markdown(f"**+{log.amount} XP**")
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: COACH IA
# ══════════════════════════════════════════════════════════════════════════════

def page_coach():
    """Page du Coach IA"""
    st.title("🤖 Coach IA Personnel")
    st.caption("Conseils intelligents basés sur tes données")
    
    db = get_db()
    
    # Data points
    data_points = (
        db.query(HabitLog).count() +
        db.query(EnergyLog).count() +
        db.query(SleepLog).count() +
        db.query(JournalEntry).count()
    )
    
    st.info(f"📊 Analyse basée sur {data_points} points de données")
    
    st.markdown("---")
    
    # Conseils
    st.subheader("💡 Conseils Personnalisés")
    tips = generate_coach_tips(db)
    for tip in tips:
        st.markdown(f"> {tip}")
    
    st.markdown("---")
    
    # Prédiction
    st.subheader("📈 Prédiction de Progression")
    
    profile = db.query(UserProfile).first()
    xp_logs_week = db.query(XPLog).filter(
        XPLog.created_at >= datetime.datetime.now() - datetime.timedelta(days=7)
    ).all()
    
    avg_xp_day = sum(l.amount for l in xp_logs_week) / 7 if xp_logs_week else 10
    current_level = profile.level if profile else 1
    current_xp = profile.total_xp if profile else 0
    next_level_xp = xp_for_level(current_level + 1)
    xp_needed = next_level_xp - current_xp
    days_to_level = max(1, int(xp_needed / avg_xp_day)) if avg_xp_day > 0 else 30
    
    st.metric("Prochain Niveau", current_level + 1, f"dans ~{days_to_level} jours")
    st.progress(min(current_xp / next_level_xp, 1.0))
    
    st.markdown("---")
    
    # Actions recommandées
    st.subheader("🎯 Actions Recommandées")
    
    today = datetime.date.today()
    
    # Journal
    journal_today = db.query(JournalEntry).filter(
        JournalEntry.created_at >= datetime.datetime.combine(today, datetime.time.min)
    ).count()
    if journal_today == 0:
        st.markdown("- 📝 Écrire dans ton journal (+5 XP)")
    
    # Énergie
    energy_today = db.query(EnergyLog).filter(
        EnergyLog.timestamp >= datetime.datetime.combine(today, datetime.time.min)
    ).count()
    if energy_today == 0:
        st.markdown("- ⚡ Logger ton niveau d'énergie (+5 XP)")
    
    # Habitudes
    habits = db.query(Habit).all()
    for h in habits[:3]:
        log = db.query(HabitLog).filter(HabitLog.habit_id == h.id, HabitLog.completed_at == today).first()
        if not log:
            st.markdown(f"- ✅ Compléter: {h.name} (+{h.xp_reward} XP)")
    
    db.close()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal"""
    
    # Sidebar et navigation
    menu = render_sidebar()
    
    # Router vers la bonne page
    if menu == "🏠 Dashboard":
        page_dashboard()
    elif menu == "💰 Finance":
        page_finance()
    elif menu == "⚡ Énergie":
        page_energy()
    elif menu == "🔥 Habitudes":
        page_habits()
    elif menu == "🎯 Objectifs":
        page_goals()
    elif menu == "🧪 Projets":
        page_projects()
    elif menu == "📔 Journal":
        page_journal()
    elif menu == "😴 Sommeil":
        page_sleep()
    elif menu == "⚔️ Quêtes":
        page_quests()
    elif menu == "📊 Analytics":
        page_analytics()
    elif menu == "👤 Profil":
        page_profile()
    elif menu == "🤖 Coach IA":
        page_coach()

if __name__ == "__main__":
    main()
