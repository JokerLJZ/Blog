import type { GalleryConfig } from "@/types/config";

// 相册配置
export const galleryConfig: GalleryConfig = {
	// 相册列表（目前为空，请在此添加自己的相册）
	// 添加方法：每个数组项是一个相册，并在 public/gallery/<id>/ 目录放入图片
	// 支持 jpg/png/webp/avif/gif 格式，字段示例如下：
	//   id: 相册唯一标识符（用于目录命名和URL路径），如 id: "travel-2025" 对应 public/gallery/travel-2025/
	//   cover: 手动指定封面图（可选，不填则用 cover.* 文件，没有则用第一张图片）
	//   name: 相册名称
	//   description: 相册描述
	//   location: 拍摄地点
	//   date: 日期，格式 YYYY-MM-DD，用于排序和显示
	//   tags: 标签数组
	//   password / passwordHint: 访问密码及提示（可选）
	// 示例：
	//   {
	//     id: "travel-2025",
	//     name: "旅行随拍",
	//     description: "一些路上的风景。",
	//     date: "2025-01-01",
	//     tags: ["旅行"],
	//   },
	albums: [],

	// 瀑布流最小列宽(px)，浏览器根据容器宽度自动计算列数，默认 240
	// 值越小列数越多，值越大列数越少
	columnWidth: 240,
};
