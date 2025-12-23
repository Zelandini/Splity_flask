from Splity.adapters.database import db
from Splity.adapters.orm import UserORM, BillORM, BillParticipantORM, GroupORM
from Splity.domainmodel.models import User, Bill, BillParticipant, Group


class UserRepository:
    """Handles all User database operations"""

    def add(self, user: User):
        user_orm = UserORM(
            name=user.name,
            username=user.username,
            email=user.email,
            password=user.password
        )
        db.session.add(user_orm)
        db.session.commit()
        return user_orm.id

    def get_by_id(self, user_id: int):
        user_orm = UserORM.query.get(user_id)
        return self._to_domain(user_orm) if user_orm else None

    def get_by_email(self, email: str):
        """Find user by email"""
        user_orm = UserORM.query.filter_by(email=email).first()
        if user_orm:
            return self._to_domain(user_orm)
        return None

    def get_by_username(self, username: str):
        user_orm = UserORM.query.filter_by(username=username).first()
        return self._to_domain(user_orm) if user_orm else None

    def get_all(self):
        """Get all users"""
        users_orm = UserORM.query.all()
        return [self._to_domain(u) for u in users_orm]

    def _to_domain(self, user_orm: UserORM) -> User:
        user = User(
            user_id=user_orm.id,
            name=user_orm.name,
            username=user_orm.username,
            email=user_orm.email,
            password=user_orm.password
        )
        # Bridge the gap: Convert ORM groups to Domain groups
        for group_orm in user_orm.groups:
            domain_group = Group(
                name=group_orm.name,
                currency=group_orm.currency,
                creator_id=group_orm.creator_id,
                group_id=group_orm.id,
                description=group_orm.description,
            )
            user.add_group(domain_group)
        return user


class BillRepository:
    """Handles all Bill database operations"""

    def create(self, bill: Bill):
        bill_orm = BillORM(
            user_id=bill.user_id,
            description=bill.description,
            date=bill.date,
            amount=bill.amount
        )
        db.session.add(bill_orm)
        db.session.commit()
        return bill_orm.id

    def get_by_id(self, bill_id: int):
        """Get bill by ID"""
        bill_orm = BillORM.query.get(bill_id)
        if bill_orm:
            return self._to_domain(bill_orm)
        return None

    def get_bills_by_user(self, user_id: int):
        """Get all bills where user is a participant"""
        # Query through participants to find all bills user is in
        participants = BillParticipantORM.query.filter_by(user_id=user_id).all()
        bill_ids = [p.bill_id for p in participants]
        bills_orm = BillORM.query.filter(BillORM.id.in_(bill_ids)).all()
        return [self._to_domain(b) for b in bills_orm]

    def get_bills_created_by_user(self, user_id: int):
        """Get all bills created by user"""
        bills_orm = BillORM.query.filter_by(user_id=user_id).all()
        return [self._to_domain(b) for b in bills_orm]

    def _to_domain(self, bill_orm: BillORM) -> Bill:
        return Bill(
            bill_id=bill_orm.id,
            user_id=bill_orm.user_id,
            description=bill_orm.description,
            created_date=bill_orm.date,
            amount=bill_orm.amount
        )


class BillParticipantRepository:
    """Handles BillParticipant operations"""

    def add_participant(self, bill_id: int, user_id: int, amount_owed: float):
        """Add a participant to a bill"""
        participant = BillParticipantORM(
            bill_id=bill_id,
            user_id=user_id,
            amount_owed=amount_owed,
            has_paid=False
        )
        db.session.add(participant)
        db.session.commit()
        return participant.id

    def get_participants_for_bill(self, bill_id: int):
        """Get all participants for a bill"""
        participants_orm = BillParticipantORM.query.filter_by(bill_id=bill_id).all()
        return [self._to_domain(p) for p in participants_orm]

    def get_bills_for_user(self, user_id: int):
        """Get all bill participations for a user"""
        participants_orm = BillParticipantORM.query.filter_by(user_id=user_id).all()
        return [self._to_domain(p) for p in participants_orm]

    def mark_paid(self, bill_id: int, user_id: int):
        """Mark a participant as having paid"""
        participant = BillParticipantORM.query.filter_by(
            bill_id=bill_id,
            user_id=user_id
        ).first()
        if participant:
            participant.has_paid = True
            db.session.commit()
            return True
        return False

    def _to_domain(self, participant_orm: BillParticipantORM) -> BillParticipant:
        return BillParticipant(
            participant_id=participant_orm.id,
            bill_id=participant_orm.bill_id,
            user_id=participant_orm.user_id,
            amount_owed=participant_orm.amount_owed,
            has_paid=participant_orm.has_paid
        )


class GroupRepository:
    def add(self, group: Group):
        group_orm = GroupORM(
            name=group.name,
            description=group.description,  # FIX: Save the description
            currency=group.currency,
            invite_code=group.invite_code,
            creator_id=group.creator_id
        )
        # Add the creator as the first member automatically
        creator_orm = UserORM.query.get(group.creator_id)
        if creator_orm:
            group_orm.members.append(creator_orm)

        db.session.add(group_orm)
        db.session.commit()
        return group_orm.id

    def join_by_code(self, user_id: int, invite_code: str):
        group_orm = GroupORM.query.filter_by(invite_code=invite_code).first()
        user_orm = UserORM.query.get(user_id)
        if group_orm and user_orm:
            if user_orm not in group_orm.members:
                group_orm.members.append(user_orm)
                db.session.commit()
                return True
        return False

    def get_by_name_and_creator(self, name: str, creator_id: int):
        """Finds if this specific user already has a group with this name."""
        group_orm = GroupORM.query.filter_by(name=name, creator_id=creator_id).first()
        return self._to_domain(group_orm) if group_orm else None

    def _to_domain(self, group_orm: GroupORM) -> Group:
        return Group(
            group_id=group_orm.id,
            name=group_orm.name,
            description=group_orm.description, # FIX: Pass description
            currency=group_orm.currency,
            creator_id=group_orm.creator_id,
            invite_code=group_orm.invite_code   # FIX: Pass the code from DB
        )
