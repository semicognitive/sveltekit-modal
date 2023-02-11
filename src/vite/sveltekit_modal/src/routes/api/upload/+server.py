from fastapi import Form, File, UploadFile

async def POST(pdf: UploadFile = File(), token: str = Form()):
    return {
        "file_size": len(pdf.file.read()),
        "token": token,
        "file_content_type": pdf.content_type,
    }
