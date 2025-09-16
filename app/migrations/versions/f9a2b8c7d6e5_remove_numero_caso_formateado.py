"""remove numero_caso_formateado field

Revision ID: f9a2b8c7d6e5
Revises: e78cd4d5ef2d
Create Date: 2025-01-16 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9a2b8c7d6e5'
down_revision: Union[str, Sequence[str], None] = 'e78cd4d5ef2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # NOTA: Esta migración elimina la columna numero_caso_formateado
    # ya que ahora usamos numero_caso_completo que tiene la misma funcionalidad
    
    # Eliminar la columna numero_caso_formateado (ya no es necesaria)
    # IMPORTANTE: Asegúrate de que numero_caso_completo esté poblado antes de ejecutar esta migración
    op.drop_column('casos', 'numero_caso_formateado')


def downgrade() -> None:
    """Downgrade schema."""
    # Recrear la columna numero_caso_formateado si es necesario hacer rollback
    op.add_column('casos', sa.Column('numero_caso_formateado', sa.String(length=20), nullable=True))
    
    # NOTA: En un rollback real, necesitarías repoblar esta columna
    # con los valores correctos basados en tipo, año y numero_caso