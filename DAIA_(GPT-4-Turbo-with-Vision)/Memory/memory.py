from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()


class Goal(Base):
    __tablename__ = "goals"
    goal_id = Column(Integer, primary_key=True)
    goal_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=True)

    # Define the relationship between Goal and GoalAction
    actions = relationship("GoalAction", back_populates="goal")


class GoalAction(Base):
    __tablename__ = "goal_actions"
    action_id = Column(Integer, primary_key=True)
    goal_id = Column(Integer, ForeignKey("goals.goal_id"))
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    full_data = Column(String(1000), nullable=False)
    important_data = Column(String(1000), nullable=False)

    # Define the relationship between GoalAction and Goal
    goal = relationship("Goal", back_populates="actions")


class Memory:
    def __init__(self):
        engine = create_engine("sqlite:///MemoryDB.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_goal_object(self, name):
        goal = Goal(goal_name=name, status="in progress")
        self.session.add(goal)
        return goal

    def create_action_object(self, goal_id, title, category, full_data, important_data):
        goal = self.session.query(Goal).filter_by(goal_id=goal_id).first()
        if goal is None:
            return None

        action = GoalAction(
            goal=goal,
            title=title,
            category=category,
            full_data=full_data,
            important_data=important_data,
        )
        return action

    def save_objects_in_db(self, objects: list):
        self.session.add_all(objects)
        self.session.commit()

    def get_all_goals(self):
        return self.session.query(Goal).all()

    def get_latest_goal(self):
        return self.session.query(Goal).order_by(Goal.goal_id.desc()).first()

    def get_latest_action_of_goal(self, goal_id):
        goal = self.session.query(Goal).filter_by(goal_id=goal_id).first()
        if goal is None:
            return None

        return (
            self.session.query(GoalAction)
            .filter_by(goal=goal)
            .order_by(GoalAction.action_id.desc())
            .first()
        )

    def get_actions_of_goal(self, goal_id):
        goal = self.session.query(Goal).filter_by(goal_id=goal_id).first()
        if goal is None:
            return []

        actions = self.session.query(GoalAction).filter(GoalAction.goal == goal).all()
        return actions

    def get_ordered_actions_of_goal(self, goal_id, num_actions):
        goal = self.session.query(Goal).filter_by(goal_id=goal_id).first()
        if goal is None:
            return []

        actions = (
            self.session.query(GoalAction)
            .filter(GoalAction.goal == goal)
            .order_by(GoalAction.action_id.desc())
            .limit(num_actions)
            .all()
        )
        return actions
