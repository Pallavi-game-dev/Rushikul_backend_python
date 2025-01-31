from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import getDB
from src.utils import getResponse
router = APIRouter(tags=["Customer"])

@router.post("/upload", status_code=status.HTTP_200_OK)
def save_image(file_path: List[str] = Depends(upload_image), item_id: int = Form(...),
               current_user=Depends(get_current_user),
               db: Session = Depends(get_db)):
    try:
        for item in file_path:
            file_data = ItemImage(image_url=item,
                                  item_id=item_id, created_by=current_user.user_id)
            db.add(file_data)
        db.commit()
        return {"message": "Item Image added Successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something Went Wrong")

if not os.path.exists(setting.UPLOAD):
    os.makedirs(setting.UPLOAD)

async def upload_image(request: Request, file: List[UploadFile] = File(...)):
    image_list = []
    for image in file:
        if not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is not an image."
            )
        file_path = os.path.join(setting.UPLOAD, image.filename)

        # Save the file to the specified directory
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_list.append(file_path)

    return image_list
