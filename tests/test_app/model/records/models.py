from invenio_db import db
from invenio_records.models import RecordMetadataBase


class ModelMetadata(db.Model, RecordMetadataBase):
    """Model for ModelRecord metadata."""

    __tablename__ = "model_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
