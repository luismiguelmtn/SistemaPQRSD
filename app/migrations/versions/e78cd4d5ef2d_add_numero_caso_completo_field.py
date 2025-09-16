"""add numero_caso_completo field

Revision ID: e78cd4d5ef2d
Revises: 304e8603a3bb
Create Date: 2025-09-16 14:53:15.641168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e78cd4d5ef2d'
down_revision: Union[str, Sequence[str], None] = '304e8603a3bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar campo numero_caso_completo a la tabla casos
    op.add_column('casos', sa.Column('numero_caso_completo', sa.String(length=20), nullable=True))
    
    # Crear índice único para búsquedas rápidas
    op.create_index('idx_caso_numero_completo', 'casos', ['numero_caso_completo'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar índice
    op.drop_index('idx_caso_numero_completo', table_name='casos')
    
    # Eliminar campo numero_caso_completo
    op.drop_column('casos', 'numero_caso_completo')
