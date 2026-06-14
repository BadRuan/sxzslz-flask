from os import SEEK_END, path
from quart import Blueprint, request, render_template, g, jsonify, send_from_directory
from app.settings import settings
from app.services.attachment_services import AttachmentService


bp = Blueprint('attachment', __name__)

@bp.route('/upload', methods=['POST'])
async def upload_attachment():
    """附件上传接口"""
    service = AttachmentService(g.db_session)
    files = await request.files
    if 'file' not in files:
        return jsonify({'error': '没有文件'}), 400

    file = files['file']

    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    file.seek(0, SEEK_END)
    file_size = file.tell()
    file.seek(0)

    attachment = await service.save(file.filename, file_size)

    save_path = path.join(settings.ATTACHMENT_UPLOAD_FOLDER, attachment.filename)
    await file.save(save_path)

    return jsonify({
        'status': 'success',
        'data': attachment.to_dict()
    }), 201


@bp.route('/<filename>/info', methods=['GET'])
async def get_attachment_info(filename: str):
    """获取文件信息"""
    service = AttachmentService(g.db_session)
    attachment = await service.get_by_filename(filename)
    if attachment is None:
        return await render_template('common/notfound.html'), 404
    else:
        return jsonify(attachment.to_dict())


@bp.route('/<filename>')
async def serve_attachment(filename: str):
    """提供文件访问"""
    service = AttachmentService(g.db_session)
    attachment = await service.get_by_filename(filename)
    if attachment is None:
        return await render_template('common/notfound.html'), 404
    else:
        await service.record_download(filename)
        return await send_from_directory(
            settings.ATTACHMENT_UPLOAD_FOLDER,
            filename,
            as_attachment=True,
            attachment_filename=attachment.original_filename
        )
