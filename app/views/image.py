from os import path, SEEK_END
from werkzeug.utils import secure_filename
from mimetypes import guess_type
from PIL import Image as PILImage
from quart import Blueprint, request, render_template, g, jsonify, send_from_directory
from app.settings import settings
from app.models import Image
from app.services import ImageService
from app.utils import generate_unique_filename


bp = Blueprint('image', __name__)


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['POST'])
async def upload_image():
    """图片上传接口"""
    service = ImageService(g.db_session)
    files = await request.files
    if 'file' not in files:
        return jsonify({'error': '没有文件'}), 400

    file = files['file']

    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件类型'}), 400

    original_filename = secure_filename(file.filename)
    filename = generate_unique_filename(original_filename)
    file_path = path.join(settings.IMAGE_UPLOAD_FOLDER, filename)

    file.seek(0, SEEK_END)
    file_size = file.tell()
    file.seek(0)

    mime_type = guess_type(filename)[0] or 'application/octet-stream'

    try:
        img = PILImage.open(file)
        width, height = img.size
        img = img.convert('RGB')
        img.save(file_path, 'JPEG', quality=85, optimize=True)
    except Exception as e:
        return jsonify({'error': f'图片处理失败: {str(e)}'}), 400

    image = Image(
        filename=filename,
        original_filename=original_filename,
        user_id='b483d5ef443444e7a1b8388545bd7038',
        file_size=file_size,
        mime_type=mime_type,
        width=width,
        height=height
    )
    await service.save(image)

    return jsonify({
        'status': 'success',
        'data': image.to_dict()
    }), 201


@bp.route('/<filename>/info', methods=['GET'])
async def get_image_info(filename: str):
    """获取图片信息"""
    service = ImageService(g.db_session)
    image = await service.get_by_filename(filename)
    if image is None:
        return await render_template('common/notfound.html'), 404
    else:
        return jsonify(image.to_dict())


@bp.route('/<filename>')
async def serve_image(filename: str):
    """提供图片访问"""
    service = ImageService(g.db_session)
    await service.record_view(filename)
    return await send_from_directory(settings.IMAGE_UPLOAD_FOLDER, filename)
