import logging

from flask_migrate import Migrate

from opserv.model.meta import Session, db
from opserv.model.base_models import EnumE
from opserv.model.rank import Rank
from opserv.model.user import User
from opserv.model.enlistment_application import EnlistmentApplication
from opserv.model.activation_code import ActivationCode
from opserv.model.reset_password import ResetPasswordCode
from opserv.model.game import Game
from opserv.model.billet import Billet
from opserv.model.operation_type import OperationType
from opserv.model.operation import Operation
from opserv.model.member_game import MemberGames
from opserv.model.audit_user import UserAuditLog

__all__ = [
    "Session",
    "User",
    "ActivationCode",
    "ResetPasswordCode",
    "Game",
    "Rank",
    "Billet",
    "OperationType",
    "Operation",
    "MemberGames",
    "EnlistmentApplication",
    "UserAuditLog",
    "init_model",
    "EnumE",
]

log = logging.getLogger(__name__)


def init_model(app):
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
