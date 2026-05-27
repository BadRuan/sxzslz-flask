from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class PostContent(Base):
    __tablename__: str = "post_contents"

    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    markdown_content: Mapped[str] = mapped_column(Text, nullable=False)
    html_content: Mapped[str] = mapped_column(Text)
    