from os import SEEK_END, path
from werkzeug.utils import secure_filename
from uuid import uuid4
from quart import Blueprint, request, render_template, g, jsonify, send_from_directory
from app.settings import settings
from app.models import Attachment
from app.crud import AttachmentCrud


bp = Blueprint('attachment', __name__)


def generate_unique_filename(filename):
    """生成唯一文件名，防止冲突"""
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid4().hex}.{ext}"

@bp.route('/upload', methods=['POST'])
async def upload_attachment():
    """附件上传接口"""
    session = g.db_session
    crud = AttachmentCrud(session)
    files = await request.files
    if 'file' not in files: 
        return jsonify({'error': '没有文件'}), 400
    
    file = files['file']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    # 安全处理文件名
    original_filename = secure_filename(file.filename)
    
    # 生成唯一文件名
    filename = generate_unique_filename(original_filename)
    # 获取文件信息
    file.seek(0, SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # 保存到数据库
    attachment = Attachment(
        filename=filename,
        original_filename=original_filename,
        file_size=file_size,
    )
    
    save_path = path.join(settings.ATTACHMENT_UPLOAD_FOLDER, filename)
    await file.save(save_path)
    await crud.save_attachment(attachment)
    
    return jsonify({
        'status': 'success',
        'data': attachment.to_dict()
    }), 201


@bp.route('/<filename>/info', methods=['GET'])
async def get_attachment_info(filename: str):
    """获取文件信息"""
    session = g.db_session
    crud = AttachmentCrud(session)
    image = await crud.get_by_filename(filename)
    if image is None:
        return await render_template('common/notfound.html'), 404
    else:
        return jsonify(image.to_dict())

@bp.route('/<filename>')
async def serve_attachment(filename: str):
    """提供文件访问"""
    session = g.db_session
    crud = AttachmentCrud(session)
    file = await crud.get_by_filename(filename)
    if file is None:
        return await render_template('common/notfound.html'), 404
    else:
        return await send_from_directory(
            settings.ATTACHMENT_UPLOAD_FOLDER, 
            filename,
            as_attachment=True,
            attachment_filename= file.original_filename
        )
