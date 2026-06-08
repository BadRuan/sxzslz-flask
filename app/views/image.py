from os import path, SEEK_END
from werkzeug.utils import secure_filename
from uuid import uuid4
from mimetypes import guess_type
from PIL import Image as PILImage
from quart import Blueprint, request, render_template, g, jsonify, send_from_directory
from app.settings import settings
from app.models import Image
from app.services import ImageService


bp = Blueprint('image', __name__)


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """生成唯一文件名，防止冲突"""
    ext = filename.rsplit('.', 1)[1].lower()
    return f"{uuid4().hex}.{ext}"

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
    
    # 安全处理文件名
    original_filename = secure_filename(file.filename)
    
    # 生成唯一文件名
    filename = generate_unique_filename(original_filename)
    file_path = path.join(settings.IMAGE_UPLOAD_FOLDER, filename) 
    
    # 获取文件信息
    file.seek(0, SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    # 获取MIME类型
    mime_type = guess_type(filename)[0] or 'application/octet-stream'
    
    # 使用Pillow处理图片（验证+压缩）
    try:
        img = PILImage.open(file)
        width, height = img.size

        # 转换为 RGB 并压缩保存
        img = img.convert('RGB')
        img.save(file_path, 'JPEG', quality=85, optimize=True)

    except Exception as e:
        return jsonify({'error': f'图片处理失败: {str(e)}'}), 400
    
    # 保存到数据库
    image = Image(
        filename=filename,
        original_filename=original_filename,
        file_size=file_size,
        mime_type=mime_type,
        width=width,
        height=height
    )
    await service.save_image(image)
    
    return jsonify({
        'status': 'success',
        'data': image.to_dict()
    }), 201


@bp.route('/<filename>/info', methods=['GET'])
async def get_image_info(filename: str):
    """获取图片信息"""
    session = g.db_session
    service = ImageService(session)
    image = await service.get_by_filename(filename)
    if image is None:
        return await render_template('common/notfound.html'), 404
    else:
        return jsonify(image.to_dict())

@bp.route('/<filename>')
async def serve_image(filename: str):
    """提供图片访问"""
    return await send_from_directory(settings.IMAGE_UPLOAD_FOLDER, filename)
