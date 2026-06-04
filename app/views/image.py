from os import path, SEEK_END
from werkzeug.utils import secure_filename
from uuid import uuid4
from mimetypes import guess_type
from PIL import Image as PILImage
from quart import Blueprint, request, render_template, g, jsonify, send_from_directory
from app.settings import settings
from app.models import Image
from app.crud import ImageCrud


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
    session = g.db_session
    crud = ImageCrud(session)
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
    file_path = path.join(settings.UPLOAD_FOLDER, filename) 
    
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
    await crud.save_image(image)
    
    return jsonify({
        'status': 'success',
        'data': image.to_dict()
    }), 201


@bp.route('/<int:id>', methods=['GET'])
async def get_image_info(id: int):
    """获取图片信息"""
    session = g.db_session
    crud = ImageCrud(session)
    image = await crud.get_image_by_id(id)
    if image is None:
        return await render_template('common/notfound.html'), 404
    else:
        return jsonify(image.to_dict())

@bp.route('/<filename>')
async def serve_image(filename: str):
    """提供图片访问"""
    return await send_from_directory(settings.UPLOAD_FOLDER, filename)

# @app.route('/images', methods=['GET'])
# async def list_images():
#     """图片列表"""
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 20, type=int)
    
#     pagination = Image.query.order_by(Image.upload_time.desc()).paginate(
#         page=page, per_page=per_page
#     )
    
#     return jsonify({
#         'total': pagination.total,
#         'pages': pagination.pages,
#         'current_page': page,
#         'images': [img.to_dict() for img in pagination.items]
#     })


# @app.route('/images/<int:image_id>/resize')
# def resize_image(image_id):
#     """动态缩放图片"""
#     width = request.args.get('width', type=int)
#     height = request.args.get('height', type=int)
    
#     if not width and not height:
#         return jsonify({'error': '需要指定width或height'}), 400
    
#     image = Image.query.get_or_404(image_id)
#     file_path = path.join(app.config['UPLOAD_FOLDER'], image.filename)
    
#     img = PILImage.open(file_path)
    
#     # 计算缩放尺寸
#     if width and height:
#         new_size = (width, height)
#     elif width:
#         ratio = width / img.width
#         new_size = (width, int(img.height * ratio))
#     else:
#         ratio = height / img.height
#         new_size = (int(img.width * ratio), height)
    
#     img = img.resize(new_size, PILImage.Resampling.LANCZOS)
    
#     # 返回缩放后的图片
#     from io import BytesIO
#     img_io = BytesIO()
#     img.save(img_io, img.format or 'JPEG')
#     img_io.seek(0)
    
#     return app.response_class(img_io, mimetype=image.mime_type)