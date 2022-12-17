function createElement(tag, attrs) {
	const keys = Object.keys(attrs || {});
	const el = document.createElement(tag);
	for (let i = 0; i < keys.length; ++i) {
		el.setAttribute(keys[i], attrs[[keys[i]]]);
	}
	return el;
}

function createNoticeitem(item, isNotice) {
	const itemDiv = createElement("div", { class: "notice-item" });

	const BlogImgContainer = createElement("a", {
		class: "notice-blog-img-container",
		href: `https://velog.io/@${item.user}/`,
		target: "_blank",
	});

	const itemBlogImg = createElement("img", {
		src: item.user_img,
		class: "notice-blog-img",
	});

	BlogImgContainer.append(itemBlogImg);

	const itemTitle = createElement("a", {
		class: "notice-post-title",
		href: `https://velog.io/@${item.user}/${item.link}`,
		target: "_blank",
	});

	itemTitle.innerHTML = item.title;
	const itemDate = createElement("div", { class: "notice-date" });

	if (isNotice) {
		itemTitle.setAttribute("style", "width : 350px;");
		itemTitle.setAttribute("href", item.link);
		itemDate.setAttribute("style", "width : 0;padding : 0;");
		itemDate.innerHTML = "";
	} else {
		itemDate.innerHTML = item.created_at.substring(5, 10);
	}

	itemDiv.append(BlogImgContainer, itemTitle, itemDate);
	return itemDiv;
}

function createNoticeItems() {
	const noticeItemsDiv = createElement("div", { class: "notice-item-div" });
	chrome.runtime.sendMessage(
		{
			message: "get_new_post",
		},
		(response) => {
			if (response.data.length == 0) {
				const items = [
					{
						user_img:
							"https://lh3.googleusercontent.com/QO4AoAGH0U9IcMouWT_m2GNvMy4P4eFwmEpVxakU4xOwGH9YpGMSgsU5alalzZf2PFg6KGL3DbA0khc8a7xiNQnuwg=w128-h128-e365-rj-sc0x00ffffff",
						link: "https://github.com/junah201/velog-helper",
						title: "Velog Helper를 사용해보세요!",
					},
					{
						user_img:
							"https://lh3.googleusercontent.com/QO4AoAGH0U9IcMouWT_m2GNvMy4P4eFwmEpVxakU4xOwGH9YpGMSgsU5alalzZf2PFg6KGL3DbA0khc8a7xiNQnuwg=w128-h128-e365-rj-sc0x00ffffff",
						link: "https://github.com/junah201/velog-helper",
						title: "새 글 알림이 없습니다.",
					},
					{
						user_img:
							"https://lh3.googleusercontent.com/QO4AoAGH0U9IcMouWT_m2GNvMy4P4eFwmEpVxakU4xOwGH9YpGMSgsU5alalzZf2PFg6KGL3DbA0khc8a7xiNQnuwg=w128-h128-e365-rj-sc0x00ffffff",
						link: "https://github.com/junah201/velog-helper",
						title: "블로그에 가서 별 모양 북마크 버튼을 눌러보세요.",
					},
					{
						user_img:
							"https://lh3.googleusercontent.com/QO4AoAGH0U9IcMouWT_m2GNvMy4P4eFwmEpVxakU4xOwGH9YpGMSgsU5alalzZf2PFg6KGL3DbA0khc8a7xiNQnuwg=w128-h128-e365-rj-sc0x00ffffff",
						link: "https://github.com/junah201/velog-helper",
						title: "이미 눌렀다면 잠시만 기다려주세요. (최대 15분)",
					},
				];

				items.forEach(function (item, index, array) {
					noticeItemsDiv.append(
						createNoticeitem((item = item), (isNotice = true))
					);
				});
			}

			response.data.forEach(function (item, index, array) {
				noticeItemsDiv.append(
					createNoticeitem((item = item), (isNotice = false))
				);
			});
		}
	);
	return noticeItemsDiv;
}

function createBlogItems() {
	const blogItemsDiv = createElement("div", { class: "blog-item-div" });
	chrome.runtime.sendMessage(
		{
			message: "get_blogs",
		},
		(response) => {
			response.blogs.forEach(function (item, index, array) {
				const blogItemDiv = createElement("div", { class: "blog-item" });
				const blogImg = createElement("img", {
					class: "blog-img",
					src: item.profile_img,
				});
				const blogName = createElement("a", {
					class: "blog-name",
					href: `https://velog.io/@${item.id}`,
					target: "_blank",
				});
				const blogRemoveButton = createElement("button", {
					class: "blog-remove-button",
					value: item.id,
				});
				blogName.innerHTML = item.id;
				blogItemDiv.append(blogImg, blogName, blogRemoveButton);
				blogItemsDiv.append(blogItemDiv);

				blogRemoveButton.addEventListener("click", (e) => {
					chrome.runtime.sendMessage(
						{
							message: "delete_bookmark",
							payload: e.target.value,
						},
						(response) => {
							if (response.message === "success") {
								console.log("success delete bookmark");
								e.path[1].classList.add("undisplay");
							}
						}
					);
				});
			});
		}
	);
	return blogItemsDiv;
}
