from app.database import SessionLocal
from app.models import Conversation
from sqlalchemy import func

def fix_updated_at():
    """Fix null updated_at values in existing conversations"""
    db = SessionLocal()
    try:
        # Update all conversations with null updated_at
        result = db.query(Conversation).filter(Conversation.updated_at == None).update(
            {Conversation.updated_at: func.now()},
            synchronize_session=False
        )
        
        db.commit()
        print(f"✅ Fixed {result} conversations with null updated_at")
        
    except Exception as e:
        print(f"❌ Error fixing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_updated_at()


