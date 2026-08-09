import type { NavBarLink } from "@/types/navBarConfig";

export const LinkPresets: Record<string, NavBarLink> = {
	Home: { name: "主页", url: "/", icon: "material-symbols:home" },
	About: { name: "关于我", url: "/about/", icon: "material-symbols:person" },
	Archive: { name: "归档", url: "/archive/", icon: "material-symbols:archive" },
	Friends: { name: "友链", url: "/friends/", icon: "material-symbols:group" },
	Sponsor: { name: "打赏", url: "/sponsor/", icon: "material-symbols:favorite" },
	Guestbook: { name: "留言", url: "/guestbook/", icon: "material-symbols:chat" },
	Bangumi: { name: "番组计划", url: "/bangumi/", icon: "material-symbols:movie" },
	Gallery: { name: "相册", url: "/gallery/", icon: "material-symbols:photo-library" },
};
