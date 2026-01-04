from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from typing import Generator

router = APIRouter(prefix="/file")


@router.post("/small")
async def upload_small_file(file: bytes = File(...)):
    try:
        return {"file_size": len(file)}
    except Exception as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.post("/large")
async def upload_large_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": len(contents),
        "message": "文件上传成功",
    }


@router.get("/small/{filename}")
async def get_small_file(filename: str):
    return FileResponse(f"{filename}")


def gen_file(path: str) -> Generator[bytes, None, None]:
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):  # 读取 1MB 的块
            yield chunk


@router.get("/large/{filename}")
async def get_large_file(filename: str):
    gen_exp = gen_file(f"{filename}")
    response = StreamingResponse(content=gen_exp, status_code=200)
    # response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
