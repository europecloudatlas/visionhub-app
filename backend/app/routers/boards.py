"""
Vision Board routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Board, BoardImage
from ..schemas import (
    BoardCreate,
    BoardUpdate,
    BoardResponse,
    BoardListItem,
    BoardImageResponse
)
from ..dependencies import get_current_user
from ..storage import upload_image, delete_image

router = APIRouter(prefix="/boards", tags=["Vision Boards"])


# ==========================================
# BOARD CRUD
# ==========================================

@router.get("/", response_model=List[BoardListItem])
def get_my_boards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all boards for current user"""
    boards = db.query(Board).filter(Board.user_id == current_user.id).all()
    
    return [
        {
            "id": board.id,
            "name": board.name,
            "description": board.description,
            "created_at": board.created_at,
            "image_count": len(board.images)
        }
        for board in boards
    ]


@router.get("/{board_id}", response_model=BoardResponse)
def get_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get board with all images"""
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    return board


@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    board_data: BoardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new vision board"""
    new_board = Board(
        user_id=current_user.id,
        name=board_data.name,
        description=board_data.description
    )
    
    db.add(new_board)
    db.commit()
    db.refresh(new_board)
    
    return new_board


@router.patch("/{board_id}", response_model=BoardResponse)
def update_board(
    board_id: int,
    board_data: BoardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update board name/description"""
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    if board_data.name is not None:
        board.name = board_data.name
    if board_data.description is not None:
        board.description = board_data.description
    
    db.commit()
    db.refresh(board)
    
    return board


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(
    board_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete board and all images"""
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    # Delete all images from S3
    for image in board.images:
        delete_image(image.filename)
    
    # Delete board (cascade deletes images from DB)
    db.delete(board)
    db.commit()


# ==========================================
# IMAGE CRUD
# ==========================================

@router.post("/{board_id}/images", response_model=BoardImageResponse, status_code=status.HTTP_201_CREATED)
async def upload_image_to_board(
    board_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload image to board"""
    # Verify board exists and belongs to user
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Upload to S3
    try:
        image_url, filename = upload_image(file.file, file.filename)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )
    
    # Save to database
    new_image = BoardImage(
        board_id=board_id,
        image_url=image_url,
        filename=filename
    )
    
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    
    return new_image


@router.delete("/{board_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_image_from_board(
    board_id: int,
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete image from board"""
    # Verify board belongs to user
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.user_id == current_user.id
    ).first()
    
    if not board:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found"
        )
    
    # Find image
    image = db.query(BoardImage).filter(
        BoardImage.id == image_id,
        BoardImage.board_id == board_id
    ).first()
    
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found"
        )
    
    # Delete from S3
    delete_image(image.filename)
    
    # Delete from database
    db.delete(image)
    db.commit()