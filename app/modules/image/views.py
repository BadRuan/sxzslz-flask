from quart import Blueprint, request, render_template, g, jsonify, send_from_directory
from app.settings import settings
from app.modules.image.services import ImageService
from app.utils import get_current_user_id


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

    user_id = get_current_user_id()
    image = await service.upload(file, user_id)

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
