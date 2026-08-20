import type { CoverImageConfig } from "../types/config";

/**
 * 文章封面图配置
 *
 * enableInPost - 是否在文章详情页显示封面图
 *
 * 随机封面图使用说明：
 * 1. 未设置 image 的文章会根据文章 id 稳定抽取一张本地封面图
 * 2. 在文章的 Frontmatter 中添加 image: "api" 仍可使用随机图 API
 *
 * // 文章 Frontmatter 示例：
 * ---
 * title: 文章标题
 * image: "api"
 * ---
 */
export const coverImageConfig: CoverImageConfig = {
	// 是否在文章详情页显示封面图
	enableInPost: true,

	randomCoverImage: {
		// 随机封面图功能开关
		enable: true,
		// 未指定封面的文章从这里稳定随机抽取，顺序变化会改变已有文章的分配
		localImages: [
			"/assets/images/article-covers/anime-sakura.png",
			"/assets/images/article-covers/anime-bamboo.jpg",
			"/assets/images/article-covers/pastel-clock.jpg",
			"/assets/images/article-covers/love-letter.jpg",
			"/assets/images/article-covers/autumn-leaves.jpg",
			"/assets/images/article-covers/study-desk.jpg",
			"/assets/images/article-covers/anime-red-bow.png",
			"/assets/images/article-covers/elf-sunlight.jpg",
			"/assets/images/article-covers/blue-mountain-elf.png",
		],
		// 封面图API列表
		apis: [
			"https://t.alcy.cc/pc",
			"https://www.dmoe.cc/random.php",
			"https://uapis.cn/api/v1/random/image?category=acg&type=pc",
		],
	},
};
