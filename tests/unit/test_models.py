from Splity.domainmodel.models import Group, User

def test_new_group_generates_invite_code():
    group = Group(name="Trip", description="Italy", currency="EUR", creator_id=1)
    assert len(group.invite_code) == 6
    # assert group.invite_code.isupper()

def test_user_get_id_returns_string():
    user = User("Alice", "alice", "a@a.com", user_id=99)
    assert user.get_id() == "99"