import os
import re
from PIL import Image


# 每张长图最多包含的图片数量
BATCH_SIZE = 25


def output_exists(subfolder_path, subfolder_name):
    """检查子文件夹下是否已存在拼接好的长图
    命名形式:
      - 单张: 子文件夹名.png
      - 分批: 子文件夹名1.png, 子文件夹名2.png ...
    """
    # 单张形式
    single = f"{subfolder_name}.png"
    if os.path.exists(os.path.join(subfolder_path, single)):
        return True
    # 分批形式: 子文件夹名 + 数字 + .png
    pattern = re.compile(
        r"^" + re.escape(subfolder_name) + r"\d+\.png$", re.IGNORECASE
    )
    for f in os.listdir(subfolder_path):
        if pattern.match(f):
            return True
    return False


def stitch_batch(images, output_path):
    """将一组图片纵向拼接并保存"""
    if not images:
        return

    max_width = max(img.width for img in images)
    total_height = sum(img.height for img in images)

    result = Image.new("RGBA", (max_width, total_height))
    y_offset = 0
    for img in images:
        # 宽度不足时居中粘贴
        x_offset = (max_width - img.width) // 2
        result.paste(img, (x_offset, y_offset))
        y_offset += img.height

    if result.mode == "RGBA":
        result = result.convert("RGB")

    result.save(output_path, "PNG")
    print(f"  已保存: {output_path} ({max_width}x{total_height})")
    result.close()


def stitch_images(subfolder_path):
    """将子文件夹下 original/第1话 中的图片纵向拼接为长图
    - 图片 <= BATCH_SIZE: 输出 子文件夹名.png
    - 图片 >  BATCH_SIZE: 分批输出 子文件夹名1.png, 子文件夹名2.png ...
    """
    subfolder_name = os.path.basename(subfolder_path)

    # 若已存在长图则跳过
    if output_exists(subfolder_path, subfolder_name):
        print(f"  跳过: 已存在拼接好的长图")
        return False

    original_dir = os.path.join(subfolder_path, "original", "第1话")
    if not os.path.isdir(original_dir):
        print(f"  跳过: original/第1话 不存在")
        return False

    # 收集所有 png 图片并按文件名排序
    png_files = sorted(
        [f for f in os.listdir(original_dir) if f.lower().endswith(".png")]
    )
    if not png_files:
        print(f"  跳过: 第1话 文件夹内无 PNG 图片")
        return False

    total = len(png_files)

    # 图片数量未超过阈值: 单张输出
    if total <= BATCH_SIZE:
        print(f"  找到 {total} 张图片，拼接为单张长图...")
        images = []
        for fname in png_files:
            img_path = os.path.join(original_dir, fname)
            images.append(Image.open(img_path))
        output_path = os.path.join(subfolder_path, f"{subfolder_name}.png")
        stitch_batch(images, output_path)
        for img in images:
            img.close()
        return True

    # 图片数量超过阈值: 分批输出
    batch_count = (total + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"  找到 {total} 张图片，分 {batch_count} 批拼接（每批 {BATCH_SIZE} 张）...")

    batch_index = 1
    for start in range(0, total, BATCH_SIZE):
        batch_files = png_files[start:start + BATCH_SIZE]

        images = []
        for fname in batch_files:
            img_path = os.path.join(original_dir, fname)
            images.append(Image.open(img_path))

        # 输出命名: 子文件夹名1.png, 子文件夹名2.png ...
        output_path = os.path.join(
            subfolder_path, f"{subfolder_name}{batch_index}.png"
        )
        stitch_batch(images, output_path)

        for img in images:
            img.close()

        batch_index += 1

    return True


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"工作目录: {base_dir}\n")

    subfolders = sorted([
        f for f in os.listdir(base_dir)
        if os.path.isdir(os.path.join(base_dir, f))
    ])

    success_count = 0
    fail_count = 0

    for sf in subfolders:
        sf_path = os.path.join(base_dir, sf)
        print(f"处理: {sf}")
        if stitch_images(sf_path):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n完成! 成功 {success_count} 个, 跳过 {fail_count} 个")


if __name__ == "__main__":
    main()
