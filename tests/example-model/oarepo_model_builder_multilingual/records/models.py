from invenio_db import db
from invenio_records.models import RecordMetadataBase


class OarepoModelBuilderMultilingualMetadata(db.Model, RecordMetadataBase):
    """Model for OarepoModelBuilderMultilingualRecord metadata."""

    __tablename__ = "oarepo_model_builder_multilingual_metadata"

    # Enables SQLAlchemy-Continuum versioning
    __versioned__ = {}
