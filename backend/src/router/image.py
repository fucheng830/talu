from fastapi import Depends, HTTPException
from fastapi import UploadFile, File

import hashlib
import os
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Image

from fastapi import APIRouter
from io import BytesIO
from starlette.responses import StreamingResponse

router = APIRouter()

@router.get("/image/{image_name}")
async def get_image(image_name: str, db: Session = Depends(get_db)):
    id, format = image_name.split(".")

    image = db.query(Image).filter_by(id=id).first()
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    # Convert the binary data to a file-like object
    file_like = BytesIO(image.image_data)

    # Determine the MIME type from the format
    mime_type = f"image/{image.format.lower()}"
    # Stream the image back to the client
    # 添加Cache-Control头部
    headers = {
        "Cache-Control": "public, max-age=31536000",  # 例如，这里设置缓存有效期为一年
        "ETag": id  # 使用图片的md5值作为ETag，确保图片更新时缓存也会更新
    }
    return StreamingResponse(file_like, media_type=mime_type, headers=headers)


@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    # 这里的contents就是上传的图片文件，现在你可以对图片文件做你想要的操作
    # 比如保存为图片文件等
    md5_hash = hashlib.md5()
    md5_hash.update(contents)
    
    id = md5_hash.hexdigest()
    ext = os.path.splitext(file.filename)[1]
    # 去掉.
    ext = ext[1:]
    
    result = db.query(Image).filter_by(id=id).first()
    if not result:
        new_image = Image(
            id=id,
            image_data=contents,
            format=ext.lower()
        )
        db.add(new_image)
        db.commit()
    static_url = os.environ.get("STATIC_URL", "http://site.123qiming.com")
    return {
        "status": 'Success',
        "message": 'Image uploaded successfully',
        "data": {
            "image_id": id,
            "image_url": f"{static_url}/image/{id}.{ext}"
        }
    }